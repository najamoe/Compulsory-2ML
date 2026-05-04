from app.agents.research_agent import run_agent
import asyncio

if __name__ == "__main__":
    query = input("Enter topic: ")
    result = asyncio.run(run_agent(query))
    print(result)