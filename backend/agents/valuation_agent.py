from crewai import Agent
import litellm

class ValuationAgent:
    def __init__(self):
        self.agent = Agent(
            name="Stock Valuation Agent",
            role="Stock Market Valuation Expert",
            goal="Analyze stock valuation metrics and financial ratios.",
            backstory="An AI agent specialized in assessing stock valuation based on earnings, growth, and market trends.",
            llm="gpt-4o",
        )

    def run(self, task, query, data):
        """Processes stock valuation analysis based on the given task"""
        return self.analyze_valuation(query, data)

    def analyze_valuation(self, query, data):
        """Uses LLM to generate stock valuation analysis"""
        prompt = f"""
        Perform a **detailed stock valuation analysis** based on financial metrics.
        
        **Query:** {query}
        
        **Sample Data (First 5 Entries):** {data[:5]}
        
        **Key Valuation Metrics to Analyze:**
        - Price-to-Earnings (P/E) ratio
        - Price-to-Book (P/B) ratio
        -  Earnings per Share (EPS) trends
        -  Market Cap and Growth Projection
        -  Industry comparison
        
        Provide a structured report with charts if necessary.
        """

        try:
            response = litellm.completion(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Error in valuation analysis: {str(e)}"

# Initialize the ValuationAgent
valuation_agent = ValuationAgent()
