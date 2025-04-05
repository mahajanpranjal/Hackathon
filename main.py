from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
import os
import re
from dotenv import load_dotenv
import requests
import litellm
import matplotlib.pyplot as plt
from backend.core.crew import FinancialCrew  
from backend.agents.web_agent import web_agent
from backend.agents.snowflake_agent import SnowflakeAgent
from backend.agents.code_agent import CodeAgent
from backend.core.report_generator import save_report_as_pdf
from backend.agents.report_agent import ReportAgent
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
# Load environment variables
load_dotenv()
 
# FastAPI Initialization
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# API Keys
openai_api_key = os.getenv("OPENAI_API_KEY")
'''
def generate_stock_image_with_openai(query: str) -> List[str]:
    """Generates AI-based images using OpenAI's DALL-E for financial insights."""
    try:
        image_prompts = [
            f"A high-resolution stock market analysis chart showing financial trends of {query}, designed for a business report.",
            f"A sentiment heatmap for {query}, showing investor sentiment and market movements.",
            f"A futuristic AI-generated financial infographic explaining stock price movements and economic trends for {query}.",
            f"A well-designed competitive market positioning chart for {query}, showing its industry rivals and market share."
        ]
        
        image_urls = []
        for prompt in image_prompts:
            response = litellm.image_generation(
                model="dall-e-3",
                prompt=prompt,
                api_key=openai_api_key
            )
            image_url = response.get("data", [{}])[0].get("url", None)
            if image_url:
                image_urls.append(image_url)

        return image_urls
    except Exception as e:
        print(f"❌ Error generating images: {str(e)}")
        return []
'''
# Request Model
class QueryRequest(BaseModel):
    query: str
    sentiment: Optional[str] = "neutral"
 
# Function to detect the company from the query
def detect_company(query: str):
    q = query.lower()
    if "apple" in q:
        return "AAPL_STOCK_HISTORY", "Apple Inc"
    elif "meta" in q or "facebook" in q:
        return "META_STOCK_HISTORY", "Meta Platforms"
    return None, None

 
# Function to detect the time period from the query
def detect_duration(query: str) -> datetime:
    q = query.lower()
    patterns = [
        (r'last (\d+) days?', lambda match: datetime.now() - timedelta(days=int(match.group(1)))),
        (r'last (\d+) weeks?', lambda match: datetime.now() - timedelta(weeks=int(match.group(1)))),
        (r'last (\d+) months?', lambda match: datetime.now() - timedelta(days=int(match.group(1)) * 30)),
    ]
 
    for pattern, func in patterns:
        match = re.search(pattern, q)
        if match:
            return func(match)
 
    return datetime.now() - timedelta(days=30)  # Default to last 30 days
 
 
# FastAPI route to handle stock research queries
from fastapi.responses import PlainTextResponse
import traceback
@app.get("/download_report")
def download_report():
    file_path = "static/reports/downloaded_report.pdf"
    return FileResponse(file_path, media_type='application/pdf', filename="financial_report.pdf")


@app.post("/search")
async def search(request: QueryRequest):
    try:
        query = request.query
        sentiment = request.sentiment

        table_name, company_name = detect_company(query)

        if not table_name:
            return JSONResponse(content={"error": "Company not identified in query."}, status_code=400)


        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        snowflake_agent = SnowflakeAgent()
        data = snowflake_agent.fetch_data(query, table_name, start_date, end_date)


        if not data:
            return JSONResponse(content={"error": "No stock data found for the given period."}, status_code=404)
        
        code_agent = CodeAgent()
        # Generate chart via code agent (NEW ADDITION)
        chart_result = code_agent.run(query, data)
        print("📊 Chart Result:", chart_result)
        print("🧠 Generated Code Preview:\n", chart_result["generated_code"][:300])

        
        report_agent = ReportAgent()
        generated_code = chart_result["generated_code"]
      


        financial_crew = FinancialCrew()
        # Inside your search function
        #news = web_agent.fetch_news(company_name)
        serp_articles = web_agent.serp_api_search(query, company_name, sentiment)


        
        financial_report_tuple = financial_crew.generate_financial_report(
        query, data, serp_articles, start_date
    )
        financial_report = financial_report_tuple[0]  # Extract the report text only

         
        # ✅ Generate AI-Based Financial Images
        #ai_generated_images = generate_stock_image_with_openai(query)

            # ✅ Save the Full Report as PDF with Images
        pdf_filename = "downloaded_report.pdf"
        save_report_as_pdf(financial_report, filename=pdf_filename)


            


        return JSONResponse(content={
            "company": company_name,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "financial_report": financial_report,
            "chart_path": chart_result.get("chart_path"),
            "generated_code": generated_code,
            #"ai_generated_images": ai_generated_images,  
            "pdf_report": pdf_filename  
        }, status_code=200)

    except Exception as e:
        traceback.print_exc()  # prints to terminal
        return PlainTextResponse("Internal Server Error: " + str(e), status_code=500)
