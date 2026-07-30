from app.rag import retrieve
from app.llm import ask_llm


def analyze(name):
    # Retrieve only the most relevant document
    results = retrieve(name, top_k=1)

    if not results:
        return "No relevant information was found in the EcoChemAI knowledge base."

    result = results[0]

    context = result["text"]

    prompt = f"""
You are EcoChemAI.

Your ONLY source of information is the knowledge base below.

KNOWLEDGE BASE:
{context}

USER INGREDIENT:
{name}

STRICT GROUNDING RULES:
1. Use ONLY facts explicitly present in the knowledge base.
2. NEVER use your general knowledge.
3. NEVER add facts that are not present in the knowledge base.
4. NEVER infer that an ingredient is safe or unsafe.
5. NEVER suggest alternatives unless they are explicitly listed.
6. NEVER add regulatory information unless it is explicitly listed.
7. If information for a requested section is missing, write exactly:
   "Not available in the current EcoChemAI knowledge base."
8. Do not recommend external websites, doctors, regulators, or other sources.
9. Do not add warnings or claims that are not present in the knowledge base.

Return exactly:

Function:
Safety information:
Health concerns:
Environmental impact:
Safer alternatives:
"""
    
    return ask_llm(prompt)
    
