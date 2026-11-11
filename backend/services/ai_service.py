import os
import json
import logging
from typing import List, Dict, Any, Optional
from models import db, Product, ProductVariant, Category

logger = logging.getLogger(__name__)

# Check for Gemini API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')

# Initialize Google GenAI client if key is available
client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("Google GenAI client successfully initialized with GEMINI_API_KEY.")
    except Exception as e:
        logger.warning(f"Could not initialize Google GenAI client: {e}")

AURA_STYLIST_SYSTEM_INSTRUCTION = """You are the Aura Atelier Concierge Privé, the private high-fashion wardrobe architect and personal stylist for AURA APPAREL.
Aura is an artisanal luxury house celebrated for quiet luxury, Venetian crystal aesthetics, and heritage tailoring in Mulberry Silk, Normandy Linen, Mongolian Cashmere, Biella Tropical Wool, and Tuscan Nappa Leather.

Your Persona:
- Cultured, discerning, sophisticated, polite, and warmly attentive.
- Master of silhouette balance, textile drape physics, and color harmony.
- You assemble capsule ensembles (2 to 4 pieces) tailored to specific occasions, climates, and patron aesthetics.

Guidelines:
1. Always suggest real Aura garments from the provided collection.
2. For each recommended piece, explain its drape, fabric quality, and why it harmonizes with the overall look.
3. Suggest the complete ensemble total and highlight styling pairings.
4. Keep advice elevated, concise, and inspiring. Never sound like a generic robotic bot.
"""

def search_aura_catalogue(query: str = "", category_name: str = "", max_price: float = None) -> List[Dict[str, Any]]:
    """Search active garments in Aura database by query, category, or price."""
    try:
        q = Product.query.filter_by(is_active=True)
        if category_name:
            cat = Category.query.filter(Category.name.ilike(f"%{category_name}%")).first()
            if cat:
                q = q.filter_by(category_id=cat.id)
        if query:
            q = q.filter(
                (Product.name.ilike(f"%{query}%")) |
                (Product.description.ilike(f"%{query}%")) |
                (Product.material.ilike(f"%{query}%"))
            )
        if max_price:
            q = q.filter(Product.base_price <= max_price)
        
        products = q.order_by(Product.average_rating.desc()).limit(8).all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "slug": p.slug,
                "category": p.category.name if p.category else "Ready-to-Wear",
                "base_price": p.base_price,
                "discount_price": p.discount_price,
                "material": p.material,
                "rating": p.average_rating,
                "primary_image": p.primary_image,
                "in_stock": p.total_stock > 0
            }
            for p in products
        ]
    except Exception as e:
        logger.error(f"Error querying Aura catalogue: {e}")
        return []

def get_product_context(product_id: int) -> Optional[Dict[str, Any]]:
    """Fetch complete product details with color/size variants for styling advice."""
    p = Product.query.get(product_id)
    if not p:
        return None
    return {
        "id": p.id,
        "name": p.name,
        "category": p.category.name if p.category else "Atelier",
        "description": p.description,
        "material": p.material,
        "fit_type": p.fit_type,
        "base_price": p.base_price,
        "discount_price": p.discount_price,
        "variants": [
            {"size": v.size, "color": v.color, "stock": v.stock_quantity}
            for v in p.variants
        ]
    }

class AuraAIService:
    @staticmethod
    def chat_with_concierge(messages: List[Dict[str, str]], image_data: Optional[str] = None) -> Dict[str, Any]:
        """
        Engage with the Aura Atelier Concierge Privé.
        Accepts conversation history and optional base64 image for multimodal styling.
        """
        user_message = messages[-1].get('content', '') if messages else ''
        
        # 1. First, search relevant Aura products based on client request
        extracted_keywords = user_message.lower()
        category_hint = ""
        for cat in ["dress", "shirt", "blazer", "linen", "knitwear", "denim", "trousers", "jacket", "coat", "boots", "shoes"]:
            if cat in extracted_keywords:
                category_hint = cat
                break
        
        matching_products = search_aura_catalogue(query=category_hint, category_name=category_hint)
        if not matching_products:
            matching_products = search_aura_catalogue(query="")[:6]

        # 2. If Gemini client is active, execute through Gemini 3.8 Flash
        if client and GEMINI_API_KEY:
            try:
                from google.genai import types
                
                catalogue_summary = json.dumps([
                    {
                        "id": p["id"],
                        "name": p["name"],
                        "category": p["category"],
                        "price": f"₹{p['discount_price'] or p['base_price']:,.2f}",
                        "material": p["material"]
                    }
                    for p in matching_products
                ])

                prompt_content = f"""Client Message: "{user_message}"

Available Authentic Aura Collection items for this inquiry:
{catalogue_summary}

Please provide your bespoke styling recommendation. Address the patron warmly, curate an ensemble using the available pieces above, explain the textile harmony and occasion appropriateness, and state the ensemble total."""

                contents: List[Any] = []
                if image_data:
                    # Multimodal vision request
                    import base64
                    try:
                        clean_b64 = image_data.split(',')[-1] if ',' in image_data else image_data
                        img_bytes = base64.b64decode(clean_b64)
                        contents.append(types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))
                        contents.append(f"The patron has uploaded this photograph of an item/aesthetic they wish to complement. {prompt_content}")
                    except Exception as img_err:
                        logger.warning(f"Failed to process image attachment: {img_err}")
                        contents.append(prompt_content)
                else:
                    contents.append(prompt_content)

                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=AURA_STYLIST_SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    )
                )

                ai_reply = response.text or "Allow me to present an ensemble curated from our atelier."
                return {
                    "reply": ai_reply,
                    "recommended_products": matching_products[:4],
                    "model": "gemini-3.8-flash",
                    "status": "success"
                }

            except Exception as e:
                logger.error(f"Gemini API generation error: {e}")
                # Fallback gracefully to luxury local stylist algorithm

        # 3. Intelligent Luxury Atelier Fallback Engine (Guarantees 100% uptime)
        selected_pieces = matching_products[:3]
        total_val = sum((p.get('discount_price') or p.get('base_price')) for p in selected_pieces)
        
        reply_intro = "Good day, Patron. For this occasion, I have orchestrated a bespoke capsule celebrating balanced proportions and effortless quiet luxury drape."
        if "gala" in extracted_keywords or "evening" in extracted_keywords or "wedding" in extracted_keywords:
            reply_intro = "For an illustrious evening affair, opulent texture and fluid lines take precedence. I have composed this evening ensemble honoring Italian and French tailoring."
        elif "linen" in extracted_keywords or "summer" in extracted_keywords or "beach" in extracted_keywords:
            reply_intro = "For warm coastal afternoons, breathable weave and natural linen drape provide supreme tactile ease without compromising elegance."
        elif "business" in extracted_keywords or "office" in extracted_keywords or "meeting" in extracted_keywords:
            reply_intro = "For commanding yet understated executive presence, crisp tailoring and rich leather craftsmanship establish an authoritative silhouette."

        pieces_text = "\n".join([
            f"• **{p['name']}** in {p['material']} ({p['category']}) — ₹{(p.get('discount_price') or p.get('base_price')):,.2f}"
            for p in selected_pieces
        ])

        ai_reply = f"""{reply_intro}

**Curated Ensemble:**
{pieces_text}

**Styling Notes:**
Pair these pieces with monochromatic neutrals or warm champagne jewelry. The drape allows breathability while maintaining structured poise from day into dusk.

**Curated Ensemble Total:** ₹{total_val:,.2f} *(Complimentary express courier shipping included)*"""

        return {
            "reply": ai_reply,
            "recommended_products": selected_pieces,
            "model": "aura-atelier-engine",
            "status": "success"
        }

    @staticmethod
    def generate_editorial_copy(name: str, material: str, category_name: str) -> Dict[str, Any]:
        """Generate high-fashion editorial product descriptions for the Admin Dashboard."""
        if client and GEMINI_API_KEY:
            try:
                from google.genai import types
                prompt = f"""Write an ultra-luxury editorial catalog description for an haute couture garment.
Product Name: {name}
Material: {material}
Category: {category_name}

Requirements:
- Evoke quiet luxury, tactile craftsmanship, and timeless elegance.
- Length: 2 to 3 poetic sentences highlighting weave, drape, and versatility.
- Tone: High-end luxury fashion house (Brunello Cucinelli / Loro Piana / The Row)."""

                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.7)
                )
                return {"description": response.text.strip(), "status": "success"}
            except Exception as e:
                logger.error(f"Error generating copy via Gemini: {e}")

        # Fallback copy generator
        desc = (
            f"Artfully tailored from exquisite {material}, this {name.lower()} embodies understated quiet luxury and fluid drape. "
            f"Mastercrafted with clean architectural lines, it transitions seamlessly from daytime engagements to intimate evening salons."
        )
        return {"description": desc, "status": "success"}

    @staticmethod
    def ask_fabric_advisor(product_id: int, question: str) -> Dict[str, Any]:
        """Answer tactile garment physics, breathability, and drape inquiries on PDP."""
        ctx = get_product_context(product_id)
        if not ctx:
            return {"answer": "Garment archives unavailable.", "status": "error"}

        if client and GEMINI_API_KEY:
            try:
                from google.genai import types
                prompt = f"""You are the Master Textile Artisan for Aura Apparel.
Garment: {ctx['name']}
Fabric Composition: {ctx['material']}
Fit: {ctx['fit_type']}
Client Question: "{question}"

Answer the patron concisely (2-3 sentences), explaining how this specific textile behaves, its breathability, wrinkle resistance, drape weight, and maintenance."""

                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.5)
                )
                return {"answer": response.text.strip(), "status": "success"}
            except Exception as e:
                logger.error(f"Error with fabric advisor Gemini: {e}")

        # Local fallback based on fabric analysis
        material = ctx.get('material', '').lower()
        if 'silk' in material:
            ans = f"Crafted from genuine {ctx['material']}, this piece offers a lustrous fluid drape that skims effortlessly over the body. It features natural thermoregulation and dry clean or delicate steam care is recommended."
        elif 'linen' in material:
            ans = f"Woven from premium {ctx['material']}, it provides maximum airflow and a relaxed, relaxed European drape. Natural softening occurs with wear, celebrating the organic texture of heirloom flax."
        elif 'cashmere' in material or 'wool' in material:
            ans = f"Spun from luxurious {ctx['material']}, it provides lightweight thermal insulation with zero bulk. The handle is remarkably soft and pill-resistant with proper knitwear cedar care."
        else:
            ans = f"Engineered from {ctx['material']}, this garment combines structured architectural drape with all-day comfort and breathability across varied climates."

        return {"answer": ans, "status": "success"}
