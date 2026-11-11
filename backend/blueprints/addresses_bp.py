from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Address

addresses_bp = Blueprint('addresses', __name__, url_prefix='/api/addresses')

@addresses_bp.route('', methods=['GET'])
@jwt_required()
def get_addresses():
    user_id = int(get_jwt_identity())
    addresses = Address.query.filter_by(user_id=user_id).order_by(Address.is_default.desc(), Address.created_at.desc()).all()
    return jsonify({'addresses': [a.to_dict() for a in addresses]}), 200

@addresses_bp.route('', methods=['POST'])
@jwt_required()
def add_address():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    full_name = data.get('full_name', '').strip()
    phone = data.get('phone', '').strip()
    address_line1 = data.get('address_line1', '').strip()
    address_line2 = data.get('address_line2', '').strip()
    city = data.get('city', '').strip()
    state = data.get('state', '').strip()
    postal_code = data.get('postal_code', '').strip()
    country = data.get('country', 'United States').strip()
    is_default = bool(data.get('is_default', False))

    if not all([full_name, phone, address_line1, city, state, postal_code]):
        return jsonify({'error': 'Please fill in all required address fields.'}), 400

    # If first address or marked default, reset other addresses
    existing_count = Address.query.filter_by(user_id=user_id).count()
    if existing_count == 0 or is_default:
        Address.query.filter_by(user_id=user_id).update({'is_default': False})
        is_default = True

    address = Address(
        user_id=user_id,
        full_name=full_name,
        phone=phone,
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        state=state,
        postal_code=postal_code,
        country=country,
        is_default=is_default
    )
    db.session.add(address)
    db.session.commit()

    return jsonify({'message': 'Address added successfully', 'address': address.to_dict()}), 201

@addresses_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_address(id):
    user_id = int(get_jwt_identity())
    address = Address.query.filter_by(id=id, user_id=user_id).first()
    if not address:
        return jsonify({'error': 'Address not found'}), 404

    data = request.get_json() or {}
    for field in ['full_name', 'phone', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country']:
        if field in data:
            setattr(address, field, data[field].strip() if isinstance(data[field], str) else data[field])

    if 'is_default' in data and data['is_default']:
        Address.query.filter_by(user_id=user_id).update({'is_default': False})
        address.is_default = True

    db.session.commit()
    return jsonify({'message': 'Address updated successfully', 'address': address.to_dict()}), 200

@addresses_bp.route('/<int:id>/set-default', methods=['PUT'])
@jwt_required()
def set_default_address(id):
    user_id = int(get_jwt_identity())
    address = Address.query.filter_by(id=id, user_id=user_id).first()
    if not address:
        return jsonify({'error': 'Address not found'}), 404

    Address.query.filter_by(user_id=user_id).update({'is_default': False})
    address.is_default = True
    db.session.commit()
    return jsonify({'message': 'Default address updated', 'address': address.to_dict()}), 200

@addresses_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    user_id = int(get_jwt_identity())
    address = Address.query.filter_by(id=id, user_id=user_id).first()
    if not address:
        return jsonify({'error': 'Address not found'}), 404

    was_default = address.is_default
    db.session.delete(address)
    db.session.commit()

    # If default was deleted, assign default to another address if any exist
    if was_default:
        next_addr = Address.query.filter_by(user_id=user_id).first()
        if next_addr:
            next_addr.is_default = True
            db.session.commit()

    return jsonify({'message': 'Address deleted successfully'}), 200
