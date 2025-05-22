import streamlit as st
from news_api import get_news
from exchange_api import get_price
from market_data_api import get_market_data
from ai_response import extract_keywords, generate_ai_response
from token_resolver import resolve_token
import re

st.set_page_config(page_title="AI Crypto Assistant", page_icon="🧠", layout="centered")
st.title("🧠 AI Crypto Assistant")

query = st.text_input("Ask a crypto-related question (e.g., What's up with Ethereum?):")

def escape_markdown(text):
    return re.sub(r'([*_`\[\]()~])', r'\\\1', text)

if st.button("Get Info"):
    if query:
        with st.spinner("🤖 Thinking... extracting keywords..."):
            keywords = extract_keywords(query)
            st.markdown("### 🧠 AI Thought Process")
            st.markdown(f"**Extracted keywords:** `{', '.join(keywords)}`")

        # 🔍 Нет ключевых слов → сгенерировать ответ напрямую
        if not keywords:
            with st.spinner("🤖 Generating general answer..."):
                fallback_prompt = (
                    "The user asked: \"" + query + "\"\n\n"
                    "You are a cryptocurrency assistant. If the question is not directly about a cryptocurrency, "
                    "briefly explain the topic (if you know it), then politely state that you specialize in crypto-related queries "
                    "and suggest the user ask about coins, tokens, prices, or news."
                )
                fallback_response = generate_ai_response(query, fallback_prompt)
                st.markdown("### 🤖 Final Answer")
                st.markdown(f"""
        <div style="border: 1px solid #ccc; padding: 16px; border-radius: 8px; background-color: #f9f9f9;">
        {fallback_response}
        </div>""", unsafe_allow_html=True)
        else:
            # 🔁 Обычный режим: найти token и собрать данные
            token = None
            for kw in keywords:
                token = resolve_token(kw)
                if token:
                    break

            if token:
                with st.spinner("📡 Collecting data..."):
                    news = get_news(token)
                    price = get_price(token)
                    market_data = get_market_data(token)

                    collected_data = f"""
🔑 Token: {token}
News:
{chr(10).join(news)}
{price}
{market_data}
                    """

                    with st.spinner("🧠 Generating AI Answer..."):
                        raw_response = generate_ai_response(query, collected_data)
                        response = escape_markdown(raw_response)

                    st.markdown("### 🤖 Final Answer")
                    st.markdown(f"""
<div style="border: 1px solid #ccc; padding: 16px; border-radius: 8px; background-color: #f9f9f9;">
{response}
</div>
""", unsafe_allow_html=True)

                    st.markdown("### 📊 Collected Data")
                    st.markdown(f"**🔑 Token:** `{token.upper()}`")

                    st.markdown("---\n### 📰 News")
                    for item in news:
                        st.markdown(f"- {item}")

                    st.markdown(f"\n---\n### 💸 Price\n{price}")
                    st.markdown(f"\n---\n### 📊 Market Data\n{market_data}")
            else:
                st.warning("⚠️ AI couldn't identify a valid crypto token in your question.")
    else:
        st.warning("Please ask something about crypto.")
