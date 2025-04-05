# financial_crew.py


from backend.core.report_generator import save_report_as_pdf

from backend.api.tasks import (
    fetch_company_overview,
    fetch_financial_performance,
    compute_stock_valuation,
    analyze_risks,
    generate_stock_rating,
    generate_full_report
)
from backend.agents.web_agent import WebAgent
from backend.agents.snowflake_agent import SnowflakeAgent
from backend.agents.code_agent import CodeAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.valuation_agent import ValuationAgent
from backend.agents.report_agent import ReportAgent

class FinancialCrew:
    def __init__(self):
        self.tasks = [
            fetch_company_overview,
            fetch_financial_performance,
            compute_stock_valuation,
            analyze_risks,
            generate_stock_rating,
            generate_full_report
        ]

        # ✅ This mapping connects task.name to the wrapper instance that has a `.run()` method
        self.agent_wrappers = {
            "Company Overview": WebAgent(),
            "Financial Performance": SnowflakeAgent(),
            "Stock Valuation": CodeAgent(),
            "Financial Risk Analysis": RiskAgent(),
            "Investment Recommendation": ValuationAgent(),
            "Generate Structured Financial Report": ReportAgent()
        }

        self.agents = {
            "web_agent": WebAgent(),
            "snowflake_agent": SnowflakeAgent(),
        }


        self.tasks = [fetch_company_overview, fetch_financial_performance, generate_full_report]  # Add tasks here
 
    def _normalize_section_output(self, section):
        """Ensure each report section is a clean string (flatten lists if needed)."""
        if isinstance(section, list):
            return "\n".join([str(s) for s in section])
        return str(section)

    def generate_financial_report(self, query, data, serp_articles, start_date):
        report_sections = []
        chart_path = None

        for task in self.tasks:
            if task.name == "Financial Performance":
                section = self.agent_wrappers[task.name].run(
                    task=task.description,
                    query=query,
                    data=data
                )

                # ❌ Skip appending if it's a list of dicts
                if isinstance(section, list) and all(isinstance(x, dict) for x in section):
                    print("[Financial Performance] returned raw data (skipping append to report).")
                    continue

            elif task.name == "Company Overview":
                _ = self.agent_wrappers[task.name].run(
                    task=task.description,
                    query=query,
                    data={ "serp_articles": serp_articles}
                )
                continue  # ✅ Don't add this to report

            else:
                section = self.agent_wrappers[task.name].run(
                    task=task.description,
                    query=query,
                    data=data
                )
            report_sections.append(self._normalize_section_output(section))

        for key, agent in self.agents.items():
            task_description = f"Executing {key} analysis for {query}"
            section = agent.run(task=task_description, query=query, data=data)

            if isinstance(section, str):
                report_sections.append(self._normalize_section_output(section))
            elif isinstance(section, list) and all(isinstance(x, dict) for x in section):
                # Skip appending raw list of dicts
                print(f"[{key}] returned structured data (skipped appending raw dicts)")
            else:
                print(f"[{key}] returned unexpected type ({type(section)})")



        report_text = "\n\n".join(report_sections)
        save_report_as_pdf(report_text, "downloaded_report.pdf")

        return report_text, chart_path
