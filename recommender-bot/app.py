import streamlit as st
from utils import load_products, recommend_products

def main():
    st.set_page_config(page_title="E-Commerce Recommender Bot", layout="centered")

    st.title("🛍️ Personalized E-Commerce Recommender")
    st.markdown("Hello! What are you looking for today?")

    query = st.text_input("Enter your preference (e.g., 'vegan snacks under ₹300')")

    if "history" not in st.session_state:
        st.session_state.history = []

    if query:
        products = load_products()
        results = recommend_products(query, products)

        st.session_state.history.append({"query": query, "results": results})

        st.markdown("### 🔎 Recommendations")
        for res in results:
            st.write(f"**{res['product']['name']}** - ₹{res['product']['price']}")
            st.write(f"Confidence: {res['score']}%")
            st.write(f"_Why it's perfect:_ {res['reason']}")
            st.markdown("---")

    st.markdown("---")
    st.markdown("🧠 Powered by Sentence Transformers + Cosine Similarity")
    st.caption("Built for Indian D2C brands | Budget-aware | Culturally aware")

if __name__ == "__main__":
    main()
