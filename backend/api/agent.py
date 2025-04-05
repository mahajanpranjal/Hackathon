from crewai import Agent
from openai import OpenAI

# Initialize OpenAI model for agents
llm = OpenAI(model="gpt-4")

# ✅ Web Agent: Fetches company overview (NO financials)
web_agent = Agent(
    name="Web Agent",
    role="Fetches company overview, market presence, and business operations.",
    backstory="Expert in retrieving non-financial corporate information.",
    llm=llm
)

# ✅ Snowflake Agent: Fetches historical financial performance (NO projections)
snowflake_agent = Agent(
    name="Snowflake Agent",
    role="Fetches revenue, earnings, and cash flow from the financial database.",
    backstory="Specialist in historical financial data extraction.",
    llm=llm
)

# ✅ Code Agent: Computes stock valuation metrics (NO revenue/earnings)
code_agent = Agent(
    name="Code Agent",
    role="Executes stock valuation models (DCF, P/E, volatility).",
    backstory="Quantitative finance expert in stock analysis.",
    llm=llm
)

# ✅ News Agent: Fetches latest financial news (NO historical data)
news_agent = Agent(
    name="News Agent",
    role="Finds market trends, competitor activity, and financial news.",
    backstory="Financial journalist tracking real-time industry trends.",
    llm=llm
)

# ✅ Risk Agent: Analyzes financial risks (NO valuation)
risk_agent = Agent(
    name="Risk Agent",
    role="Identifies financial risks from economic and industry reports.",
    backstory="Risk assessment expert analyzing stock price stability.",
    llm=llm
)

# ✅ Valuation Agent: Provides stock rating (NO charts/data)
valuation_agent = Agent(
    name="Valuation Agent",
    role="Gives final investment recommendation based on all insights.",
    backstory="Equity research expert providing stock ratings.",
    llm=llm
)

# ✅ Report Generator Agent: Creates full structured report (NO duplicate text)
report_agent = Agent(
    name="Report Generator",
    role="Compiles all insights into a structured, non-repetitive report.",
    backstory="Expert in financial reporting and structured document creation.",
    llm=llm
)
