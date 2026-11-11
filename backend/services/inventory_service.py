from typing import List, Tuple, Dict, Any
from models import db, ProductVariant, Product

class InventoryService:
    @staticmethod
    def check_availability(items: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        Validates whether requested quantities are available in stock.
        items: [{'variant_id': int, 'quantity': int}, ...]
        Returns (is_available, error_messages)
        """
        errors = []
        for item in items:
            v_id = item.get('variant_id')
            qty = item.get('quantity', 1)
            variant = ProductVariant.query.get(v_id)
            if not variant:
                errors.append(f"Product variant ID {v_id} does not exist.")
                continue

            product = variant.product
            product_name = product.name if product else "Item"
            variant_desc = f"{product_name} ({variant.color}, {variant.size})"

            if variant.stock_quantity < qty:
                errors.append(f"Insufficient stock for {variant_desc}. Available: {variant.stock_quantity}, requested: {qty}.")

        return (len(errors) == 0), errors

    @staticmethod
    def reserve_and_deduct(items: List[Dict[str, Any]]) -> bool:
        """
        Deducts stock and increments sales_count on products.
        Must be called within a database session transaction.
        """
        for item in items:
            variant = ProductVariant.query.filter_by(id=item['variant_id']).with_for_update().first()
            if not variant or variant.stock_quantity < item['quantity']:
                raise ValueError(f"Insufficient stock for variant ID {item.get('variant_id')}")
            
            variant.stock_quantity -= item['quantity']
            if variant.product:
                variant.product.sales_count += item['quantity']
        
        return True

    @staticmethod
    def restore_stock(items: List[Dict[str, Any]]) -> bool:
        """
        Restores stock when an order is cancelled or returned.
        items: [{'variant_id': int, 'quantity': int}, ...]
        """
        for item in items:
            if not item.get('variant_id'):
                continue
            variant = ProductVariant.query.get(item['variant_id'])
            if variant:
                variant.stock_quantity += item['quantity']
                if variant.product and variant.product.sales_count >= item['quantity']:
                    variant.product.sales_count -= item['quantity']
        return True

    @staticmethod
    def get_low_stock_variants(threshold: int = 5) -> List[Dict[str, Any]]:
        """Finds all variants whose stock quantity is at or below threshold."""
        variants = ProductVariant.query.filter(
            ProductVariant.stock_quantity <= threshold
        ).join(Product).all()

        results = []
        for v in variants:
            results.append({
                'variant_id': v.id,
                'product_id': v.product_id,
                'product_name': v.product.name if v.product else 'Unknown',
                'sku': v.sku,
                'size': v.size,
                'color': v.color,
                'stock_quantity': v.stock_quantity,
                'threshold': threshold
            })
        return results

inventory_service = InventoryService()
