from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

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

