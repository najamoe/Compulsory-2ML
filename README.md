# AI Research Agent
The agent can:
- Understand a request (e.g. subject, year or citations)
- Retrieve data from an external API (openAlex)
- Filtrate results by demands
- Choose the most relevant paper
- Give a short description of the paper

The Agent doesn't just use LLM-knowledge, but is based on actual data from the external API source (openAlex), which reduces hallucinations

The LLM is created using Mistral's API and the research papers are retrieved from the openAlex library. 
___

# The Agent workflow explained

1. Parsing (code)
      - Extracts the topic, publication year, and citation requirements from the user input

3. Tool (OpenAlex API)
      - Retrieves research papers from the external API

3. Filtering (code)
      - Removes papers that do not meet the specified constraints

4. Selection (code)
      - Selects the best paper (highest citation count)

5. Explanation (LLM)
      - Generates a short explanation of why the paper is relevant



# Tech Stack
Python 3.11 (64-bit)  
AutoGen (0.3.1)  
Mistral AI (open-mistral-nemo)  
OpenAlex API (research papers)  
python-dotenv  
requests   

--- 
# Setup
### **1. Clone Project**
      git clone <The projects url found on the project page>

### **2. Create Virutal environment** 
1. Make sure you are in the root of the project and run:

       py -3.11 -m venv .venv
  
2. Activate the virutal environment
   
       .venv\Scripts\activate

### **3. Install dependencies***
    pip install --upgrade pip setuptools wheel
    pip install autogen==0.3.1
    pip install mistralai==1.2.3
    pip install python-dotenv requests 

### **4. Configure API key**
1. Go to  [Mistral AI](https://mistral.ai) and retrive your API-key (requires a login to Mistral)
2. Create a .env file and add your key (API=YourKey)

---
# Running the project
run the project using:   

    python main.py

Test with an output like:  
"machine learning 2015 1000 citations"

---
# Running the evaluator   
    python -m app.evaluation.evaluator

This will:   
- Run 10 test prompts (located in evaluation -> test_cases.py  
- Evaluate the agents performance  
- Show the results like relevance and correctness



    
