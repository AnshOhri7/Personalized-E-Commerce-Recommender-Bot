import streamlit as st
from utils import fetch_live_products, generate_reason_for_live_product

def main():
    st.set_page_config(page_title="E-Commerce Recommender Bot", layout="centered")

    st.title("🛍️ Rasa(रस) - Personalized E-Commerce Recommender Bot")
    st.markdown("Hello! What are you looking for today?")

    query = st.text_input("Enter your preference (e.g., 'vegan snacks under ₹300')")

    if query:
        with st.spinner("Searching the internet for best matches..."):
            live_results = fetch_live_products(query)

        st.markdown("### 🌐 Top Picks from the Internet")
        if live_results:
            for item in live_results:
                with st.container():
                    cols = st.columns([1, 3])
                    with cols[0]:
                        st.image(item.get("thumbnail", ""), width=100)
                    with cols[1]:
                        st.markdown(
                            f"<h4><a href='{item.get('link')}' target='_blank' style='text-decoration:none;color:#4F8BF9;'>{item.get('title')}</a></h4>",
                            unsafe_allow_html=True
                        )
                        st.markdown(f"💰 **{item.get('price', 'N/A')}**")
                        st.markdown(f"🛒 *{item.get('source', 'Unknown')}*")

                        # Add Gemini-generated explanation
                        reason = generate_reason_for_live_product(query, item)
                        print(f"\nProduct: {item.get('title')}\nReason: {reason}")
                        st.markdown(f"🧠 _Rasa Says:_ {reason}")
                    st.markdown("---")
        else:
            st.warning("No live results available. Try another query or check your internet.")

    st.markdown("---")
    st.markdown("🧠 Powered by Gemini + SerpAPI + Streamlit")
    st.caption("Built for Indian D2C brands | Budget-aware | Culturally aware")
    st.markdown("""
        <style>
        .stMarkdown h4 {
            margin-bottom: 0.3rem;
        }
        .stMarkdown p {
            margin-top: 0;
            margin-bottom: 0.2rem;
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
