from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from serpapi import GoogleSearch
import google.generativeai as genai
import json

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# API Keys
SERP_API_KEY = "0e51dd65f52e130c8df9cf71b6bf0ef9495e255422837061d0b6c9192eaf2254"
GEMINI_API_KEY = "AIzaSyDOJcwmzHZfK8l77jgn1mpQVApunyY5zxQ"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

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
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        You are a helpful Indian shopping assistant.

        User Query: "{user_query}"

        Product:
        Name: {product['name']}
        Description: {product['description']}
        Price: ₹{product['price']}

        Explain in 1–2 sentences why this product is a perfect recommendation for the user.
        Be clear, friendly, and relevant to the user's intent.
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        # Fallback explanation
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

def generate_reason_for_live_product(user_query, product):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
            You are a helpful Indian fashion and lifestyle assistant.

            Here is a user's product search query:
            "{user_query}"

            Here is a product you found:
            Title: {product.get('title')}
            Price: {product.get('price')}
            Sold on: {product.get('source')}

            Based on the user's request, explain in 1-2 short sentences **why this product fits their needs**. Focus on attributes like:
            - Style (formal/casual/festive)
            - Fabric (machine-washable, breathable, sweat-resistant)
            - Price match
            - Occasion fit (workwear, summer use, etc.)
            - Any premium or useful feature inferred from the title

            Don't repeat the title — instead, summarize how it helps the user.
                    """

        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No explanation generated."

    except Exception as e:
        print(f"Error generating reason: {e}")
        return "Sorry, could not generate reason at this time."
