from crewai import Agent
import litellm
import os

class ReportAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Report Generator",
            role="Financial Report Creator",
            goal="Generate a structured financial analysis report for stock trends.",
            backstory="An AI agent specialized in analyzing stock market data and generating comprehensive reports.",
            llm="gpt-4o",
        )

    def run(self, task, query, data):
        """Processes financial data and generates a structured report."""
        return self.generate_code( task, query, data)  # Ensure correct parameter passing

    def generate_code(self, task, query, data):
            """Generates an in-depth financial research report with rich insights across all sections, targeting a minimum of 30 pages of detailed content."""

            prompt = f"""
            import matplotlib.pyplot as plt
            import datetime
            import pandas as pd
            # **Financial Research Report**
            ## **{query}**
            
            ## **Table of Contents**
            1. **Executive Summary**
            2. **Introduction to {query}**
            3. **Stock Overview**
            4. **Technical Analysis**
            5. **Fundamental Analysis**
            6. **Risk Assessment**
            7. **Market News Impact**
            8. **Investment Outlook**
            9. **Recommendations**
            10. **Conclusion**
            11. **References**
            
            ---
            
            ## - Executive Summary**
            This section provides a in-depth high-level overview of the financial health and investment potential of {query}. Key findings and major takeaways are summarized here, including revenue trends, market position, and risk factors.
            - Brief financial health overview.
            - Key investment takeaways and risk considerations.
            - Summary of technical and fundamental analysis insights.
            - Investment recommendation summary (Buy, Hold, or Sell).
            
            ---
            
            ## - Introduction to {query}**
            - Detailed company history, including foundation, growth trajectory, and strategic vision.
            - Core business segments and revenue sources.
            - Industry positioning and competitive landscape analysis.
            - SWOT analysis (Strengths, Weaknesses, Opportunities, and Threats).
            - Analysis of company innovations, recent acquisitions, and partnerships.
            
            ---
            
            ##  - Stock Overview**
            - Stock performance history, covering the past decade.
            - Comparative analysis with key industry players and market benchmarks.
            - Breakdown of major institutional investors and their holdings.
            - Price volatility trends and correlation with macroeconomic events.
            - Shareholder value creation strategy and past dividend performance.
            
            ---
            
            ## - Technical Analysis**
            - In-depth examination of **50-day and 200-day moving averages**.
            - **MACD, RSI, and Bollinger Bands** for momentum assessment.
            - **Key breakout levels and resistance trends**.
            - Historical trading volume analysis and its impact on price movement.
            - Pattern recognition (head & shoulders, double tops/bottoms).
            
            ---
            
            ## - Fundamental Analysis**
            - **Revenue and earnings growth analysis** over the last decade.
            - **EBITDA margins and cost structure** comparison with competitors.
            - **Return on Assets (ROA) and Return on Equity (ROE) trends**.
            - **Debt burden assessment**, including interest coverage ratios.
            - **Future earnings forecast** using discounted cash flow (DCF) model.
            
            ---
            
            ## - Risk Assessment**
            - Market risk: Inflation, interest rate changes, and geopolitical influences.
            - Industry risks: Regulatory constraints and technological disruptions.
            - Financial risks: Leverage ratios, liquidity issues, and debt maturity profile.
            - Operational risks: Supply chain vulnerabilities and production costs.
            - Company-specific risks: Leadership stability and governance concerns.
            
            ---
            
            ## - Market News Impact**
            - Influence of recent macroeconomic events and regulatory changes.
            - Impact of mergers, acquisitions, or restructuring on stock price.
            - Sentiment analysis of major financial news headlines.
            - Assessment of how company announcements affect investor confidence.
            
            ---
            
            ## - Investment Outlook**
            - **Short-term projections (1-6 months)** based on trend analysis.
            - **Long-term forecast (3-5 years)** leveraging economic indicators.
            - **Growth drivers and future expansion plans**.
            - **Sector performance trends** and industry cycles impact.
            - **Potential catalysts for future stock price movement**.
            
            ---
            
            ## - Recommendations**
            - Comprehensive Buy/Hold/Sell recommendation based on multi-factor analysis.
            - Optimal entry and exit price ranges based on valuation models.
            - Alternative investment strategies (diversification and hedging options).
            - Risk-adjusted return evaluation for different investor profiles.
            - Analyst consensus and forecast revisions.
            
            ---
            
            ## - Conclusion**
            A in-depth final summary of the key insights, investment potential, and risk factors for {query}, incorporating both qualitative and quantitative evaluations.
            
            ---
            
            ## - References**
            Citations for financial reports, industry benchmarks, news sources, and analyst research.
            
            ---
            
            **Stock Data Overview:**
            {data[:5]}  # Sample data for analysis.
            
             **Additional Instructions for AI:**
            - Aim to generate a comprehensive report with **at least 4000–5000 words**.
            - Include detailed **quantitative analysis**, comparisons, charts (describe in text), and relevant formulas.
            - Provide **realistic hypothetical data** when specific numbers are missing.
            - Write as if presenting to **institutional investors or analysts**.
            - Expand **each section** to include examples, commentary, and industry trends.
            - For each section, include **bullet points**, **paragraphs**, and **subsections** where necessary.
            -create more 15 pages of report.
            Include **at least 2–3 well-explained bullet points and 7-8 subpoints** under *every major heading*.

            """

            try:
                response = litellm.completion(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    api_key=os.getenv("OPENAI_API_KEY")
                )

                content = response['choices'][0]['message']['content']
                return content.strip()
            except Exception as e:
                print(f"\u274c Error generating report: {str(e)}")
                return "No valid report generated."

# Instantiate the agent
report_agent = ReportAgent()
