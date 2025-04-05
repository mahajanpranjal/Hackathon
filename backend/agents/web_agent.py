from crewai import Agent
import requests
import os

class WebAgent:
    def __init__(self):
        self.agent = Agent(
            name="Web Research Agent",
            role="Financial News Fetcher",
            goal="Fetches company-related news and market trends.",
            backstory="An AI agent specialized in gathering financial news from the web to help traders make informed decisions.",
            llm="gpt-4o",
        )
        self.serp_api_key = os.getenv("WEB_SEARCH_API_KEY")

    def format_news_bulletpoints(self, serp_articles, query):
        bullets = [f"📰 News and Articles for '{query}':\n"]


        if isinstance(serp_articles, list):
            bullets.append("\n🔍 SERP Articles:\n")
            for art in serp_articles:
                title = art.get("title", "No title")
                link = art.get("link", "#")
                snippet = art.get("snippet", "")
                source = art.get("source", "Unknown")
                bullets.append(f"- **{title}** ({source}): {snippet} [Link]({link})")

        return "\n".join(bullets)

     
    def run(self, task, query, data):
        #news = data.get("news") if isinstance(data, dict) else None
        serp_articles = data.get("serp_articles") if isinstance(data, dict) else None

        #if not news:
         #   news = self.fetch_news(query)
        if not serp_articles:
            serp_articles = self.serp_api_search(query=query, company=query, sentiment="finance")

        # ✅ Return only the formatted string, not full dict
        return self.format_news_bulletpoints (serp_articles, query)


    '''
    def fetch_news(self, company):
        try:
            api_key = os.getenv("NEWS_API_KEY")
            url = f"https://newsapi.org/v2/everything?q={company}&apiKey={api_key}"
            response = requests.get(url)
            news_data = response.json()

            if "articles" in news_data:
                return news_data["articles"][:5]
            else:
                return "No news available."
        except Exception as e:
            return f"Failed to fetch news. Error: {str(e)}"
    '''
    def serp_api_search(self, query: str, company: str, sentiment: str):
        if sentiment != "finance":
            return {"error": "Sentiment must be 'finance' for stock-related queries."}

        url = "https://serpapi.com/search"
        params = {
            'q': f"{company} stock",
            'api_key': self.serp_api_key,
            'engine': 'google',
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if "organic_results" not in data:
                return {"error": "No organic_results found in API response"}

            articles = []
            for i, result in enumerate(data["organic_results"][:5]):
                if isinstance(result, dict):
                    article = {
                        'title': result.get("title", "No Title"),
                        'link': result.get("link", "#"),
                        'snippet': result.get("snippet", ""),
                        'source': result.get("source", "Unknown"),
                    }
                    articles.append(article)
                    if i >= 4:
                        break

            return articles
        else:
            return {"error": f"Failed to fetch data from SERP API. Status code: {response.status_code}"}

# Initialize the WebAgent
web_agent = WebAgent()
