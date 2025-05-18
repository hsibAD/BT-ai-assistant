import streamlit as st
from news_api import get_news
from exchange_api import get_price
from market_data_api import get_market_data
from ai_response import extract_keywords, generate_ai_response
from token_resolver import resolve_token

# Популярные токены (для фильтрации ключевых слов)

st.set_page_config(page_title="AI Crypto Assistant", page_icon="🧠", layout="centered")
st.title("🧠 AI Crypto Assistant (Natural Language + Ollama)")

query = st.text_input("Ask a crypto-related question (e.g., What's up with Ethereum?):")

if st.button("Get Info"):
    if query:
        with st.spinner("🤖 Thinking... extracting keywords..."):
            keywords = extract_keywords(query)
            st.markdown("### 🧠 AI Thought Process")
            st.markdown(f"**Extracted keywords:** `{', '.join(keywords)}`")

        # Определяем токен из извлечённых ключей
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
                    response = generate_ai_response(query, collected_data)

                # СНАЧАЛА — ОТВЕТ
                st.markdown("### 🤖 Final Answer")
                st.markdown(f"""
<div style="border: 1px solid #ccc; padding: 16px; border-radius: 8px; background-color: #f9f9f9;">
{response}
</div>
""", unsafe_allow_html=True)

                # ПОТОМ — ДАННЫЕ
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
