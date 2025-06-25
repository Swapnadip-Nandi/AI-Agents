from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai

import os
from dotenv import load_dotenv 
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Web Search Agent
# This agent is designed to search the web for financial information and provide insights based on the latest
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the information you need.",
    model=Groq(id="llama-3-70b-8192-tools-use-preview"),
    tools=[
        DuckDuckGo()],
        instructions=["Alwaya include the source of the information you find."],
        show_tool_calls=True,
        markdown=True,
)

## Financial Agent
# This agent is designed to provide financial insights and analysis using the YFinance API.

finance_agent = Agent(
    name="Financial Agent",
    role="Analyze financial data and provide insights.",
    model=Groq(id="llama-3-70b-8192-tools-use-preview"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True,
                      company_news = True)],
        instructions=["Use Tables to present financial data clearly.",
                      "Always include the source of the information you find."],
        show_tool_calls=True,
        markdown=True,
)

multi_ai_agent = Agent(
    team=[web_search_agent, finance_agent],
    instructions=["Always include the source", "Use Tables to present financial data clearly."],
    show_tool_calls=True,
    markdown=True,
)
# This agent combines the capabilities of both the web search and financial agents to provide comprehensive financial insights.

multi_ai_agent.print_response("Summarize Analyst recommendations and share the latest news for NVIDIA",stream=True)

