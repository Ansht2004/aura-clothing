from flask import Blueprint, request, jsonify
from sqlalchemy import or_, and_
from models import db, Product, ProductVariant, Category, Review
from services.recommendation_service import recommendation_engine

products_bp = Blueprint('products', __name__, url_prefix='/api')

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify({
        'categories': [c.to_dict() for c in categories]
    }), 200

@products_bp.route('/products', methods=['GET'])
def list_products():
    query = Product.query.filter(Product.is_active == True)

    # 1. Search keyword
    search = request.args.get('search', '').strip()
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern),
                Product.brand.ilike(search_pattern),
                Product.material.ilike(search_pattern)
            )
        )

    # 2. Category filter (slug or id)
    cat_param = request.args.get('category', '').strip()
    if cat_param:
        if cat_param.isdigit():
            query = query.filter(Product.category_id == int(cat_param))
        else:
            cat = Category.query.filter_by(slug=cat_param).first()
            if cat:
                query = query.filter(Product.category_id == cat.id)

    # 3. Price range
    min_price = request.args.get('min_price', type=float)
    if min_price is not None:
        query = query.filter(
            db.case(
                (Product.discount_price.isnot(None) & (Product.discount_price > 0), Product.discount_price),
                else_=Product.base_price
            ) >= min_price
        )

    max_price = request.args.get('max_price', type=float)
    if max_price is not None:
        query = query.filter(
            db.case(
                (Product.discount_price.isnot(None) & (Product.discount_price > 0), Product.discount_price),
                else_=Product.base_price
            ) <= max_price
        )

    # 4. Rating filter
    min_rating = request.args.get('min_rating', type=float)
    if min_rating is not None and min_rating > 0:
        query = query.filter(Product.average_rating >= min_rating)

    # 5. Featured filter
    featured = request.args.get('featured')
    if featured and featured.lower() in ['true', '1']:
        query = query.filter(Product.is_featured == True)

    # 6. Size filter (joins ProductVariant)
    size = request.args.get('size', '').strip()
    if size:
        query = query.join(ProductVariant).filter(
            ProductVariant.size == size,
            ProductVariant.stock_quantity > 0
        )

    # 7. Color filter
    color = request.args.get('color', '').strip()
    if color:
        # Check if already joined
        if not size:
            query = query.join(ProductVariant)
        query = query.filter(ProductVariant.color.ilike(color))

    # 8. In stock only
    in_stock_only = request.args.get('in_stock')
    if in_stock_only and in_stock_only.lower() in ['true', '1']:
        if not size and not color:
            query = query.join(ProductVariant)
        query = query.filter(ProductVariant.stock_quantity > 0)

    # Prevent duplicate product rows from join
    query = query.distinct()

    # 9. Sorting
    sort_by = request.args.get('sort', 'popular').lower()
    if sort_by == 'price_asc':
        query = query.order_by(
            db.case(
                (Product.discount_price.isnot(None) & (Product.discount_price > 0), Product.discount_price),
                else_=Product.base_price
            ).asc()
        )
    elif sort_by == 'price_desc':
        query = query.order_by(
            db.case(
                (Product.discount_price.isnot(None) & (Product.discount_price > 0), Product.discount_price),
                else_=Product.base_price
            ).desc()
        )
    elif sort_by == 'rating':
        query = query.order_by(Product.average_rating.desc(), Product.review_count.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:  # 'popular' default
        query = query.order_by(Product.sales_count.desc(), Product.average_rating.desc())

    # 10. Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    per_page = min(max(per_page, 1), 100)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'products': [p.to_dict(include_details=False) for p in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_items': pagination.total,
            'total_pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product or not product.is_active:
        return jsonify({'error': 'Product not found'}), 404

    # Calculate ratings distribution
    reviews = Review.query.filter_by(product_id=id).all()
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in reviews:
        if 1 <= r.rating <= 5:
            rating_counts[r.rating] += 1

    product_dict = product.to_dict(include_details=True)
    product_dict['rating_breakdown'] = rating_counts
    product_dict['recent_reviews'] = [r.to_dict() for r in reviews[:10]]

    return jsonify({'product': product_dict}), 200

@products_bp.route('/products/<int:id>/recommendations', methods=['GET'])
def get_recommendations(id):
    limit = request.args.get('limit', 8, type=int)
    recommendations = recommendation_engine.get_related_recommendations(id, limit=limit)
    return jsonify({
        'product_id': id,
        'algorithm': 'MCA-weighted-ranking',
        'weights': {
            'category_match': 0.40,
            'price_match': 0.25,
            'rating': 0.20,
            'popularity': 0.15
        },
        'recommendations': recommendations
    }), 200
