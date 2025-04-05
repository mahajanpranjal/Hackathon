from crewai import Agent
import litellm

class RiskAgent:
    def __init__(self):
        self.agent = Agent(
            name="Risk Assessment Agent",
            role="Financial Risk Analyzer",
            goal="Analyze financial risks associated with stock investments.",
            backstory="An AI agent specialized in assessing financial risks based on historical data and market trends.",
            llm="gpt-4o",
        )

    def run(self, task, query, data):
        """Processes financial risk analysis based on a given task"""
        return self.analyze_risk(query, data)

    def analyze_risk(self, query, data):
        """Uses LLM to analyze financial risks based on market trends"""
        prompt = f"""
        Perform a **detailed financial risk analysis** for stock investments.
        
        **Query:** {query}
        
        **Sample Data (First 5 Entries):** {data[:5]}
        
        **Key Risk Areas to Analyze:**
        -  Market trends and volatility
        -  Global financial risks (e.g., inflation, economic downturns)
        -  Company-specific risks (e.g., revenue loss, leadership changes)
        -  Competitor performance impact
        
        Provide a structured analysis and recommendations.
        """

        try:
            response = litellm.completion(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Error in risk analysis: {str(e)}"

# Initialize the RiskAgent
risk_agent = RiskAgent()
