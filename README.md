Dette projekt implementerer en AI-baseret research agent, som kan finde relevante forskningsartikler baseret på en brugerforespørgsel.

Agenten kan:

forstå en forespørgsel (fx emne, år og citationskrav)
hente data fra en ekstern API
filtrere resultater efter krav
vælge den mest relevante artikel
give en kort, evidensbaseret forklaring

Agenten bruger ikke kun LLM-viden, men er baseret på faktiske data fra en ekstern kilde(openAlex), hvilket reducerer hallucination.
___

#Tech Stack
Python 3.11 (64-bit)
AutoGen (0.3.1 + kursus-fork)
Mistral AI (open-mistral-nemo)
OpenAlex API (research papers)
python-dotenv
requests

