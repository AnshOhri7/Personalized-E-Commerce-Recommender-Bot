import streamlit as st
from utils import load_products, recommend_products, fetch_live_products

def main():
    st.set_page_config(page_title="E-Commerce Recommender Bot", layout="centered")

    st.title("🛍️ Rasa - Personalized E-Commerce Recommender Bot")
    st.markdown("Hello! What are you looking for today?")

    query = st.text_input("Enter your preference (e.g., 'vegan snacks under ₹300')")

    if "history" not in st.session_state:
        st.session_state.history = []

    if query:
        # products = load_products()
        # results = recommend_products(query, products)
        live_results = fetch_live_products(query)

        # st.session_state.history.append({"query": query, "results": results})


        st.markdown("### 🔎 Recommendations")
        # if results:
        #     for res in results:
        #         st.write(f"**{res['product']['name']}** - ₹{res['product']['price']}")
        #         st.write(f"Confidence: {res['score']}%")
        #         st.write(f"_Why it's perfect:_ {res['reason']}")
        #         st.markdown("---")
        # else:
        #     st.info("No local recommendations found.")

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
                    st.markdown("---")
        else:
            st.warning("No live results available. Try another query or check your internet.")

        # st.markdown("### 🔎 Recommendations")
        # st.markdown("### 🌐 Top Picks from the Internet")
        # if live_results:
        #     for item in live_results:
        #         st.image(item['thumbnail'], width=100)
        #         st.markdown(f"**[{item['title']}]({item['link']})**")
        #         st.markdown(f"💰 {item['price']} — 🛒 {item['source']}")
        #         st.markdown("---")
        # elif not live_results and results:
        #     for res in results:
        #         st.write(f"**{res['product']['name']}** - ₹{res['product']['price']}")
        #         st.write(f"Confidence: {res['score']}%")
        #         st.write(f"_Why it's perfect:_ {res['reason']}")
        #         st.markdown("---")
        # else:
        #     st.info("Could not fetch live results. Check API key or query.")

    st.markdown("---")
    st.markdown("🧠 Powered by Sentence Transformers + Cosine Similarity")
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
