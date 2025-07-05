from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from serpapi import GoogleSearch
import os
import json

model = SentenceTransformer('all-MiniLM-L6-v2')
SERP_API_KEY = os.getenv("SERPAPI_KEY", "0e51dd65f52e130c8df9cf71b6bf0ef9495e255422837061d0b6c9192eaf2254")

def load_products(filepath="data/products.json"):
    with open(filepath, "r") as f:
        return json.load(f)

def embed_text(text):
    return model.encode([text])[0]

def recommend_products(user_query, products, top_k=2):
    user_vec = embed_text(user_query)
    scores = []

    for product in products:
        full_text = f"{product['name']} {product['description']} {' '.join(product['tags'])}"
        product_vec = embed_text(full_text)
        score = cosine_similarity([user_vec], [product_vec])[0][0]
        scores.append((product, score))

    top_matches = sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
    return [
        {
            "product": match[0],
            "score": round(match[1] * 100),
            "reason": generate_reason(user_query, match[0])
        } for match in top_matches
    ]

def generate_reason(user_query, product):
    reasons = []
    if "vegan" in user_query:
        reasons.append("vegan-friendly")
    if "protein" in user_query:
        reasons.append("high in protein")
    if "summer" in user_query or "light" in user_query:
        reasons.append("ideal for summer")
    if f"₹{product['price']}" in user_query or "under" in user_query:
        reasons.append(f"under your ₹{product['price']} budget")
    if "casual" in user_query:
        reasons.append("great for casual wear")

    if reasons:
        return f"This product is {', '.join(reasons)} — {product['description']}"
    else:
        return f"Matches your query — {product['description']}"

def fetch_live_products(query, num_results=3):
    if not SERP_API_KEY:
        return []

    params = {
        "engine": "google",
        "q": query,
        "tbm": "shop",
        "api_key": SERP_API_KEY,
        "gl": "in",
        "hl": "en",
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    products = []
    for item in results.get("shopping_results", [])[:num_results]:
        products.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "price": item.get("price"),
            "source": item.get("source"),
            "thumbnail": item.get("thumbnail")
        })
    return products
