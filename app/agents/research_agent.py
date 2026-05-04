from email.mime import message
from urllib import response

from autogen import AssistantAgent, UserProxyAgent
from app.tools.openalex import search_papers
import asyncio
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API")
LLM_CONFIG = {
    "config_list": [
        {
            "model": "open-mistral-nemo",
            "api_key": API_KEY,
            "api_type": "mistral",
            "api_rate_limit": 0.25,
            "temperature": 0.0,
        }
    ]
}

assistant = AssistantAgent(
    name="ResearchAgent",
    llm_config=LLM_CONFIG,
    system_message=""",
    
You are a research agent.

You MUST use the tool `search_papers`.
Do NOT make up papers.
Only return results from the tool.
"""
)


async def run_agent(query):
    topic, year, min_citations = parse_query(query)

    papers = search_papers(topic, year, min_citations)

    if not papers:
        return "No paper found that satisfies the constraints."

    best_paper = sorted(papers, key=lambda x: x["citations"], reverse=True)[0]

    message = f"""
    Here is a research paper:

    {best_paper}

    Explain in 5-7 sentences:
    - why this paper matches the user request
    - why it is relevant

    Do not invent information.
    """

    user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1
        )

    response = user_proxy.initiate_chat(
    assistant,
    message=message
)

    explanation = response.summary

    return {
        "title": best_paper["title"],
        "authors": best_paper["authors"],
        "year": best_paper["year"],
        "citations": best_paper["citations"],
        "source": "OpenAlex",
        "url": best_paper["url"],
        "explanation": explanation
    }

def parse_query(text: str):
    year = None
    min_citations = None

    # year (e.g. 2022)
    year_match = re.search(r"(20\d{2})", text)
    if year_match:
        year = int(year_match.group(1))

    # citations (e.g. "at least 100 citations")
    citation_match = re.search(r"(\d+)\s+citations", text)
    if citation_match:
        min_citations = int(citation_match.group(1))

    return text, year, min_citations