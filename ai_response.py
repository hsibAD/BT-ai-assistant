import subprocess
import re

def extract_keywords(question):
    prompt = f"""
You are a cryptocurrency domain assistant. Your task is to extract only **cryptocurrency tokens** from the user's question.

A valid token is one that appears on public exchanges like Binance or CoinGecko. Only include names, symbols (e.g., 'btc', 'eth'), or token IDs (e.g., 'cardano', 'solana') that are **explicitly mentioned** in the question.

Do NOT include generic terms like 'blockchain', 'wallet', 'mining', or any technologies, platforms, companies, or services (e.g., 'Ollama', 'MetaMask', 'Coinbase').

Output a **valid Python list of lowercase strings**, like:
["bitcoin", "eth", "solana"]

User question:
\"{question}\"
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

def escape_markdown(text):
    return re.sub(r'([*_`\[\]()~])', r'\\\1', text)

def generate_ai_response(user_question, collected_info):
    if len(collected_info) > 2000:
        collected_info = collected_info[:2000] + "\n...[truncated]"

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
        raw_output = result.stdout.strip()
        return escape_markdown(raw_output)
    except Exception as e:
        return f"Error generating answer: {e}"
