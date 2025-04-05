from crewai import Task
from backend.agents.web_agent import WebAgent
from backend.agents.snowflake_agent import SnowflakeAgent
from backend.agents.code_agent import CodeAgent
from backend.agents.report_agent import ReportAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.valuation_agent import ValuationAgent

web_agent_instance = WebAgent()
snowflake_agent_instance = SnowflakeAgent()
risk_agent_instance = RiskAgent()
valuation_agent_instance = ValuationAgent()
report_agent_instance =  ReportAgent()
code_agent_instance = CodeAgent()

# ✅ Company Overview Task
fetch_company_overview = Task(
    name="Company Overview",
    description="Gather details about the company's market presence and business operations.",
    agent=web_agent_instance.agent,
    expected_output="A structured summary of the company's history, market presence, industry, leadership, and operational highlights."
)

# ✅ Financial Performance Task
fetch_financial_performance = Task(
    name="Financial Performance",
    description="Extract revenue, earnings, and cash flow trends from Snowflake.",
    agent=snowflake_agent_instance.agent,
    expected_output="Tabular financial metrics including revenue growth, earnings per share (EPS), and cash flow trends over the specified time period."
)

# ✅ Stock Valuation Analysis Task
compute_stock_valuation = Task(
    name="Stock Valuation",
    description="Calculate DCF, P/E, SMA, and other stock price-related metrics.",
    agent=code_agent_instance.agent,
    expected_output="Valuation summary containing DCF analysis, price-to-earnings ratio, and moving average (SMA) trends with brief insights."
)

# ✅ Risk Assessment Task
analyze_risks = Task(
    name="Financial Risk Analysis",
    description="Evaluate company risk factors including market volatility and debt concerns.",
    agent=risk_agent_instance.agent,
    expected_output="Risk report outlining market-related threats, financial exposure, credit/debt ratios, and volatility analysis."
)

# ✅ Investment Recommendation Task
generate_stock_rating = Task(
    name="Investment Recommendation",
    description="Based on all sections, provide a stock rating (Buy/Hold/Sell).",
    agent=valuation_agent_instance.agent,
    expected_output="Clear investment recommendation (Buy/Hold/Sell) with rationale based on financial performance and valuation insights."
)

# ✅ Report Generation Task
generate_full_report = Task(
    name="Generate Structured Financial Report",
    description="Compile all sections into a structured, non-repetitive 20-25 page report.",
    agent=report_agent_instance,
    expected_output="Formatted, cohesive financial report with distinct sections covering company overview, financials, risks, valuation, and recommendation."
)
