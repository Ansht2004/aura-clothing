from typing import List, Dict, Any, Optional
from models import Product, Order, OrderItem, db

class RecommendationEngine:
    """
    Recommendation Engine implementing the MCA Project Synopsis Product-Ranking Method.
    Weights:
      - Category Match: 0.40
      - Price Proximity Match: 0.25
      - Product Rating: 0.20
      - Product Popularity: 0.15
    """

    W_CATEGORY = 0.40
    W_PRICE = 0.25
    W_RATING = 0.20
    W_POPULARITY = 0.15

    def __init__(self, w_cat=0.40, w_price=0.25, w_rating=0.20, w_pop=0.15):
        self.w_cat = w_cat
        self.w_price = w_price
        self.w_rating = w_rating
        self.w_pop = w_pop

    def score_candidate(self, target: Product, candidate: Product, max_sales: float = 100.0) -> Dict[str, Any]:
        """Calculates component and composite score for a candidate product relative to target."""
        # 1. Category Match (0.40)
        if candidate.category_id == target.category_id:
            cat_score = 1.0
        else:
            cat_score = 0.0

        # 2. Price Proximity Match (0.25)
        target_effective_price = target.discount_price if (target.discount_price and target.discount_price > 0) else target.base_price
        cand_effective_price = candidate.discount_price if (candidate.discount_price and candidate.discount_price > 0) else candidate.base_price

        if target_effective_price > 0:
            diff_ratio = abs(cand_effective_price - target_effective_price) / target_effective_price
            price_score = max(0.0, 1.0 - min(1.0, diff_ratio))
        else:
            price_score = 1.0 if cand_effective_price == 0 else 0.0

        # 3. Product Rating (0.20)
        rating_val = candidate.average_rating or 0.0
        rating_score = min(1.0, max(0.0, rating_val / 5.0))

        # 4. Popularity (0.15)
        sales = candidate.sales_count or 0
        reviews = candidate.review_count or 0
        pop_metric = sales + (reviews * 0.5)
        pop_score = min(1.0, pop_metric / max_sales) if max_sales > 0 else 0.0

        # Weighted Total
        total_score = (
            (self.w_cat * cat_score) +
            (self.w_price * price_score) +
            (self.w_rating * rating_score) +
            (self.w_pop * pop_score)
        )

        return {
            'product': candidate.to_dict(),
            'score': round(total_score, 4),
            'breakdown': {
                'category_score': round(cat_score, 4),
                'price_score': round(price_score, 4),
                'rating_score': round(rating_score, 4),
                'popularity_score': round(pop_score, 4)
            }
        }

    def get_related_recommendations(self, target_product_id: int, limit: int = 8) -> List[Dict[str, Any]]:
        """Returns top ranked related products for a product detail page."""
        target = Product.query.get(target_product_id)
        if not target:
            return []

        candidates = Product.query.filter(
            Product.id != target_product_id,
            Product.is_active == True
        ).all()

        if not candidates:
            return []

        # Find maximum sales across candidates for proper normalization
        max_sales = max([c.sales_count + (c.review_count * 0.5) for c in candidates] or [10.0])
        max_sales = max(max_sales, 10.0)

        scored = [self.score_candidate(target, c, max_sales=max_sales) for c in candidates]
        scored.sort(key=lambda x: x['score'], reverse=True)

        return scored[:limit]

    def get_personalized_recommendations(self, user_id: int, limit: int = 8) -> List[Dict[str, Any]]:
        """
        Calculates personalized recommendations based on past user orders or popular top rated items.
        """
        # Get user's ordered product categories
        user_orders = Order.query.filter_by(user_id=user_id).all()
        order_ids = [o.id for o in user_orders]

        ordered_items = OrderItem.query.filter(OrderItem.order_id.in_(order_ids)).all() if order_ids else []
        ordered_product_ids = {item.product_id for item in ordered_items if item.product_id}

        if ordered_product_ids:
            # User has purchase history: pick the most recent product as anchor
            anchor_product = Product.query.get(list(ordered_product_ids)[-1])
            if anchor_product:
                # Rank candidates excluding already purchased products
                candidates = Product.query.filter(
                    Product.id.notin_(ordered_product_ids),
                    Product.is_active == True
                ).all()

                if candidates:
                    max_sales = max([c.sales_count + (c.review_count * 0.5) for c in candidates] or [10.0])
                    scored = [self.score_candidate(anchor_product, c, max_sales=max_sales) for c in candidates]
                    scored.sort(key=lambda x: x['score'], reverse=True)
                    return scored[:limit]

        # Cold start fallback: top rated and popular products
        popular = Product.query.filter_by(is_active=True).order_by(
            Product.average_rating.desc(), 
            Product.sales_count.desc()
        ).limit(limit).all()

        return [{'product': p.to_dict(), 'score': round((p.average_rating / 5.0) * 0.6 + 0.4, 4), 'breakdown': {}} for p in popular]

recommendation_engine = RecommendationEngine()
