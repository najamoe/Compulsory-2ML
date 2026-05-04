import asyncio
from app.agents.research_agent import run_agent
from app.evaluation.test_cases import test_cases
import re


def extract_constraints(prompt):
    year = None
    citations = None

    year_match = re.search(r"(20\d{2})", prompt)
    if year_match:
        year = int(year_match.group(1))

    citation_match = re.search(r"(\d+)\s+citations", prompt)
    if citation_match:
        citations = int(citation_match.group(1))

    return year, citations


def evaluate_result(result, prompt):
    score = {
        "relevant": 1,
        "year_correct": 1,
        "citations_ok": 1,
        "valid_source": 1,
        "no_hallucination": 1
    }

    # If no result returned
    if isinstance(result, str):
        return {k: 0 for k in score}

    year_constraint, citation_constraint = extract_constraints(prompt)

    # Check year
    if year_constraint and result["year"] != year_constraint:
        score["year_correct"] = 0

    # Check citations
    if citation_constraint and result["citations"] < citation_constraint:
        score["citations_ok"] = 0

    # Check URL exists
    if not result.get("url"):
        score["valid_source"] = 0

    # Basic hallucination check
    if not result.get("title") or not result.get("citations"):
        score["no_hallucination"] = 0

    return score


async def evaluate():
    all_scores = []

    for prompt in test_cases:
        print(f"\nRunning: {prompt}")

        result = await run_agent(prompt)
        print("Result:", result)

        score = evaluate_result(result, prompt)
        print("Score:", score)

        all_scores.append(score)

    # Aggregate results
    totals = {
        "relevant": 0,
        "year_correct": 0,
        "citations_ok": 0,
        "valid_source": 0,
        "no_hallucination": 0
    }

    for score in all_scores:
        for key in totals:
            totals[key] += score[key]

    print("\n=== FINAL RESULTS ===")
    for key, value in totals.items():
        print(f"{key}: {value}/{len(test_cases)}")


if __name__ == "__main__":
    asyncio.run(evaluate())