from crewai import Agent
import litellm
import os
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from typing import Optional
import re  # needed for code block extraction

class CodeAgent:
    def __init__(self):
        self.agent = Agent(
            role="Stock Valuation Expert",
            goal="Analyze stock metrics like DCF, P/E, and SMA to evaluate value.",
            backstory="You are a financial modeling expert skilled in quantitative analysis.",
            llm="gpt-4o"
        )

    def run(self, query, data):
        try:
            prompt = f"""
            You are a financial data analyst. Based on the stock data below, generate a matplotlib chart in Python.

            Requirements:
            - Plot \"Date\" on the X-axis
            - Plot \"Close\" prices on the Y-axis
            - Add a title and labels
            - Save chart as chart.png using plt.savefig(\"chart.png\")

            Sample Data:
            {data[:10]}

            Output only valid Python code:
            """

            response = litellm.completion(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                api_key=os.getenv("OPENAI_API_KEY")
            )

            content = response["choices"][0]["message"]["content"]
            code_block = re.search(r"```python(.*?)```", content, re.DOTALL)
            generated_code = code_block.group(1).strip() if code_block else content.strip()

            # 🔥 Remove plt.show() to prevent desktop popup
            cleaned_code = re.sub(r'plt\.show\(\)', '', generated_code)

            if not cleaned_code or not cleaned_code.strip():
                print(" Error: AI-generated code is empty or invalid.")
                return {"generated_code": "No valid code generated.", "chart_path": None}

            print("📊 Generated Matplotlib Code Preview:\n", cleaned_code[:500])

            chart_base64 = self.execute_generated_code(cleaned_code)

            
            if chart_base64 is None:
                print("Error: Chart generation failed.")
                return {"generated_code": generated_code, "chart_path": None}

            return {
                "generated_code": generated_code,
                "chart_path": chart_base64
            }

        except Exception as e:
            print(f"❌ Error in CodeAgent.run: {e}")
            return {"generated_code": "Error occurred", "chart_path": None}

    def execute_generated_code(self, code: str) -> Optional[str]:
        """Executes the generated code and returns the base64-encoded chart."""
        try:
            if not code or not code.strip():
                print(" Error: No valid code to execute.")
                return None

            local_vars = {}
            exec(code, {"plt": plt}, local_vars)

            img_buffer = BytesIO()
            plt.savefig(img_buffer, format="png")
            img_buffer.seek(0)

            encoded_image = base64.b64encode(img_buffer.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded_image}"

        except Exception as e:
            print(f" Error executing generated code: {str(e)}")
            return None

#  Instantiate the agent
code_agent = CodeAgent()