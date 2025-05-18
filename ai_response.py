import subprocess

def extract_keywords(question):
    prompt = f"""
You are a helpful assistant. Extract only cryptocurrency-related tokens, coins, or terms from the following user question. 
Do NOT invent or assume keywords. Only include those that are actually mentioned.

Return a valid Python list of lowercase strings (e.g., ["bitcoin", "cardano"]).

Question: "{question}"
Answer:
"""
    try:
        result = subprocess.run(["ollama", "run", "llama3", prompt],
                                capture_output=True, text=True, timeout=30)
        raw = result.stdout.strip()
        print("🪵 [KEYWORDS OUTPUT]:", raw)

        if "[" in raw and "]" in raw:
            list_text = raw[raw.index("["):raw.index("]")+1]
            return eval(list_text)
        else:
            return []
    except Exception as e:
        return [f"extraction_error: {e}"]

def generate_ai_response(user_question, collected_info):
    prompt = f"""
You are a crypto assistant. The user asked: "{user_question}"

Based on the collected data below, give a helpful, summarized answer in natural language.

Data:
{collected_info}

Answer:
"""
    try:
        result = subprocess.run(["ollama", "run", "llama3", prompt],
                                capture_output=True, text=True, timeout=60)
        return result.stdout.strip()
    except Exception as e:
        return f"Error generating answer: {e}"
