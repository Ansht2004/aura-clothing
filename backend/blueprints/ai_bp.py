from flask import Blueprint, request, jsonify
from services.ai_service import AuraAIService

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@ai_bp.route('/concierge', methods=['POST'])
def concierge_chat():
    """
    Haute Couture AI Concierge Privé endpoint.
    Processes conversational styling queries with optional multimodal image.
    """
    try:
        data = request.get_json() or {}
        messages = data.get('messages', [])
        image_data = data.get('image', None)
        
        if not messages and not image_data:
            return jsonify({
                "status": "error",
                "message": "Message content or style inspiration image is required."
            }), 400

        result = AuraAIService.chat_with_concierge(messages, image_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Atelier Concierge encountered an error: {str(e)}"
        }), 500

@ai_bp.route('/editorial-copy', methods=['POST'])
def generate_editorial_copy():
    """
    Admin AI Copilot: Generates luxury poetic description & styling prose for a garment.
    """
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        material = data.get('material', '').strip()
        category_name = data.get('category_name', 'Atelier Collection').strip()

        if not name:
            return jsonify({"status": "error", "message": "Product name is required."}), 400

        result = AuraAIService.generate_editorial_copy(name, material, category_name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Editorial copywriter failed: {str(e)}"
        }), 500

@ai_bp.route('/fabric-advisor', methods=['POST'])
def fabric_advisor():
    """
    PDP Tactile Physics Advisor: Inquires on drape, wrinkle resistance, and fabric feel.
    """
    try:
        data = request.get_json() or {}
        product_id = data.get('product_id')
        question = data.get('question', '').strip()

        if not product_id or not question:
            return jsonify({
                "status": "error",
                "message": "product_id and inquiry question are required."
            }), 400

        result = AuraAIService.ask_fabric_advisor(int(product_id), question)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Fabric advisor failed: {str(e)}"
        }), 500
