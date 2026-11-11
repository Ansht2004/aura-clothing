from flask import Blueprint, request, jsonify
from models import Coupon

coupons_bp = Blueprint('coupons', __name__, url_prefix='/api/coupons')

@coupons_bp.route('/validate', methods=['POST'])
def validate_coupon():
    data = request.get_json() or {}
    code = data.get('code', '').strip().upper()
    subtotal = float(data.get('subtotal', 0.0))

    if not code:
        return jsonify({'valid': False, 'message': 'Coupon code is required'}), 400

    coupon = Coupon.query.filter_by(code=code).first()
    if not coupon:
        return jsonify({
            'valid': False, 
            'message': f"Coupon code '{code}' is not recognized."
        }), 404

    is_valid, reason = coupon.is_valid(subtotal=subtotal)
    if not is_valid:
        return jsonify({
            'valid': False,
            'message': reason,
            'code': coupon.code
        }), 400

    discount_amount = coupon.calculate_discount(subtotal=subtotal)

    return jsonify({
        'valid': True,
        'message': f"Coupon '{coupon.code}' applied! You saved ₹{discount_amount:,.2f}.",
        'coupon': {
            'code': coupon.code,
            'discount_type': coupon.discount_type,
            'discount_value': coupon.discount_value,
            'discount_amount': discount_amount,
            'new_subtotal': max(0.0, round(subtotal - discount_amount, 2))
        }
    }), 200

@coupons_bp.route('/active', methods=['GET'])
def get_active_coupons():
    coupons = Coupon.query.filter_by(is_active=True).all()
    # Filter only unexpired
    valid_coupons = []
    for c in coupons:
        is_val, _ = c.is_valid(subtotal=999999)
        if is_val:
            valid_coupons.append(c.to_dict())
    return jsonify({'coupons': valid_coupons}), 200
