import os
import random
from datetime import datetime, timezone
from app import create_app
from models import (
    db, User, Address, Category, Product, ProductVariant,
    ProductImage, Coupon, Order, OrderItem, Payment, Review
)

CATEGORIES_DATA = [
    {
        "name": "Evening Gowns & Gala Dresses",
        "slug": "evening-gowns",
        "description": "Couture gala evening gowns, architectural silhouettes, and red-carpet floor-sweeping dresses handcrafted from Italian duchess satin and French Chantilly lace.",
        "image_url": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Cocktail & Silk Day Dresses",
        "slug": "cocktail-day-dresses",
        "description": "Bias-cut mulberry silk midi slips, structured crepe cocktail dresses, and day-to-evening dresses with refined drape and bespoke tailoring.",
        "image_url": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Formal & Dress Shirts",
        "slug": "formal-dress-shirts",
        "description": "Single-needle stitched 120s two-ply Giza Egyptian cotton dress shirts, mother-of-pearl buttons, and bespoke spread and point collars.",
        "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Luxury Polos & Resort Shirts",
        "slug": "luxury-polos-shirts",
        "description": "Fine-gauge silk-cotton knit polos, open-weave Sea Island cotton pique, and relaxed camp-collar vacation shirts.",
        "image_url": "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Tailored Blazers & Sport Coats",
        "slug": "tailored-blazers",
        "description": "Unstructured Italian wool-silk-linen blazers, canvassed double-breasted sport coats, and bespoke horn button jackets.",
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Luxury Overcoats & Trench Coats",
        "slug": "overcoats-trench",
        "description": "Double-faced cashmere topcoats, heavy Melton wool overcoats, and storm-proof gabardine belted trench coats.",
        "image_url": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Fine Knitwear",
        "slug": "fine-knitwear",
        "description": "Ultra-fine 18-gauge Australian merino wool crewnecks, mock necks, and featherweight silk-cashmere knitwear for seamless layering.",
        "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Luxury Sweaters & Cardigans",
        "slug": "sweaters-cardigans",
        "description": "Chunky Mongolian cashmere turtlenecks, ribbed fisherman sweaters, and hand-loomed shawl collar cardigans.",
        "image_url": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Tailored Dress Trousers",
        "slug": "tailored-trousers",
        "description": "High-rise pleated wool flannel trousers, side-adjuster dress slacks, and refined formal trousers woven in Biella, Italy.",
        "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Refined Chinos & Casual Pants",
        "slug": "chinos-casual-pants",
        "description": "Garment-dyed stretch Supima cotton chinos, relaxed pleated fatigue trousers, and versatile tailored casual pants.",
        "image_url": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Japanese Selvedge Denim",
        "slug": "selvedge-denim",
        "description": "Shuttle-loom woven raw Japanese selvedge denim from Kojima, Okayama. Custom copper hardware, rope-dyed indigo, and chainstitched hems.",
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Contemporary Jeans & Denim Wear",
        "slug": "designer-jeans",
        "description": "Artisanal washed slim-tapered jeans, relaxed luxury denim jackets, and distressed vintage-inspired modern denim.",
        "image_url": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Cashmere & Cotton Loungewear",
        "slug": "cashmere-loungewear",
        "description": "Plush pure cashmere hoodies, heavyweight 450GSM French terry sweatpants, and elevated minimalist relaxed loungewear.",
        "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Silk Sleepwear & Robes",
        "slug": "silk-sleepwear-robes",
        "description": "100% 22-Momme mulberry silk pajama sets, belted satin kimono robes, and temperature-regulating silk nightwear.",
        "image_url": "https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Haute Activewear & Training",
        "slug": "haute-activewear",
        "description": "Four-way stretch technical compression leggings, sculpt bras, and sweat-wicking aerodynamic tops for luxury performance.",
        "image_url": "https://images.unsplash.com/photo-1607914660217-754fdd90041d?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Technical & Weather Performance",
        "slug": "technical-performance",
        "description": "Three-layer GORE-TEX waterproof shells, windproof technical hybrid jackets, and laser-cut bonded seam outerwear.",
        "image_url": "https://images.unsplash.com/photo-1516257984-b1b4d707412e?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Leather & Suede Jackets",
        "slug": "leather-suede-jackets",
        "description": "Buttery Italian lambskin biker jackets, calf suede cafe racer jackets, and shearling-lined aviator flight jackets.",
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Parkas, Puffers & Rainwear",
        "slug": "parkas-puffers",
        "description": "800-fill power goose down expedition parkas, diamond-quilted puffers, and taped-seam technical rainproof mac coats.",
        "image_url": "https://images.unsplash.com/photo-1547406683-690698712a08?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Pure Linen Shirts & Tops",
        "slug": "linen-shirts",
        "description": "Breathable Normandy flax pure linen button-downs, popover vacation tunics, and relaxed collarless linen resort shirts.",
        "image_url": "https://images.unsplash.com/photo-1578932750294-f5075e85f44a?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Linen Trousers & Resortwear",
        "slug": "linen-resortwear",
        "description": "Wide-leg drawstring linen trousers, tailored linen-cotton resort shorts, and breezy coastal travel apparel.",
        "image_url": "https://images.pexels.com/photos/19090/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=800",
        "is_featured": 1
    },
    {
        "name": "Artisanal Leather Boots",
        "slug": "leather-boots",
        "description": "Goodyear-welted Tuscan leather Chelsea boots, hand-burnished combat boots, and waxed roughout suede desert boots.",
        "image_url": "https://images.unsplash.com/photo-1628193104037-3590917fb66e?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Luxury Dress Shoes & Loafers",
        "slug": "dress-shoes-loafers",
        "description": "Blake-stitched Italian penny loafers, hand-patinated calfskin oxfords, and equestrian-inspired horsebit slip-ons.",
        "image_url": "https://images.unsplash.com/photo-1490114538077-0a7f8cb49891?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Leather Bags & Luggage",
        "slug": "leather-bags-luggage",
        "description": "Full-grain vegetable-tanned leather weekender duffels, structured briefcases, luxury totes, and modular travel bags.",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    },
    {
        "name": "Fine Accessories & Silk Goods",
        "slug": "accessories-fine-goods",
        "description": "Hand-rolled Como silk scarves, Italian calfskin belts with solid brass buckles, cashmere beanies, and fine leather goods.",
        "image_url": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?auto=format&fit=crop&w=1000&q=80",
        "is_featured": 1
    }
]

PRODUCTS_DATA = [
    {
        "name": "Duchess Silk Faille Gala Gown",
        "slug": "duchess-silk-faille-gala-gown-1",
        "description": "Architectural strapless gala evening gown cut from heavy Italian silk faille with an internal corset and dramatic sweep train.",
        "category_slug": "evening-gowns",
        "base_price": 24999.0,
        "discount_price": 21999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 13,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-EVE-001-MID-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-EVE-001-MID-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-EVE-001-MID-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-EVE-001-MID-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-EVE-001-MID-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-EVE-001-CHA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-EVE-001-CHA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-EVE-001-CHA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-EVE-001-CHA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-EVE-001-CHA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Mulberry Silk Bias-Cut Column Slip",
        "slug": "mulberry-silk-bias-cut-column-slip-2",
        "description": "Sensuous floor-length column dress crafted from 30-momme heavy mulberry silk with delicate cowl back detailing.",
        "category_slug": "evening-gowns",
        "base_price": 18999.0,
        "discount_price": 15999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 19,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-EVE-002-FOR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-EVE-002-FOR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-EVE-002-FOR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-EVE-002-FOR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-EVE-002-FOR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-EVE-002-SLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-EVE-002-SLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-EVE-002-SLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-EVE-002-SLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-EVE-002-SLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "French Chantilly Lace Embroidered Gown",
        "slug": "french-chantilly-lace-embroidered-gown-3",
        "description": "Intricately hand-embroidered black-tie gown layered with sheer Chantilly lace over silk georgette lining.",
        "category_slug": "evening-gowns",
        "base_price": 28999.0,
        "discount_price": 24999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 25,
        "sales_count": 33,
        "primary_image": "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-EVE-003-OBS-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-EVE-003-OBS-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-EVE-003-OBS-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-EVE-003-OBS-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-EVE-003-OBS-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-EVE-003-IVO-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-EVE-003-IVO-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-EVE-003-IVO-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-EVE-003-IVO-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-EVE-003-IVO-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Emerald Velvet Asymmetric Evening Dress",
        "slug": "emerald-velvet-asymmetric-evening-dress-4",
        "description": "Plush Italian cotton velvet gown featuring a dramatic one-shoulder neckline and side-slit contour silhouette.",
        "category_slug": "evening-gowns",
        "base_price": 22999.0,
        "discount_price": 19999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 31,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1568252542512-9fe8fe9c87bb?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-EVE-004-CAM-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-EVE-004-CAM-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-EVE-004-CAM-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-EVE-004-CAM-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-EVE-004-CAM-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-EVE-004-ESP-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-EVE-004-ESP-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-EVE-004-ESP-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-EVE-004-ESP-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-EVE-004-ESP-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Liquid Metallic Lam\u00e9 Gala Gown",
        "slug": "liquid-metallic-lam-gala-gown-5",
        "description": "Reflective gold liquid-lam\u00e9 floor-sweeping gown with plunging halter neckline and pleated godet train.",
        "category_slug": "evening-gowns",
        "base_price": 26999.0,
        "discount_price": 22999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 37,
        "sales_count": 35,
        "primary_image": "https://images.unsplash.com/photo-1502716119720-b23a93e5fe1b?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-EVE-005-BUR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-EVE-005-BUR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-EVE-005-BUR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-EVE-005-BUR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-EVE-005-BUR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-EVE-005-CLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-EVE-005-CLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-EVE-005-CLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-EVE-005-CLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-EVE-005-CLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Pliss\u00e9 Chiffon Empire Gala Dress",
        "slug": "pliss-chiffon-empire-gala-dress-6",
        "description": "Airy micro-pleated silk chiffon gown with an empire waistline and fluttering cape sleeves for black-tie galas.",
        "category_slug": "evening-gowns",
        "base_price": 19999.0,
        "discount_price": 16999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 43,
        "sales_count": 36,
        "primary_image": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-EVE-006-MID-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-EVE-006-MID-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-EVE-006-MID-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-EVE-006-MID-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-EVE-006-MID-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-EVE-006-CHA-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-EVE-006-CHA-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-EVE-006-CHA-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-EVE-006-CHA-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-EVE-006-CHA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Off-Shoulder Crepe Column Gown",
        "slug": "off-shoulder-crepe-column-gown-7",
        "description": "Architectural crepe gown with structured fold-over off-shoulder sleeves and a sleek mermaid hem.",
        "category_slug": "evening-gowns",
        "base_price": 17999.0,
        "discount_price": 14999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 42,
        "sales_count": 37,
        "primary_image": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-EVE-007-FOR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-EVE-007-FOR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-EVE-007-FOR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-EVE-007-FOR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-EVE-007-FOR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-EVE-007-SLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-EVE-007-SLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-EVE-007-SLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-EVE-007-SLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-EVE-007-SLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Crystal-Embellished Open-Back Gown",
        "slug": "crystal-embellished-open-back-gown-8",
        "description": "Sleek obsidian black crepe gown highlighted by hand-applied Swarovski crystal piping along the spine.",
        "category_slug": "evening-gowns",
        "base_price": 27999.0,
        "discount_price": 23999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 48,
        "sales_count": 38,
        "primary_image": "https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-EVE-008-OBS-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-EVE-008-OBS-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-EVE-008-OBS-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-EVE-008-OBS-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-EVE-008-OBS-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-EVE-008-IVO-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-EVE-008-IVO-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-EVE-008-IVO-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-EVE-008-IVO-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-EVE-008-IVO-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Draped Silk Satin Mermaid Dress",
        "slug": "draped-silk-satin-mermaid-dress-9",
        "description": "Sculptural evening gown cut on the bias in champagne silk satin with an hourglass corset foundation.",
        "category_slug": "evening-gowns",
        "base_price": 21999.0,
        "discount_price": 18999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 54,
        "sales_count": 39,
        "primary_image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-EVE-009-CAM-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-EVE-009-CAM-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-EVE-009-CAM-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-EVE-009-CAM-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-EVE-009-CAM-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-EVE-009-ESP-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-EVE-009-ESP-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-EVE-009-ESP-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-EVE-009-ESP-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-EVE-009-ESP-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Corseted Tulle Ballgown in Midnight Navy",
        "slug": "corseted-tulle-ballgown-in-midnight-navy-10",
        "description": "Multi-layered French illusion tulle gown supported by a hand-boned velvet corset for gala events.",
        "category_slug": "evening-gowns",
        "base_price": 29999.0,
        "discount_price": 25999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 60,
        "sales_count": 40,
        "primary_image": "https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-EVE-010-BUR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-EVE-010-BUR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-EVE-010-BUR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-EVE-010-BUR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-EVE-010-BUR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-EVE-010-CLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-EVE-010-CLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-EVE-010-CLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-EVE-010-CLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-EVE-010-CLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Mulberry Silk Bias-Cut Midi Slip Dress",
        "slug": "mulberry-silk-bias-cut-midi-slip-dress-11",
        "description": "Iconic 90s-inspired midi slip dress in washed silk crepe with adjustable silk rouleau straps.",
        "category_slug": "cocktail-day-dresses",
        "base_price": 12999.0,
        "discount_price": 10999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 16,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-COC-011-MID-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-COC-011-MID-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-COC-011-MID-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-COC-011-MID-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-COC-011-MID-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-COC-011-CHA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-COC-011-CHA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-COC-011-CHA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-COC-011-CHA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-COC-011-CHA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Double-Breasted Crepe Tuxedo Mini Dress",
        "slug": "double-breasted-crepe-tuxedo-mini-dress-12",
        "description": "Sharp tailored cocktail mini dress featuring peak satin lapels and double-breasted horn buttons.",
        "category_slug": "cocktail-day-dresses",
        "base_price": 14999.0,
        "discount_price": 12499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 22,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-COC-012-FOR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-COC-012-FOR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-COC-012-FOR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-COC-012-FOR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-COC-012-FOR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-COC-012-SLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-COC-012-SLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-COC-012-SLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-COC-012-SLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-COC-012-SLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Botanical Print Silk Georgette Day Dress",
        "slug": "botanical-print-silk-georgette-day-dress-13",
        "description": "Romantic tiered day dress cut from sheer Italian silk georgette with smocked cuffs and waist tie.",
        "category_slug": "cocktail-day-dresses",
        "base_price": 13999.0,
        "discount_price": 11499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 28,
        "sales_count": 43,
        "primary_image": "https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-COC-013-OBS-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-COC-013-OBS-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-COC-013-OBS-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-COC-013-OBS-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-COC-013-OBS-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-COC-013-IVO-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-COC-013-IVO-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-COC-013-IVO-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-COC-013-IVO-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-COC-013-IVO-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Pleated Silk Crepe de Chine Shirt Dress",
        "slug": "pleated-silk-crepe-de-chine-shirt-dress-14",
        "description": "Tailored shirt dress with sharp knife pleats through the skirt and a self-fabric buckle belt.",
        "category_slug": "cocktail-day-dresses",
        "base_price": 15999.0,
        "discount_price": 13499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 27,
        "sales_count": 44,
        "primary_image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-COC-014-CAM-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-COC-014-CAM-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-COC-014-CAM-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-COC-014-CAM-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-COC-014-CAM-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-COC-014-ESP-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-COC-014-ESP-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-COC-014-ESP-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-COC-014-ESP-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-COC-014-ESP-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Asymmetric Ribbed Knit Midi Cocktail Dress",
        "slug": "asymmetric-ribbed-knit-midi-cocktail-dress-15",
        "description": "Body-contouring viscose-silk knit dress featuring an asymmetric neckline and ribbed column drape.",
        "category_slug": "cocktail-day-dresses",
        "base_price": 11999.0,
        "discount_price": 9999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 33,
        "sales_count": 45,
        "primary_image": "https://images.unsplash.com/photo-1485230895905-ec40ba36b9bc?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-COC-015-BUR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-COC-015-BUR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-COC-015-BUR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-COC-015-BUR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-COC-015-BUR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-COC-015-CLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-COC-015-CLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-COC-015-CLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-COC-015-CLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-COC-015-CLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Belted Safari Linen-Silk Day Dress",
        "slug": "belted-safari-linen-silk-day-dress-16",
        "description": "Structured safari-inspired day dress with horn buttons, utility flap pockets, and wide buckle belt.",
        "category_slug": "cocktail-day-dresses",
        "base_price": 12499.0,
        "discount_price": 10499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 39,
        "sales_count": 46,
        "primary_image": "https://images.unsplash.com/photo-1485968579580-b6d095142e6e?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-COC-016-MID-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-COC-016-MID-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-COC-016-MID-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-COC-016-MID-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-COC-016-MID-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-COC-016-CHA-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-COC-016-CHA-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-COC-016-CHA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-COC-016-CHA-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-COC-016-CHA-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Scalloped Guipure Lace Cocktail Dress",
        "slug": "scalloped-guipure-lace-cocktail-dress-17",
        "description": "Feminine A-line cocktail dress constructed from heavyweight geometric guipure lace over tonal silk.",
        "category_slug": "cocktail-day-dresses",
        "base_price": 16999.0,
        "discount_price": 13999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 45,
        "sales_count": 47,
        "primary_image": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-COC-017-FOR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-COC-017-FOR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-COC-017-FOR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-COC-017-FOR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-COC-017-FOR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-COC-017-SLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-COC-017-SLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-COC-017-SLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-COC-017-SLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-COC-017-SLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Ruched Stretch-Silk Halter Dress",
        "slug": "ruched-stretch-silk-halter-dress-18",
        "description": "Sculpting cocktail dress with delicate center ruching and a crossover halter neckline in ruby red.",
        "category_slug": "cocktail-day-dresses",
        "base_price": 14499.0,
        "discount_price": 11999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 51,
        "sales_count": 48,
        "primary_image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-COC-018-OBS-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-COC-018-OBS-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-COC-018-OBS-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-COC-018-OBS-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-COC-018-OBS-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-COC-018-IVO-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-COC-018-IVO-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-COC-018-IVO-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-COC-018-IVO-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-COC-018-IVO-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Draped One-Shoulder Silk Midi Dress",
        "slug": "draped-one-shoulder-silk-midi-dress-19",
        "description": "Graceful one-shoulder midi dress in iridescent sage silk charmeuse with fluid waterfall drape.",
        "category_slug": "cocktail-day-dresses",
        "base_price": 15499.0,
        "discount_price": 12999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 57,
        "sales_count": 49,
        "primary_image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-COC-019-CAM-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-COC-019-CAM-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-COC-019-CAM-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-COC-019-CAM-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-COC-019-CAM-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-COC-019-ESP-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-COC-019-ESP-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-COC-019-ESP-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-COC-019-ESP-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-COC-019-ESP-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Jacquard Brocade Flare Cocktail Dress",
        "slug": "jacquard-brocade-flare-cocktail-dress-20",
        "description": "Opulent metallic floral jacquard dress tailored with a fitted bodice and box-pleated skirt.",
        "category_slug": "cocktail-day-dresses",
        "base_price": 17499.0,
        "discount_price": 14499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 63,
        "sales_count": 30,
        "primary_image": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-COC-020-BUR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-COC-020-BUR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-COC-020-BUR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-COC-020-BUR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-COC-020-BUR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-COC-020-CLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-COC-020-CLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-COC-020-CLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-COC-020-CLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-COC-020-CLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Signature 120s Egyptian Cotton Dress Shirt",
        "slug": "signature-120s-egyptian-cotton-dress-shirt-21",
        "description": "Crisp luxury poplin dress shirt woven from 120s two-ply Giza cotton with hand-set mother-of-pearl buttons.",
        "category_slug": "formal-dress-shirts",
        "base_price": 6999.0,
        "discount_price": 5799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 12,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FOR-021-MID-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FOR-021-MID-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FOR-021-MID-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FOR-021-MID-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FOR-021-MID-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FOR-021-CHA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FOR-021-CHA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FOR-021-CHA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FOR-021-CHA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FOR-021-CHA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Bespoke Spread-Collar French Cuff Shirt",
        "slug": "bespoke-spread-collar-french-cuff-shirt-22",
        "description": "Formal tuxedo-ready dress shirt tailored in twill cotton with double French cuffs for cufflinks.",
        "category_slug": "formal-dress-shirts",
        "base_price": 7499.0,
        "discount_price": 6299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 18,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FOR-022-FOR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FOR-022-FOR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FOR-022-FOR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FOR-022-FOR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FOR-022-FOR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FOR-022-SLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FOR-022-SLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FOR-022-SLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FOR-022-SLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FOR-022-SLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Tailored Pinpoint Oxford Button-Down",
        "slug": "tailored-pinpoint-oxford-button-down-23",
        "description": "Refined pinpoint Oxford woven from Supima cotton, featuring a soft rolling collar and athletic taper.",
        "category_slug": "formal-dress-shirts",
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 24,
        "sales_count": 33,
        "primary_image": "https://images.unsplash.com/photo-1603252109303-2751441dd157?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FOR-023-OBS-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FOR-023-OBS-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FOR-023-OBS-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FOR-023-OBS-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FOR-023-OBS-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FOR-023-IVO-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FOR-023-IVO-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FOR-023-IVO-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FOR-023-IVO-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FOR-023-IVO-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Fine Herringbone Royal Oxford Shirt",
        "slug": "fine-herringbone-royal-oxford-shirt-24",
        "description": "Subtle texture dress shirt in Egyptian cotton royal Oxford weave with removable brass collar stays.",
        "category_slug": "formal-dress-shirts",
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 30,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1589310243389-96a5483213a8?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FOR-024-CAM-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FOR-024-CAM-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FOR-024-CAM-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FOR-024-CAM-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FOR-024-CAM-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FOR-024-ESP-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FOR-024-ESP-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FOR-024-ESP-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FOR-024-ESP-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FOR-024-ESP-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Micro-Houndstooth Cotton Dress Shirt",
        "slug": "micro-houndstooth-cotton-dress-shirt-25",
        "description": "Sophisticated micro-houndstooth business shirt with semi-spread collar and curved barrel cuffs.",
        "category_slug": "formal-dress-shirts",
        "base_price": 6799.0,
        "discount_price": 5699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 36,
        "sales_count": 35,
        "primary_image": "https://images.pexels.com/photos/10484491/pexels-photo-10484491.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FOR-025-BUR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FOR-025-BUR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FOR-025-BUR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FOR-025-BUR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FOR-025-BUR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FOR-025-CLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FOR-025-CLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FOR-025-CLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FOR-025-CLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FOR-025-CLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Pleated Bib Piqu\u00e9 Marcella Tuxedo Shirt",
        "slug": "pleated-bib-piqu-marcella-tuxedo-shirt-26",
        "description": "Traditional black-tie formal shirt featuring a Marcella piqu\u00e9 bib front and stud buttonholes.",
        "category_slug": "formal-dress-shirts",
        "base_price": 8999.0,
        "discount_price": 7499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 42,
        "sales_count": 36,
        "primary_image": "https://images.unsplash.com/photo-1607345366928-199ea26cfe3e?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FOR-026-MID-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FOR-026-MID-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FOR-026-MID-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FOR-026-MID-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FOR-026-MID-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FOR-026-CHA-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FOR-026-CHA-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FOR-026-CHA-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FOR-026-CHA-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FOR-026-CHA-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Tab-Collar Dobby Stripe Formal Shirt",
        "slug": "tab-collar-dobby-stripe-formal-shirt-27",
        "description": "Classic English tab-collar shirt that elevates neckties, woven in a subtle self-stripe cotton dobby.",
        "category_slug": "formal-dress-shirts",
        "base_price": 6999.0,
        "discount_price": 5899.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 48,
        "sales_count": 37,
        "primary_image": "https://images.unsplash.com/photo-1621072156002-e2fccdc0b176?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FOR-027-FOR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FOR-027-FOR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FOR-027-FOR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FOR-027-FOR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FOR-027-FOR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FOR-027-SLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FOR-027-SLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FOR-027-SLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FOR-027-SLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FOR-027-SLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Sea Island Cotton Spread Collar Shirt",
        "slug": "sea-island-cotton-spread-collar-shirt-28",
        "description": "Featherweight luxury shirt crafted from genuine West Indian Sea Island cotton for unmatched softness.",
        "category_slug": "formal-dress-shirts",
        "base_price": 9499.0,
        "discount_price": 7999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 47,
        "sales_count": 38,
        "primary_image": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FOR-028-OBS-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FOR-028-OBS-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FOR-028-OBS-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FOR-028-OBS-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FOR-028-OBS-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FOR-028-IVO-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FOR-028-IVO-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FOR-028-IVO-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FOR-028-IVO-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FOR-028-IVO-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cutaway Collar Italian Poplin Shirt",
        "slug": "cutaway-collar-italian-poplin-shirt-29",
        "description": "Contemporary wide cutaway collar tailored in Thomas Mason Italian poplin with hand-stitched armholes.",
        "category_slug": "formal-dress-shirts",
        "base_price": 7999.0,
        "discount_price": 6699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 53,
        "sales_count": 39,
        "primary_image": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FOR-029-CAM-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FOR-029-CAM-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FOR-029-CAM-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FOR-029-CAM-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FOR-029-CAM-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FOR-029-ESP-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FOR-029-ESP-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FOR-029-ESP-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FOR-029-ESP-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FOR-029-ESP-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Textured Chambray Formal Dress Shirt",
        "slug": "textured-chambray-formal-dress-shirt-30",
        "description": "Fine-count indigo chambray formal shirt combining sartorial tailoring with modern depth.",
        "category_slug": "formal-dress-shirts",
        "base_price": 6299.0,
        "discount_price": 5299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 59,
        "sales_count": 40,
        "primary_image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FOR-030-BUR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FOR-030-BUR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FOR-030-BUR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FOR-030-BUR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FOR-030-BUR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FOR-030-CLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FOR-030-CLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FOR-030-CLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FOR-030-CLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FOR-030-CLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Signature Fine-Gauge Silk-Cotton Knit Polo",
        "slug": "signature-fine-gauge-silk-cotton-knit-polo-31",
        "description": "Luxurious knit polo blending mulberry silk and long-staple cotton with a ribbed collar and seamless placket.",
        "category_slug": "luxury-polos-shirts",
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 15,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LUX-031-MID-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LUX-031-MID-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LUX-031-MID-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LUX-031-MID-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LUX-031-MID-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LUX-031-CHA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LUX-031-CHA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LUX-031-CHA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LUX-031-CHA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LUX-031-CHA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Sea Island Cotton Piqu\u00e9 Polo Shirt",
        "slug": "sea-island-cotton-piqu-polo-shirt-32",
        "description": "Ultra-breathable pique polo shirt crafted from rare Sea Island cotton with genuine mother-of-pearl buttons.",
        "category_slug": "luxury-polos-shirts",
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 21,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LUX-032-FOR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LUX-032-FOR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LUX-032-FOR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LUX-032-FOR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LUX-032-FOR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LUX-032-SLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LUX-032-SLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LUX-032-SLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LUX-032-SLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LUX-032-SLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Camp-Collar Silk Resort Vacation Shirt",
        "slug": "camp-collar-silk-resort-vacation-shirt-33",
        "description": "Fluid Cuban-collar shirt in printed 16-momme silk crepe with relaxed dropped shoulders and vented hem.",
        "category_slug": "luxury-polos-shirts",
        "base_price": 7999.0,
        "discount_price": 6799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 27,
        "sales_count": 43,
        "primary_image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LUX-033-OBS-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LUX-033-OBS-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LUX-033-OBS-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LUX-033-OBS-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LUX-033-OBS-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LUX-033-IVO-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LUX-033-IVO-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LUX-033-IVO-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LUX-033-IVO-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LUX-033-IVO-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Open-Weave Cotton Crochet Resort Polo",
        "slug": "open-weave-cotton-crochet-resort-polo-34",
        "description": "Textured artisanal crochet polo shirt with airy retro stitchwork and relaxed open neckline.",
        "category_slug": "luxury-polos-shirts",
        "base_price": 6999.0,
        "discount_price": 5799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 33,
        "sales_count": 44,
        "primary_image": "https://images.unsplash.com/photo-1617137984095-74e4e5e3613f?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LUX-034-CAM-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LUX-034-CAM-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LUX-034-CAM-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LUX-034-CAM-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LUX-034-CAM-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LUX-034-ESP-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LUX-034-ESP-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LUX-034-ESP-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LUX-034-ESP-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LUX-034-ESP-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Milano Ribbed Wool-Silk Polo Sweater",
        "slug": "milano-ribbed-wool-silk-polo-sweater-35",
        "description": "Substantial Milano stitch knit polo with structured collar, perfect for elevated evening resort dining.",
        "category_slug": "luxury-polos-shirts",
        "base_price": 7499.0,
        "discount_price": 6299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 32,
        "sales_count": 45,
        "primary_image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LUX-035-BUR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LUX-035-BUR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LUX-035-BUR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LUX-035-BUR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LUX-035-BUR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LUX-035-CLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LUX-035-CLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LUX-035-CLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LUX-035-CLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LUX-035-CLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Retro Johnny-Collar Piqu\u00e9 Polo",
        "slug": "retro-johnny-collar-piqu-polo-36",
        "description": "Clean collar design without buttons, tailored in double-mercerized Egyptian cotton with ribbed cuffs.",
        "category_slug": "luxury-polos-shirts",
        "base_price": 5499.0,
        "discount_price": 4599.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 38,
        "sales_count": 46,
        "primary_image": "https://images.unsplash.com/photo-1506152983158-b4a74a01c721?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LUX-036-MID-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LUX-036-MID-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LUX-036-MID-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LUX-036-MID-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LUX-036-MID-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LUX-036-CHA-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LUX-036-CHA-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LUX-036-CHA-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LUX-036-CHA-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LUX-036-CHA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Washed Linen-Tencel Camp Resort Top",
        "slug": "washed-linen-tencel-camp-resort-top-37",
        "description": "Silky-soft relaxed resort shirt combining cooling linen with fluid Tencel in sun-bleached terracotta.",
        "category_slug": "luxury-polos-shirts",
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 44,
        "sales_count": 47,
        "primary_image": "https://images.unsplash.com/photo-1527719327859-c6ce80353573?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LUX-037-FOR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LUX-037-FOR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LUX-037-FOR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LUX-037-FOR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LUX-037-FOR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LUX-037-SLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LUX-037-SLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LUX-037-SLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LUX-037-SLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LUX-037-SLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Fine-Stripe Textured Cotton Popover",
        "slug": "fine-stripe-textured-cotton-popover-38",
        "description": "Casual elegance three-button popover shirt with standing band collar and chest patch pocket.",
        "category_slug": "luxury-polos-shirts",
        "base_price": 5799.0,
        "discount_price": 4799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 50,
        "sales_count": 48,
        "primary_image": "https://images.unsplash.com/photo-1499971856191-1a420a42b498?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LUX-038-OBS-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LUX-038-OBS-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LUX-038-OBS-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LUX-038-OBS-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LUX-038-OBS-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LUX-038-IVO-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LUX-038-IVO-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LUX-038-IVO-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LUX-038-IVO-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LUX-038-IVO-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cable-Knit Cashmere-Cotton Blend Polo",
        "slug": "cable-knit-cashmere-cotton-blend-polo-39",
        "description": "Delicate micro-cable knit polo in ultra-soft cashmere-cotton with horn buttons and ribbed hem.",
        "category_slug": "luxury-polos-shirts",
        "base_price": 8499.0,
        "discount_price": 7199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 56,
        "sales_count": 49,
        "primary_image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LUX-039-CAM-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LUX-039-CAM-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LUX-039-CAM-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LUX-039-CAM-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LUX-039-CAM-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LUX-039-ESP-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LUX-039-ESP-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LUX-039-ESP-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LUX-039-ESP-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LUX-039-ESP-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Watercolor Botanical Silk Resort Shirt",
        "slug": "watercolor-botanical-silk-resort-shirt-40",
        "description": "Hand-painted botanical motif printed on pure silk twill with straight hem and mother-of-pearl buttons.",
        "category_slug": "luxury-polos-shirts",
        "base_price": 8999.0,
        "discount_price": 7499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 62,
        "sales_count": 30,
        "primary_image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LUX-040-BUR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LUX-040-BUR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LUX-040-BUR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LUX-040-BUR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LUX-040-BUR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LUX-040-CLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LUX-040-CLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LUX-040-CLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LUX-040-CLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LUX-040-CLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Sartorial Super 150s Wool-Silk Navy Blazer",
        "slug": "sartorial-super-150s-wool-silk-navy-blazer-41",
        "description": "Unstructured Italian tailoring featuring Super 150s virgin wool blended with mulberry silk and horn buttons.",
        "category_slug": "tailored-blazers",
        "base_price": 18999.0,
        "discount_price": 15999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 18,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-041-MID-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-041-MID-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-041-MID-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-041-MID-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-041-MID-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-041-CHA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-041-CHA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-041-CHA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-041-CHA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-041-CHA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Double-Breasted Camel Wool Sport Coat",
        "slug": "double-breasted-camel-wool-sport-coat-42",
        "description": "Classic 6x2 double-breasted sport coat with peak lapels, patch pockets, and half-canvas construction.",
        "category_slug": "tailored-blazers",
        "base_price": 21999.0,
        "discount_price": 18499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 17,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-042-FOR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-042-FOR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-042-FOR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-042-FOR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-042-FOR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-042-SLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-042-SLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-042-SLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-042-SLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-042-SLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Houndstooth Tweed Hand-Tailored Blazer",
        "slug": "houndstooth-tweed-hand-tailored-blazer-43",
        "description": "Heritage wool-cashmere tweed jacket featuring timeless micro-houndstooth and soft Neapolitan shoulders.",
        "category_slug": "tailored-blazers",
        "base_price": 19999.0,
        "discount_price": 16999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 23,
        "sales_count": 33,
        "primary_image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-043-OBS-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-043-OBS-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-043-OBS-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-043-OBS-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-043-OBS-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-043-IVO-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-043-IVO-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-043-IVO-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-043-IVO-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-043-IVO-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Linen-Silk-Wool Hopsack Summer Blazer",
        "slug": "linen-silk-wool-hopsack-summer-blazer-44",
        "description": "Breathable three-season hopsack jacket woven in Biella with butterfly lining and patch pockets.",
        "category_slug": "tailored-blazers",
        "base_price": 17999.0,
        "discount_price": 14999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 29,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1539025828301-b314ca222fa9?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-044-CAM-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-044-CAM-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-044-CAM-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-044-CAM-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-044-CAM-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-044-ESP-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-044-ESP-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-044-ESP-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-044-ESP-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-044-ESP-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Black Velvet Shawl-Collar Dinner Jacket",
        "slug": "black-velvet-shawl-collar-dinner-jacket-45",
        "description": "Opulent evening tuxedo blazer tailored from deep black cotton velvet with grosgrain silk lapels.",
        "category_slug": "tailored-blazers",
        "base_price": 22999.0,
        "discount_price": 19499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 35,
        "sales_count": 35,
        "primary_image": "https://images.unsplash.com/photo-1667846088471-a8b126bf77ba?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-045-BUR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-045-BUR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-045-BUR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-045-BUR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-045-BUR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-045-CLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-045-CLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-045-CLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-045-CLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-045-CLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Checked Cashmere-Blend Winter Sport Coat",
        "slug": "checked-cashmere-blend-winter-sport-coat-46",
        "description": "Warm windowpane check jacket combining Scottish cashmere with lambswool and genuine leather buttons.",
        "category_slug": "tailored-blazers",
        "base_price": 23999.0,
        "discount_price": 20499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 41,
        "sales_count": 36,
        "primary_image": "https://images.unsplash.com/photo-1520975954732-35dd22299614?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-046-MID-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-046-MID-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-046-MID-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-046-MID-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-046-MID-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-046-CHA-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-046-CHA-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-046-CHA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-046-CHA-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-046-CHA-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Single-Breasted Cream Silk-Wool Blazer",
        "slug": "single-breasted-cream-silk-wool-blazer-47",
        "description": "Refined warm-weather blazer with soft drape, pick-stitched lapels, and custom engraved corozo buttons.",
        "category_slug": "tailored-blazers",
        "base_price": 18499.0,
        "discount_price": 15499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 47,
        "sales_count": 37,
        "primary_image": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-047-FOR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-047-FOR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-047-FOR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-047-FOR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-047-FOR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-047-SLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-047-SLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-047-SLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-047-SLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-047-SLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Charcoal Herringbone Flannel Sport Coat",
        "slug": "charcoal-herringbone-flannel-sport-coat-48",
        "description": "Brushed wool flannel jacket featuring timeless herringbone weave and natural horn buttons.",
        "category_slug": "tailored-blazers",
        "base_price": 19499.0,
        "discount_price": 16499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 53,
        "sales_count": 38,
        "primary_image": "https://images.unsplash.com/photo-1479064555552-3ef4979f8908?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-048-OBS-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-048-OBS-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-048-OBS-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-048-OBS-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-048-OBS-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-048-IVO-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-048-IVO-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-048-IVO-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-048-IVO-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-048-IVO-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Olive Washed Cotton-Linen Safari Blazer",
        "slug": "olive-washed-cotton-linen-safari-blazer-49",
        "description": "Casual sartorial jacket with belted back, pleated bellows pockets, and convertible notched lapel.",
        "category_slug": "tailored-blazers",
        "base_price": 16999.0,
        "discount_price": 13999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 52,
        "sales_count": 39,
        "primary_image": "https://images.pexels.com/photos/1342609/pexels-photo-1342609.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-049-CAM-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-049-CAM-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-049-CAM-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-049-CAM-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-049-CAM-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-049-ESP-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-049-ESP-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-049-ESP-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-049-ESP-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-049-ESP-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Midnight Navy Tuxedo Jacket with Satin Lapels",
        "slug": "midnight-navy-tuxedo-jacket-with-satin-lapels-50",
        "description": "Black-tie dinner jacket tailored from barathea wool with silk satin face peak lapels and covered buttons.",
        "category_slug": "tailored-blazers",
        "base_price": 24999.0,
        "discount_price": 21499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 58,
        "sales_count": 40,
        "primary_image": "https://images.pexels.com/photos/325876/pexels-photo-325876.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-050-BUR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-050-BUR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-050-BUR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-050-BUR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-050-BUR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-050-CLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-050-CLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-050-CLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-050-CLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-050-CLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Double-Faced Cashmere Balmacaan Overcoat",
        "slug": "double-faced-cashmere-balmacaan-overcoat-51",
        "description": "Hand-sewn double-faced Mongolian cashmere overcoat with raglan sleeves and hidden horn button placket.",
        "category_slug": "overcoats-trench",
        "base_price": 28999.0,
        "discount_price": 24999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 14,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-OVE-051-MID-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-OVE-051-MID-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-OVE-051-MID-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-OVE-051-MID-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-OVE-051-MID-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-OVE-051-CHA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-OVE-051-CHA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-OVE-051-CHA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-OVE-051-CHA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-OVE-051-CHA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Belted Gabardine Storm-Proof Trench Coat",
        "slug": "belted-gabardine-storm-proof-trench-coat-52",
        "description": "Heritage weatherproof cotton gabardine trench coat featuring D-ring leather buckles and storm flap.",
        "category_slug": "overcoats-trench",
        "base_price": 21999.0,
        "discount_price": 18499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 20,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-OVE-052-FOR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-OVE-052-FOR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-OVE-052-FOR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-OVE-052-FOR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-OVE-052-FOR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-OVE-052-SLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-OVE-052-SLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-OVE-052-SLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-OVE-052-SLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-OVE-052-SLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Heavy Melton Wool Officers Greatcoat",
        "slug": "heavy-melton-wool-officers-greatcoat-53",
        "description": "Substantial 32oz Melton wool double-breasted coat with broad peak lapels and deep welt pockets.",
        "category_slug": "overcoats-trench",
        "base_price": 23999.0,
        "discount_price": 19999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 26,
        "sales_count": 43,
        "primary_image": "https://images.unsplash.com/photo-1724709972210-4beb408de580?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-OVE-053-OBS-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-OVE-053-OBS-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-OVE-053-OBS-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-OVE-053-OBS-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-OVE-053-OBS-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-OVE-053-IVO-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-OVE-053-IVO-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-OVE-053-IVO-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-OVE-053-IVO-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-OVE-053-IVO-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Camel Hair Double-Breasted Polo Coat",
        "slug": "camel-hair-double-breasted-polo-coat-54",
        "description": "Luxurious 100% baby camel hair coat featuring frame pockets, half-belt back, and cupro lining.",
        "category_slug": "overcoats-trench",
        "base_price": 26999.0,
        "discount_price": 22999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 32,
        "sales_count": 44,
        "primary_image": "https://images.pexels.com/photos/157675/fashion-men-s-individuality-black-and-white-157675.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-OVE-054-CAM-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-OVE-054-CAM-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-OVE-054-CAM-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-OVE-054-CAM-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-OVE-054-CAM-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-OVE-054-ESP-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-OVE-054-ESP-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-OVE-054-ESP-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-OVE-054-ESP-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-OVE-054-ESP-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Houndstooth Raglan Car Coat",
        "slug": "houndstooth-raglan-car-coat-55",
        "description": "Modern minimalist overcoat in checked wool tweed with water-repellent finish and slash pockets.",
        "category_slug": "overcoats-trench",
        "base_price": 19999.0,
        "discount_price": 16999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 38,
        "sales_count": 45,
        "primary_image": "https://images.pexels.com/photos/1040880/pexels-photo-1040880.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-OVE-055-BUR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-OVE-055-BUR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-OVE-055-BUR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-OVE-055-BUR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-OVE-055-BUR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-OVE-055-CLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-OVE-055-CLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-OVE-055-CLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-OVE-055-CLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-OVE-055-CLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Navy Cashmere-Wool Chesteck Overcoat",
        "slug": "navy-cashmere-wool-chesteck-overcoat-56",
        "description": "Slim-tailored single-breasted overcoat with velvet collar accent and interior ticket pocket.",
        "category_slug": "overcoats-trench",
        "base_price": 22499.0,
        "discount_price": 18999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 37,
        "sales_count": 46,
        "primary_image": "https://images.pexels.com/photos/1040882/pexels-photo-1040882.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-OVE-056-MID-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-OVE-056-MID-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-OVE-056-MID-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-OVE-056-MID-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-OVE-056-MID-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-OVE-056-CHA-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-OVE-056-CHA-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-OVE-056-CHA-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-OVE-056-CHA-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-OVE-056-CHA-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Waxed Cotton Storm Duster Raincoat",
        "slug": "waxed-cotton-storm-duster-raincoat-57",
        "description": "Heritage British waxed cotton long raincoat with corduroy collar and plaid cotton lining.",
        "category_slug": "overcoats-trench",
        "base_price": 18999.0,
        "discount_price": 15999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 43,
        "sales_count": 47,
        "primary_image": "https://images.pexels.com/photos/1040883/pexels-photo-1040883.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-OVE-057-FOR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-OVE-057-FOR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-OVE-057-FOR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-OVE-057-FOR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-OVE-057-FOR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-OVE-057-SLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-OVE-057-SLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-OVE-057-SLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-OVE-057-SLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-OVE-057-SLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Boucl\u00e9 Wool Wrap Coat with Sash Belt",
        "slug": "boucl-wool-wrap-coat-with-sash-belt-58",
        "description": "Plush textured boucl\u00e9 wool wrap coat with dropped shoulders and oversized patch pockets.",
        "category_slug": "overcoats-trench",
        "base_price": 20999.0,
        "discount_price": 17499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 49,
        "sales_count": 48,
        "primary_image": "https://images.pexels.com/photos/1040885/pexels-photo-1040885.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-OVE-058-OBS-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-OVE-058-OBS-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-OVE-058-OBS-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-OVE-058-OBS-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-OVE-058-OBS-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-OVE-058-IVO-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-OVE-058-IVO-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-OVE-058-IVO-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-OVE-058-IVO-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-OVE-058-IVO-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Herringbone Wool-Alpaca Longline Coat",
        "slug": "herringbone-wool-alpaca-longline-coat-59",
        "description": "Warm textured alpaca-wool blend overcoat with dramatic longline drape and horn buttons.",
        "category_slug": "overcoats-trench",
        "base_price": 24499.0,
        "discount_price": 20999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 55,
        "sales_count": 49,
        "primary_image": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-OVE-059-CAM-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-OVE-059-CAM-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-OVE-059-CAM-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-OVE-059-CAM-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-OVE-059-CAM-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-OVE-059-ESP-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-OVE-059-ESP-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-OVE-059-ESP-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-OVE-059-ESP-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-OVE-059-ESP-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Bonded Storm-Shell Hooded Mac Coat",
        "slug": "bonded-storm-shell-hooded-mac-coat-60",
        "description": "Ultra-clean bonded Italian technical wool mac with taped waterproof seams and detachable hood.",
        "category_slug": "overcoats-trench",
        "base_price": 21499.0,
        "discount_price": 17999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 61,
        "sales_count": 30,
        "primary_image": "https://images.pexels.com/photos/1043474/pexels-photo-1043474.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-OVE-060-BUR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-OVE-060-BUR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-OVE-060-BUR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-OVE-060-BUR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-OVE-060-BUR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-OVE-060-CLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-OVE-060-CLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-OVE-060-CLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-OVE-060-CLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-OVE-060-CLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "18-Gauge Extra-Fine Merino Crewneck",
        "slug": "18-gauge-extra-fine-merino-crewneck-61",
        "description": "Ultra-fine lightweight crewneck knit from Australian merino wool with ribbed cuffs and hem.",
        "category_slug": "fine-knitwear",
        "base_price": 6999.0,
        "discount_price": 5799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 17,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FIN-061-MID-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FIN-061-MID-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FIN-061-MID-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FIN-061-MID-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FIN-061-MID-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FIN-061-CHA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FIN-061-CHA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FIN-061-CHA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FIN-061-CHA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FIN-061-CHA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Silk-Cashmere Seamless Mock Neck",
        "slug": "silk-cashmere-seamless-mock-neck-62",
        "description": "Featherweight mock neck sweater blending 70% silk and 30% cashmere for effortless under-blazer layering.",
        "category_slug": "fine-knitwear",
        "base_price": 8499.0,
        "discount_price": 7199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 23,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FIN-062-FOR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FIN-062-FOR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FIN-062-FOR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FIN-062-FOR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FIN-062-FOR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FIN-062-SLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FIN-062-SLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FIN-062-SLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FIN-062-SLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FIN-062-SLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Waffle-Knit Organic Pima Cotton Crew",
        "slug": "waffle-knit-organic-pima-cotton-crew-63",
        "description": "Subtle micro-waffle textured long sleeve top knit from Peruvian Pima cotton with saddle shoulders.",
        "category_slug": "fine-knitwear",
        "base_price": 5499.0,
        "discount_price": 4599.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 22,
        "sales_count": 33,
        "primary_image": "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FIN-063-OBS-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FIN-063-OBS-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FIN-063-OBS-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FIN-063-OBS-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FIN-063-OBS-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FIN-063-IVO-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FIN-063-IVO-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FIN-063-IVO-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FIN-063-IVO-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FIN-063-IVO-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Fine-Gauge Merino V-Neck Sweater",
        "slug": "fine-gauge-merino-v-neck-sweater-64",
        "description": "Classic sartorial V-neck sweater in 16-gauge merino wool with refined hand-linked neckline.",
        "category_slug": "fine-knitwear",
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 28,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1619856699906-09e1f58c98b1?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FIN-064-CAM-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FIN-064-CAM-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FIN-064-CAM-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FIN-064-CAM-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FIN-064-CAM-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FIN-064-ESP-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FIN-064-ESP-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FIN-064-ESP-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FIN-064-ESP-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FIN-064-ESP-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Tissue-Weight Cashmere Long Sleeve",
        "slug": "tissue-weight-cashmere-long-sleeve-65",
        "description": "Semi-sheer tissue cashmere top designed for transitional weather and luxurious skin-soft warmth.",
        "category_slug": "fine-knitwear",
        "base_price": 9499.0,
        "discount_price": 7999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 34,
        "sales_count": 35,
        "primary_image": "https://images.unsplash.com/photo-1627161683077-e34782c24d81?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FIN-065-BUR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FIN-065-BUR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FIN-065-BUR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FIN-065-BUR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FIN-065-BUR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FIN-065-CLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FIN-065-CLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FIN-065-CLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FIN-065-CLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FIN-065-CLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Ribbed Viscose-Silk Fitted Turtleneck",
        "slug": "ribbed-viscose-silk-fitted-turtleneck-66",
        "description": "Sleek second-skin ribbed turtleneck knit with shape retention and luminous luster.",
        "category_slug": "fine-knitwear",
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 40,
        "sales_count": 36,
        "primary_image": "https://images.pexels.com/photos/45982/pexels-photo-45982.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FIN-066-MID-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FIN-066-MID-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FIN-066-MID-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FIN-066-MID-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-FIN-066-MID-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FIN-066-CHA-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FIN-066-CHA-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FIN-066-CHA-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FIN-066-CHA-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-FIN-066-CHA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "French Terry Knit Long-Sleeve Henley",
        "slug": "french-terry-knit-long-sleeve-henley-67",
        "description": "Three-button henley knit from micro-loop French terry with tonal mother-of-pearl buttons.",
        "category_slug": "fine-knitwear",
        "base_price": 5299.0,
        "discount_price": 4399.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 46,
        "sales_count": 37,
        "primary_image": "https://images.pexels.com/photos/704815/pexels-photo-704815.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FIN-067-FOR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FIN-067-FOR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FIN-067-FOR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FIN-067-FOR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-FIN-067-FOR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FIN-067-SLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FIN-067-SLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FIN-067-SLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FIN-067-SLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-FIN-067-SLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Sea Island Cotton Fine Polo Sweater",
        "slug": "sea-island-cotton-fine-polo-sweater-68",
        "description": "Refined knitted polo with collar and placket in genuine Sea Island cotton with clean finish.",
        "category_slug": "fine-knitwear",
        "base_price": 7999.0,
        "discount_price": 6799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 52,
        "sales_count": 38,
        "primary_image": "https://images.pexels.com/photos/1036623/pexels-photo-1036623.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FIN-068-OBS-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FIN-068-OBS-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FIN-068-OBS-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FIN-068-OBS-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-FIN-068-OBS-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FIN-068-IVO-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FIN-068-IVO-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FIN-068-IVO-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FIN-068-IVO-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-FIN-068-IVO-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Pure Silk Knit Long-Sleeve Undershirt",
        "slug": "pure-silk-knit-long-sleeve-undershirt-69",
        "description": "Ultra-luxurious pure silk jersey top offering natural thermal regulation and sublime comfort.",
        "category_slug": "fine-knitwear",
        "base_price": 7499.0,
        "discount_price": 6299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 58,
        "sales_count": 39,
        "primary_image": "https://images.pexels.com/photos/1964970/pexels-photo-1964970.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FIN-069-CAM-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FIN-069-CAM-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FIN-069-CAM-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FIN-069-CAM-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-FIN-069-CAM-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FIN-069-ESP-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FIN-069-ESP-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FIN-069-ESP-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FIN-069-ESP-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-FIN-069-ESP-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Two-Tone Mouline Fine Wool Crewneck",
        "slug": "two-tone-mouline-fine-wool-crewneck-70",
        "description": "Sophisticated melange yarn crewneck sweater blending charcoal and cream merino fibers.",
        "category_slug": "fine-knitwear",
        "base_price": 6799.0,
        "discount_price": 5699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 57,
        "sales_count": 40,
        "primary_image": "https://images.pexels.com/photos/2584269/pexels-photo-2584269.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FIN-070-BUR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FIN-070-BUR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FIN-070-BUR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FIN-070-BUR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-FIN-070-BUR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FIN-070-CLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FIN-070-CLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FIN-070-CLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FIN-070-CLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-FIN-070-CLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Chunky Cable-Knit Mongolian Cashmere Turtleneck",
        "slug": "chunky-cable-knit-mongolian-cashmere-turtleneck-71",
        "description": "Heavyweight 4-ply pure cashmere sweater featuring hand-finished cables and a plush foldover neck.",
        "category_slug": "sweaters-cardigans",
        "base_price": 14999.0,
        "discount_price": 12499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 13,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SWE-071-MID-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SWE-071-MID-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SWE-071-MID-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SWE-071-MID-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SWE-071-MID-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SWE-071-CHA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SWE-071-CHA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SWE-071-CHA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SWE-071-CHA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SWE-071-CHA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Shawl-Collar Ribbed Cardigan in Merino Wool",
        "slug": "shawl-collar-ribbed-cardigan-in-merino-wool-72",
        "description": "Architectural cardigan featuring a substantial ribbed shawl collar and genuine braided leather buttons.",
        "category_slug": "sweaters-cardigans",
        "base_price": 12999.0,
        "discount_price": 10999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 19,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SWE-072-FOR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SWE-072-FOR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SWE-072-FOR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SWE-072-FOR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SWE-072-FOR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SWE-072-SLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SWE-072-SLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SWE-072-SLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SWE-072-SLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SWE-072-SLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Brushed Mohair-Wool Ombr\u00e9 Cardigan",
        "slug": "brushed-mohair-wool-ombr-cardigan-73",
        "description": "Soft fuzzy mohair-blend cardigan in rich autumn tones with dropped shoulders and horn buttons.",
        "category_slug": "sweaters-cardigans",
        "base_price": 11999.0,
        "discount_price": 9999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 25,
        "sales_count": 43,
        "primary_image": "https://images.unsplash.com/photo-1536243298747-ea8874136d64?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SWE-073-OBS-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SWE-073-OBS-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SWE-073-OBS-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SWE-073-OBS-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SWE-073-OBS-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SWE-073-IVO-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SWE-073-IVO-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SWE-073-IVO-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SWE-073-IVO-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SWE-073-IVO-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Fisherman Rib Cashmere-Wool Pullover",
        "slug": "fisherman-rib-cashmere-wool-pullover-74",
        "description": "Heavyweight British fisherman knit sweater with raglan sleeves and deep ribbed trims.",
        "category_slug": "sweaters-cardigans",
        "base_price": 13499.0,
        "discount_price": 11299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 31,
        "sales_count": 44,
        "primary_image": "https://images.pexels.com/photos/1036622/pexels-photo-1036622.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SWE-074-CAM-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SWE-074-CAM-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SWE-074-CAM-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SWE-074-CAM-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SWE-074-CAM-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SWE-074-ESP-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SWE-074-ESP-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SWE-074-ESP-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SWE-074-ESP-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SWE-074-ESP-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Button-Through Fine Cashmere Cardigan",
        "slug": "button-through-fine-cashmere-cardigan-75",
        "description": "Tailored slim-fit cardigan in 2-ply cashmere with mother-of-pearl buttons and welt pockets.",
        "category_slug": "sweaters-cardigans",
        "base_price": 10999.0,
        "discount_price": 9199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 37,
        "sales_count": 45,
        "primary_image": "https://images.pexels.com/photos/1040881/pexels-photo-1040881.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SWE-075-BUR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SWE-075-BUR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SWE-075-BUR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SWE-075-BUR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SWE-075-BUR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SWE-075-CLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SWE-075-CLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SWE-075-CLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SWE-075-CLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SWE-075-CLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Waffle-Knit Alpaca-Blend Crew Sweater",
        "slug": "waffle-knit-alpaca-blend-crew-sweater-76",
        "description": "Airy yet exceptionally insulating alpaca wool sweater with textured thermal waffle stitch.",
        "category_slug": "sweaters-cardigans",
        "base_price": 11499.0,
        "discount_price": 9699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 43,
        "sales_count": 46,
        "primary_image": "https://images.pexels.com/photos/1381553/pexels-photo-1381553.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SWE-076-MID-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SWE-076-MID-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SWE-076-MID-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SWE-076-MID-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SWE-076-MID-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SWE-076-CHA-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SWE-076-CHA-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SWE-076-CHA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SWE-076-CHA-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SWE-076-CHA-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Zip-Through Cashmere Funnel-Neck Sweater",
        "slug": "zip-through-cashmere-funnel-neck-sweater-77",
        "description": "Sporty sartorial sweater with two-way palladium zipper and supple lambskin pull tab.",
        "category_slug": "sweaters-cardigans",
        "base_price": 13999.0,
        "discount_price": 11799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 42,
        "sales_count": 47,
        "primary_image": "https://images.pexels.com/photos/1381557/pexels-photo-1381557.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SWE-077-FOR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SWE-077-FOR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SWE-077-FOR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SWE-077-FOR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SWE-077-FOR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SWE-077-SLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SWE-077-SLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SWE-077-SLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SWE-077-SLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SWE-077-SLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Fair Isle Lambswool Heritage Sweater",
        "slug": "fair-isle-lambswool-heritage-sweater-78",
        "description": "Authentic Scottish Fair Isle patterned yoke sweater spun from pure supersoft Shetland lambswool.",
        "category_slug": "sweaters-cardigans",
        "base_price": 10499.0,
        "discount_price": 8799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 48,
        "sales_count": 48,
        "primary_image": "https://images.pexels.com/photos/1381558/pexels-photo-1381558.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SWE-078-OBS-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SWE-078-OBS-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SWE-078-OBS-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SWE-078-OBS-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SWE-078-OBS-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SWE-078-IVO-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SWE-078-IVO-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SWE-078-IVO-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SWE-078-IVO-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SWE-078-IVO-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Oversized Ribbed Cashmere Boyfriend Cardigan",
        "slug": "oversized-ribbed-cashmere-boyfriend-cardigan-79",
        "description": "Slouchy luxury cardigan with deep V-neckline, oversized patch pockets, and tortoiseshell buttons.",
        "category_slug": "sweaters-cardigans",
        "base_price": 15499.0,
        "discount_price": 12999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 54,
        "sales_count": 49,
        "primary_image": "https://images.pexels.com/photos/6995704/pexels-photo-6995704.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SWE-079-CAM-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SWE-079-CAM-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SWE-079-CAM-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SWE-079-CAM-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SWE-079-CAM-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SWE-079-ESP-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SWE-079-ESP-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SWE-079-ESP-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SWE-079-ESP-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SWE-079-ESP-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Double-Breasted Knit Wool Peacoat Cardigan",
        "slug": "double-breasted-knit-wool-peacoat-cardigan-80",
        "description": "Substantial outerwear cardigan knit in dense Milano stitch with anchor-embossed metal buttons.",
        "category_slug": "sweaters-cardigans",
        "base_price": 16499.0,
        "discount_price": 13999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 60,
        "sales_count": 30,
        "primary_image": "https://images.pexels.com/photos/1485781/pexels-photo-1485781.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SWE-080-BUR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SWE-080-BUR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SWE-080-BUR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SWE-080-BUR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SWE-080-BUR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SWE-080-CLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SWE-080-CLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SWE-080-CLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SWE-080-CLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SWE-080-CLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "High-Rise Pleated Wool Flannel Trousers",
        "slug": "high-rise-pleated-wool-flannel-trousers-81",
        "description": "Sartorial formal trousers with double forward pleats, extended tab waistband, and side adjusters.",
        "category_slug": "tailored-trousers",
        "base_price": 9999.0,
        "discount_price": 8499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 16,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-081-MID-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-081-MID-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-081-MID-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-081-MID-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-081-MID-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-081-CHA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-081-CHA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-081-CHA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-081-CHA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-081-CHA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Vitale Barberis Canonico Wool Serge Slacks",
        "slug": "vitale-barberis-canonico-wool-serge-slacks-82",
        "description": "Year-round dress trousers woven by Italy's VBC mill, featuring curtained waistband and unfinished hems.",
        "category_slug": "tailored-trousers",
        "base_price": 10999.0,
        "discount_price": 9299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 22,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-082-FOR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-082-FOR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-082-FOR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-082-FOR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-082-FOR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-082-SLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-082-SLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-082-SLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-082-SLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-082-SLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Bespoke Tuxedo Trousers with Silk Side Stripe",
        "slug": "bespoke-tuxedo-trousers-with-silk-side-stripe-83",
        "description": "Formal black-tie trousers crafted from midnight barathea wool with pure silk satin galon side stripes.",
        "category_slug": "tailored-trousers",
        "base_price": 11999.0,
        "discount_price": 9999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 28,
        "sales_count": 33,
        "primary_image": "https://images.unsplash.com/photo-1614890085618-0e1054da74f8?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-083-OBS-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-083-OBS-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-083-OBS-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-083-OBS-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-083-OBS-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-083-IVO-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-083-IVO-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-083-IVO-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-083-IVO-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-083-IVO-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Gurkha Waistband Wool-Linen Trousers",
        "slug": "gurkha-waistband-wool-linen-trousers-84",
        "description": "Heritage double-buckle Gurkha waistband trousers with deep front pleats and tapered cuff hems.",
        "category_slug": "tailored-trousers",
        "base_price": 10499.0,
        "discount_price": 8799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 27,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1580411450318-6abb27b94eeb?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-084-CAM-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-084-CAM-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-084-CAM-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-084-CAM-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-084-CAM-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-084-ESP-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-084-ESP-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-084-ESP-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-084-ESP-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-084-ESP-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Houndstooth Tweed Dress Trousers",
        "slug": "houndstooth-tweed-dress-trousers-85",
        "description": "English country style tailored trousers in pure wool houndstooth with horn button tab and coin pocket.",
        "category_slug": "tailored-trousers",
        "base_price": 9499.0,
        "discount_price": 7999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 33,
        "sales_count": 35,
        "primary_image": "https://images.unsplash.com/photo-1582439170934-d089aa10abda?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-085-BUR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-085-BUR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-085-BUR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-085-BUR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-085-BUR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-085-CLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-085-CLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-085-CLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-085-CLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-085-CLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Slim-Cut Stretch Wool Gabardine Slacks",
        "slug": "slim-cut-stretch-wool-gabardine-slacks-86",
        "description": "Modern slim trousers with comfortable natural stretch, crease retention, and pick-stitched pockets.",
        "category_slug": "tailored-trousers",
        "base_price": 8999.0,
        "discount_price": 7499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 39,
        "sales_count": 36,
        "primary_image": "https://images.unsplash.com/photo-1704775991545-fc0507822fea?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-086-MID-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-086-MID-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-086-MID-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-086-MID-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TAI-086-MID-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-086-CHA-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-086-CHA-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-086-CHA-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-086-CHA-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TAI-086-CHA-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Drawstring Tailored Wool Flannel Pants",
        "slug": "drawstring-tailored-wool-flannel-pants-87",
        "description": "Contemporary hybrid pants pairing sartorial wool flannel with an internal elastic drawstring waist.",
        "category_slug": "tailored-trousers",
        "base_price": 8499.0,
        "discount_price": 7199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 45,
        "sales_count": 37,
        "primary_image": "https://images.pexels.com/photos/2897531/pexels-photo-2897531.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-087-FOR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-087-FOR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-087-FOR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-087-FOR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TAI-087-FOR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-087-SLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-087-SLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-087-SLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-087-SLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TAI-087-SLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Lightweight Tropical Wool Travel Trousers",
        "slug": "lightweight-tropical-wool-travel-trousers-88",
        "description": "High-twist wrinkle-resistant tropical wool pants designed for global business travel.",
        "category_slug": "tailored-trousers",
        "base_price": 9799.0,
        "discount_price": 8299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 51,
        "sales_count": 38,
        "primary_image": "https://images.pexels.com/photos/247204/pexels-photo-247204.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-088-OBS-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-088-OBS-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-088-OBS-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-088-OBS-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TAI-088-OBS-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-088-IVO-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-088-IVO-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-088-IVO-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-088-IVO-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TAI-088-IVO-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Wide-Leg Pleated Wool Twill Trousers",
        "slug": "wide-leg-pleated-wool-twill-trousers-89",
        "description": "Dramatic relaxed drape trousers with deep pleats, wide leg profile, and horn button fly.",
        "category_slug": "tailored-trousers",
        "base_price": 11499.0,
        "discount_price": 9699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 57,
        "sales_count": 39,
        "primary_image": "https://images.pexels.com/photos/1183266/pexels-photo-1183266.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-089-CAM-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-089-CAM-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-089-CAM-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-089-CAM-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TAI-089-CAM-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-089-ESP-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-089-ESP-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-089-ESP-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-089-ESP-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TAI-089-ESP-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Charcoal Sharkskin Tailored Dress Pants",
        "slug": "charcoal-sharkskin-tailored-dress-pants-90",
        "description": "Luminous two-tone sharkskin wool trousers offering exceptional drape and boardroom polish.",
        "category_slug": "tailored-trousers",
        "base_price": 10299.0,
        "discount_price": 8699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 63,
        "sales_count": 40,
        "primary_image": "https://images.pexels.com/photos/375880/pexels-photo-375880.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-090-BUR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-090-BUR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-090-BUR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-090-BUR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TAI-090-BUR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-090-CLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-090-CLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-090-CLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-090-CLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TAI-090-CLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Garment-Dyed Supima Cotton Chinos",
        "slug": "garment-dyed-supima-cotton-chinos-91",
        "description": "Tailored flat-front chinos crafted from American Supima cotton with a peach-skin finish and horn buttons.",
        "category_slug": "chinos-casual-pants",
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 12,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CHI-091-MID-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CHI-091-MID-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CHI-091-MID-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CHI-091-MID-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CHI-091-MID-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CHI-091-CHA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CHI-091-CHA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CHI-091-CHA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CHI-091-CHA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CHI-091-CHA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Pleated Relaxed-Fit Cotton Fatigue Trousers",
        "slug": "pleated-relaxed-fit-cotton-fatigue-trousers-92",
        "description": "Military-inspired casual trousers with front patch pockets, button side-tabs, and relaxed taper.",
        "category_slug": "chinos-casual-pants",
        "base_price": 6999.0,
        "discount_price": 5899.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 18,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1517445312882-bc9910d016b7?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CHI-092-FOR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CHI-092-FOR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CHI-092-FOR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CHI-092-FOR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CHI-092-FOR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CHI-092-SLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CHI-092-SLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CHI-092-SLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CHI-092-SLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CHI-092-SLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Stretch Cotton-Cashmere Luxury Chinos",
        "slug": "stretch-cotton-cashmere-luxury-chinos-93",
        "description": "Incredibly soft five-pocket casual trousers blending combed cotton with a touch of noble cashmere.",
        "category_slug": "chinos-casual-pants",
        "base_price": 7999.0,
        "discount_price": 6799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 24,
        "sales_count": 43,
        "primary_image": "https://images.pexels.com/photos/1687719/pexels-photo-1687719.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CHI-093-OBS-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CHI-093-OBS-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CHI-093-OBS-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CHI-093-OBS-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CHI-093-OBS-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CHI-093-IVO-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CHI-093-IVO-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CHI-093-IVO-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CHI-093-IVO-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CHI-093-IVO-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Fine-Wale Corduroy Tailored Pants",
        "slug": "fine-wale-corduroy-tailored-pants-94",
        "description": "Vintage-inspired trousers in 16-wale Italian cotton corduroy with brass hardware and coin pocket.",
        "category_slug": "chinos-casual-pants",
        "base_price": 7499.0,
        "discount_price": 6299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 30,
        "sales_count": 44,
        "primary_image": "https://images.unsplash.com/photo-1618001789196-8b986847cd5e?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CHI-094-CAM-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CHI-094-CAM-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CHI-094-CAM-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CHI-094-CAM-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CHI-094-CAM-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CHI-094-ESP-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CHI-094-ESP-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CHI-094-ESP-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CHI-094-ESP-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CHI-094-ESP-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Drawstring Elastic-Waist Casual Linen-Cotton Pants",
        "slug": "drawstring-elastic-waist-casual-linen-cotton-pants-95",
        "description": "Effortless casual trousers with a stretch waistband, internal cotton drawcord, and tapered leg.",
        "category_slug": "chinos-casual-pants",
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 36,
        "sales_count": 45,
        "primary_image": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CHI-095-BUR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CHI-095-BUR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CHI-095-BUR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CHI-095-BUR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CHI-095-BUR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CHI-095-CLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CHI-095-CLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CHI-095-CLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CHI-095-CLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CHI-095-CLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Utility Carpenter Pants in Brushed Cotton Canvas",
        "slug": "utility-carpenter-pants-in-brushed-cotton-canvas-96",
        "description": "Refined utilitarian trousers with hammer loop, reinforced tool pockets, and triple-needle stitching.",
        "category_slug": "chinos-casual-pants",
        "base_price": 6799.0,
        "discount_price": 5699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 42,
        "sales_count": 46,
        "primary_image": "https://images.pexels.com/photos/1598508/pexels-photo-1598508.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CHI-096-MID-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CHI-096-MID-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CHI-096-MID-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CHI-096-MID-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CHI-096-MID-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CHI-096-CHA-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CHI-096-CHA-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CHI-096-CHA-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CHI-096-CHA-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CHI-096-CHA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Tapered Tech-Cotton Commuter Trousers",
        "slug": "tapered-tech-cotton-commuter-trousers-97",
        "description": "Weather-resistant cotton-blend trousers with articulated knees and hidden zippered phone pocket.",
        "category_slug": "chinos-casual-pants",
        "base_price": 7299.0,
        "discount_price": 6199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 48,
        "sales_count": 47,
        "primary_image": "https://images.pexels.com/photos/1598509/pexels-photo-1598509.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CHI-097-FOR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CHI-097-FOR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CHI-097-FOR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CHI-097-FOR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CHI-097-FOR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CHI-097-SLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CHI-097-SLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CHI-097-SLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CHI-097-SLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CHI-097-SLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Herringbone Twill Officer Field Pants",
        "slug": "herringbone-twill-officer-field-pants-98",
        "description": "Rugged military chino reproduced in textured herringbone cotton with melamine button fly.",
        "category_slug": "chinos-casual-pants",
        "base_price": 6299.0,
        "discount_price": 5299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 47,
        "sales_count": 48,
        "primary_image": "https://images.pexels.com/photos/1598510/pexels-photo-1598510.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CHI-098-OBS-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CHI-098-OBS-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CHI-098-OBS-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CHI-098-OBS-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CHI-098-OBS-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CHI-098-IVO-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CHI-098-IVO-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CHI-098-IVO-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CHI-098-IVO-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CHI-098-IVO-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Pleated Cropped Cotton Trousers",
        "slug": "pleated-cropped-cotton-trousers-99",
        "description": "Modern Japanese-cut cropped trousers with single forward pleats and clean 2-inch turned-up cuffs.",
        "category_slug": "chinos-casual-pants",
        "base_price": 6699.0,
        "discount_price": 5599.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 53,
        "sales_count": 49,
        "primary_image": "https://images.pexels.com/photos/1126993/pexels-photo-1126993.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CHI-099-CAM-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CHI-099-CAM-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CHI-099-CAM-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CHI-099-CAM-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CHI-099-CAM-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CHI-099-ESP-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CHI-099-ESP-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CHI-099-ESP-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CHI-099-ESP-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CHI-099-ESP-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Selvedge Cotton Twill Casual Chinos",
        "slug": "selvedge-cotton-twill-casual-chinos-100",
        "description": "Durable casual pants crafted on vintage shuttle looms with visible red selvedge id along the outseam.",
        "category_slug": "chinos-casual-pants",
        "base_price": 8499.0,
        "discount_price": 7199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 59,
        "sales_count": 30,
        "primary_image": "https://images.pexels.com/photos/1040945/pexels-photo-1040945.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CHI-100-BUR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CHI-100-BUR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CHI-100-BUR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CHI-100-BUR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CHI-100-BUR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CHI-100-CLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CHI-100-CLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CHI-100-CLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CHI-100-CLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CHI-100-CLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Kuroki Mills 14oz Raw Vintage Selvedge Denim",
        "slug": "kuroki-mills-14oz-raw-vintage-selvedge-denim-101",
        "description": "Woven on Toyoda shuttle looms in Kojima, Japan. Pure indigo rope dye, custom solid brass hardware.",
        "category_slug": "selvedge-denim",
        "base_price": 11999.0,
        "discount_price": 9999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 15,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SEL-101-MID-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SEL-101-MID-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SEL-101-MID-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SEL-101-MID-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SEL-101-MID-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SEL-101-CHA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SEL-101-CHA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SEL-101-CHA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SEL-101-CHA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SEL-101-CHA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Nihon Menpu 15oz Indigo-Black Selvedge Jeans",
        "slug": "nihon-menpu-15oz-indigo-black-selvedge-jeans-102",
        "description": "Rigid raw denim featuring deep indigo warp and sulphur black weft for dramatic high-contrast fading.",
        "category_slug": "selvedge-denim",
        "base_price": 12499.0,
        "discount_price": 10499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 21,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1565084888279-aca607ecce0c?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SEL-102-FOR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SEL-102-FOR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SEL-102-FOR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SEL-102-FOR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SEL-102-FOR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SEL-102-SLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SEL-102-SLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SEL-102-SLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SEL-102-SLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SEL-102-SLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Kaihara Mills 13.5oz One-Wash Selvedge Denim",
        "slug": "kaihara-mills-13-5oz-one-wash-selvedge-denim-103",
        "description": "Sanforized Japanese selvedge denim pre-washed once for instant comfort while preserving raw texture.",
        "category_slug": "selvedge-denim",
        "base_price": 10999.0,
        "discount_price": 9299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 27,
        "sales_count": 33,
        "primary_image": "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SEL-103-OBS-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SEL-103-OBS-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SEL-103-OBS-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SEL-103-OBS-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SEL-103-OBS-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SEL-103-IVO-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SEL-103-IVO-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SEL-103-IVO-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SEL-103-IVO-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SEL-103-IVO-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Natural Indigo 16oz Heavyweight Selvedge Jeans",
        "slug": "natural-indigo-16oz-heavyweight-selvedge-jeans-104",
        "description": "Substantial shuttle-loomed denim hand-dyed with natural plant indigo, featuring raised belt loops.",
        "category_slug": "selvedge-denim",
        "base_price": 13999.0,
        "discount_price": 11799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 33,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1624378441864-6eda7eac51cb?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SEL-104-CAM-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SEL-104-CAM-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SEL-104-CAM-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SEL-104-CAM-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SEL-104-CAM-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SEL-104-ESP-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SEL-104-ESP-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SEL-104-ESP-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SEL-104-ESP-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SEL-104-ESP-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Left-Hand Twill 13oz Selvedge Denim",
        "slug": "left-hand-twill-13oz-selvedge-denim-105",
        "description": "Silky-smooth left-hand twill denim known for vintage fades and softer hand feel right out of the box.",
        "category_slug": "selvedge-denim",
        "base_price": 11499.0,
        "discount_price": 9699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 32,
        "sales_count": 35,
        "primary_image": "https://images.unsplash.com/photo-1640336437301-8368b53861ab?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SEL-105-BUR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SEL-105-BUR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SEL-105-BUR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SEL-105-BUR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SEL-105-BUR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SEL-105-CLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SEL-105-CLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SEL-105-CLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SEL-105-CLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SEL-105-CLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Slubby Nep Japanese Selvedge Denim Jeans",
        "slug": "slubby-nep-japanese-selvedge-denim-jeans-106",
        "description": "Textured rough-spun denim with visible white cotton neps throughout the weave for unique character.",
        "category_slug": "selvedge-denim",
        "base_price": 12999.0,
        "discount_price": 10999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 38,
        "sales_count": 36,
        "primary_image": "https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SEL-106-MID-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SEL-106-MID-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SEL-106-MID-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SEL-106-MID-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SEL-106-MID-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SEL-106-CHA-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SEL-106-CHA-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SEL-106-CHA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SEL-106-CHA-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SEL-106-CHA-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Organic Cotton 12.5oz Summer Selvedge Jeans",
        "slug": "organic-cotton-12-5oz-summer-selvedge-jeans-107",
        "description": "Lightweight Japanese selvedge denim woven from certified organic long-staple cotton.",
        "category_slug": "selvedge-denim",
        "base_price": 10499.0,
        "discount_price": 8799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 44,
        "sales_count": 37,
        "primary_image": "https://images.pexels.com/photos/1082528/pexels-photo-1082528.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SEL-107-FOR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SEL-107-FOR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SEL-107-FOR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SEL-107-FOR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SEL-107-FOR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SEL-107-SLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SEL-107-SLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SEL-107-SLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SEL-107-SLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SEL-107-SLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Type III Japanese Selvedge Denim Jacket",
        "slug": "type-iii-japanese-selvedge-denim-jacket-108",
        "description": "Classic trucker jacket tailored in 14.5oz raw Kuroki selvedge with custom donut buttons.",
        "category_slug": "selvedge-denim",
        "base_price": 14999.0,
        "discount_price": 12499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 50,
        "sales_count": 38,
        "primary_image": "https://images.pexels.com/photos/428340/pexels-photo-428340.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SEL-108-OBS-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SEL-108-OBS-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SEL-108-OBS-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SEL-108-OBS-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SEL-108-OBS-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SEL-108-IVO-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SEL-108-IVO-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SEL-108-IVO-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SEL-108-IVO-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SEL-108-IVO-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Relaxed Straight-Leg 1950s Cut Selvedge Denim",
        "slug": "relaxed-straight-leg-1950s-cut-selvedge-denim-109",
        "description": "High-rise vintage cut inspired by 1950s denim workwear, complete with hidden back pocket rivets.",
        "category_slug": "selvedge-denim",
        "base_price": 11999.0,
        "discount_price": 9999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 56,
        "sales_count": 39,
        "primary_image": "https://images.pexels.com/photos/52518/jeans-pants-blue-shop-52518.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SEL-109-CAM-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SEL-109-CAM-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SEL-109-CAM-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SEL-109-CAM-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SEL-109-CAM-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SEL-109-ESP-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SEL-109-ESP-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SEL-109-ESP-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SEL-109-ESP-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SEL-109-ESP-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Indigo x Indigo Double-Dyed Selvedge Denim",
        "slug": "indigo-x-indigo-double-dyed-selvedge-denim-110",
        "description": "Yarn-dyed indigo warp and weft creating a saturated midnight blue that fades to cobalt.",
        "category_slug": "selvedge-denim",
        "base_price": 13499.0,
        "discount_price": 11299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 62,
        "sales_count": 40,
        "primary_image": "https://images.pexels.com/photos/603022/pexels-photo-603022.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SEL-110-BUR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SEL-110-BUR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SEL-110-BUR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SEL-110-BUR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SEL-110-BUR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SEL-110-CLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SEL-110-CLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SEL-110-CLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SEL-110-CLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SEL-110-CLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Artisanal Washed Slim-Tapered Jeans",
        "slug": "artisanal-washed-slim-tapered-jeans-111",
        "description": "Hand-distressed washed denim in an authentic 3-year vintage wash with gentle whiskering and honeycombs.",
        "category_slug": "designer-jeans",
        "base_price": 8999.0,
        "discount_price": 7499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 18,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DES-111-MID-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DES-111-MID-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DES-111-MID-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DES-111-MID-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DES-111-MID-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DES-111-CHA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DES-111-CHA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DES-111-CHA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DES-111-CHA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DES-111-CHA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Relaxed Wide-Leg 90s Skate Denim",
        "slug": "relaxed-wide-leg-90s-skate-denim-112",
        "description": "Contemporary loose-fit jeans in washed light indigo with dropped waist and clean puddling hem.",
        "category_slug": "designer-jeans",
        "base_price": 7999.0,
        "discount_price": 6799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 17,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DES-112-FOR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DES-112-FOR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DES-112-FOR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DES-112-FOR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DES-112-FOR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DES-112-SLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DES-112-SLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DES-112-SLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DES-112-SLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DES-112-SLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Black Mineral-Washed Slim-Fit Jeans",
        "slug": "black-mineral-washed-slim-fit-jeans-113",
        "description": "Overdyed faded black denim with subtle sulfur wash, tonal stitching, and matte gunmetal rivets.",
        "category_slug": "designer-jeans",
        "base_price": 8499.0,
        "discount_price": 7199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 23,
        "sales_count": 43,
        "primary_image": "https://images.unsplash.com/photo-1619216910014-1fdb7a8e98e9?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DES-113-OBS-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DES-113-OBS-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DES-113-OBS-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DES-113-OBS-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DES-113-OBS-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DES-113-IVO-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DES-113-IVO-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DES-113-IVO-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DES-113-IVO-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DES-113-IVO-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Oversized Vintage-Washed Denim Chore Jacket",
        "slug": "oversized-vintage-washed-denim-chore-jacket-114",
        "description": "Utilitarian denim chore coat with contrast corduroy collar, four front pockets, and shank buttons.",
        "category_slug": "designer-jeans",
        "base_price": 11999.0,
        "discount_price": 9999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 29,
        "sales_count": 44,
        "primary_image": "https://images.pexels.com/photos/3760610/pexels-photo-3760610.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DES-114-CAM-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DES-114-CAM-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DES-114-CAM-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DES-114-CAM-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DES-114-CAM-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DES-114-ESP-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DES-114-ESP-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DES-114-ESP-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DES-114-ESP-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DES-114-ESP-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Raw Black Minimalist Stretch Denim",
        "slug": "raw-black-minimalist-stretch-denim-115",
        "description": "Clean modern 5-pocket jeans in deep pitch black with 2% elastane for shape retention and mobility.",
        "category_slug": "designer-jeans",
        "base_price": 7499.0,
        "discount_price": 6299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 35,
        "sales_count": 45,
        "primary_image": "https://images.pexels.com/photos/3760611/pexels-photo-3760611.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DES-115-BUR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DES-115-BUR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DES-115-BUR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DES-115-BUR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DES-115-BUR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DES-115-CLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DES-115-CLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DES-115-CLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DES-115-CLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DES-115-CLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Ecru Natural Undyed Cotton Denim Jeans",
        "slug": "ecru-natural-undyed-cotton-denim-jeans-116",
        "description": "Fresh summer denim crafted from unbleached natural cotton with speckled seeds and tonal thread.",
        "category_slug": "designer-jeans",
        "base_price": 8299.0,
        "discount_price": 6999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 41,
        "sales_count": 46,
        "primary_image": "https://images.pexels.com/photos/15728343/pexels-photo-15728343.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DES-116-MID-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DES-116-MID-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DES-116-MID-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DES-116-MID-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DES-116-MID-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DES-116-CHA-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DES-116-CHA-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DES-116-CHA-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DES-116-CHA-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DES-116-CHA-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Distressed Knee-Rip Skinny Tapered Jeans",
        "slug": "distressed-knee-rip-skinny-tapered-jeans-117",
        "description": "Editorial streetwear denim with hand-abraded rips, vintage knee wear, and tapered leg opening.",
        "category_slug": "designer-jeans",
        "base_price": 7899.0,
        "discount_price": 6599.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 47,
        "sales_count": 47,
        "primary_image": "https://images.pexels.com/photos/13816106/pexels-photo-13816106.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DES-117-FOR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DES-117-FOR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DES-117-FOR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DES-117-FOR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DES-117-FOR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DES-117-SLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DES-117-SLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DES-117-SLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DES-117-SLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DES-117-SLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Fleece-Lined Denim Trucker Jacket",
        "slug": "fleece-lined-denim-trucker-jacket-118",
        "description": "Classic denim jacket lined with warm faux-shearling fleece body and quilted sleeve lining.",
        "category_slug": "designer-jeans",
        "base_price": 12999.0,
        "discount_price": 10999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 53,
        "sales_count": 48,
        "primary_image": "https://images.pexels.com/photos/2363825/pexels-photo-2363825.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DES-118-OBS-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DES-118-OBS-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DES-118-OBS-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DES-118-OBS-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DES-118-OBS-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DES-118-IVO-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DES-118-IVO-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DES-118-IVO-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DES-118-IVO-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DES-118-IVO-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Bleached Stone-Washed 80s Straight Jeans",
        "slug": "bleached-stone-washed-80s-straight-jeans-119",
        "description": "Pale stone-washed denim with authentic marbling effect, high-rise waist, and brass hardware.",
        "category_slug": "designer-jeans",
        "base_price": 8199.0,
        "discount_price": 6899.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 52,
        "sales_count": 49,
        "primary_image": "https://images.pexels.com/photos/449977/pexels-photo-449977.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DES-119-CAM-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DES-119-CAM-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DES-119-CAM-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DES-119-CAM-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DES-119-CAM-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DES-119-ESP-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DES-119-ESP-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DES-119-ESP-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DES-119-ESP-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DES-119-ESP-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Denim Western Shirt with Pearl Snap Buttons",
        "slug": "denim-western-shirt-with-pearl-snap-buttons-120",
        "description": "Tailored 7oz indigo denim shirt featuring authentic western front yokes and snap closures.",
        "category_slug": "designer-jeans",
        "base_price": 7299.0,
        "discount_price": 6199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 58,
        "sales_count": 30,
        "primary_image": "https://images.pexels.com/photos/428338/pexels-photo-428338.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DES-120-BUR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DES-120-BUR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DES-120-BUR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DES-120-BUR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DES-120-BUR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DES-120-CLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DES-120-CLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DES-120-CLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DES-120-CLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DES-120-CLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Pure Mongolian Cashmere Pullover Hoodie",
        "slug": "pure-mongolian-cashmere-pullover-hoodie-121",
        "description": "Plush 2-ply pure cashmere hoodie featuring a double-layered hood, kangaroo pocket, and ribbed trims.",
        "category_slug": "cashmere-loungewear",
        "base_price": 13999.0,
        "discount_price": 11799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 14,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CAS-121-MID-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CAS-121-MID-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CAS-121-MID-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CAS-121-MID-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CAS-121-MID-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CAS-121-CHA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CAS-121-CHA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CAS-121-CHA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CAS-121-CHA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CAS-121-CHA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Matching Pure Cashmere Knit Sweatpants",
        "slug": "matching-pure-cashmere-knit-sweatpants-122",
        "description": "Tapered cashmere lounge pants with an elasticated drawstring waistband and rib-knit cuffs.",
        "category_slug": "cashmere-loungewear",
        "base_price": 12999.0,
        "discount_price": 10999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 20,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1609873814058-a8928924184a?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CAS-122-FOR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CAS-122-FOR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CAS-122-FOR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CAS-122-FOR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CAS-122-FOR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CAS-122-SLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CAS-122-SLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CAS-122-SLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CAS-122-SLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CAS-122-SLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Heavyweight 450GSM French Terry Sweatshirt",
        "slug": "heavyweight-450gsm-french-terry-sweatshirt-123",
        "description": "Ultra-dense combed cotton crewneck sweatshirt with ribbed side gussets and flatlock seams.",
        "category_slug": "cashmere-loungewear",
        "base_price": 6999.0,
        "discount_price": 5899.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 26,
        "sales_count": 33,
        "primary_image": "https://images.pexels.com/photos/3162769/pexels-photo-3162769.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CAS-123-OBS-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CAS-123-OBS-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CAS-123-OBS-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CAS-123-OBS-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CAS-123-OBS-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CAS-123-IVO-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CAS-123-IVO-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CAS-123-IVO-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CAS-123-IVO-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CAS-123-IVO-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Structured French Terry Lounge Joggers",
        "slug": "structured-french-terry-lounge-joggers-124",
        "description": "Premium sweatpants crafted from 450GSM loopback cotton with deep welt pockets and metal aglets.",
        "category_slug": "cashmere-loungewear",
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 32,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1550274191-c185b733bb9f?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CAS-124-CAM-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CAS-124-CAM-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CAS-124-CAM-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CAS-124-CAM-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CAS-124-CAM-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CAS-124-ESP-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CAS-124-ESP-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CAS-124-ESP-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CAS-124-ESP-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CAS-124-ESP-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cashmere-Cotton Blend Zip Lounge Hoodie",
        "slug": "cashmere-cotton-blend-zip-lounge-hoodie-125",
        "description": "Two-way zippered hoodie blending fine cotton and soft cashmere for all-day working-from-home comfort.",
        "category_slug": "cashmere-loungewear",
        "base_price": 9999.0,
        "discount_price": 8499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 38,
        "sales_count": 35,
        "primary_image": "https://images.unsplash.com/photo-1609803384069-19f3e5a70e75?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CAS-125-BUR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CAS-125-BUR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CAS-125-BUR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CAS-125-BUR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CAS-125-BUR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CAS-125-CLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CAS-125-CLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CAS-125-CLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CAS-125-CLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CAS-125-CLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Organic Waffle-Knit Thermal Lounge Set",
        "slug": "organic-waffle-knit-thermal-lounge-set-126",
        "description": "Two-piece cozy lounge set in organic waffle cotton including long-sleeve crew and cuffed pants.",
        "category_slug": "cashmere-loungewear",
        "base_price": 8499.0,
        "discount_price": 7199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 37,
        "sales_count": 36,
        "primary_image": "https://images.pexels.com/photos/7887199/pexels-photo-7887199.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CAS-126-MID-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CAS-126-MID-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CAS-126-MID-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CAS-126-MID-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-CAS-126-MID-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CAS-126-CHA-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CAS-126-CHA-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CAS-126-CHA-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CAS-126-CHA-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-CAS-126-CHA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Oversized Brushed-Back Cotton Fleece Hoodie",
        "slug": "oversized-brushed-back-cotton-fleece-hoodie-127",
        "description": "Substantial streetwear-proportioned hoodie with dropped shoulders and plush fleece interior.",
        "category_slug": "cashmere-loungewear",
        "base_price": 7499.0,
        "discount_price": 6299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 43,
        "sales_count": 37,
        "primary_image": "https://images.pexels.com/photos/1578997/pexels-photo-1578997.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CAS-127-FOR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CAS-127-FOR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CAS-127-FOR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CAS-127-FOR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-CAS-127-FOR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CAS-127-SLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CAS-127-SLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CAS-127-SLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CAS-127-SLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-CAS-127-SLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Silk-Cashmere Knit Lounge Trousers",
        "slug": "silk-cashmere-knit-lounge-trousers-128",
        "description": "Fluid wide-leg knit pants blending silk and cashmere for ultimate lightweight lounging.",
        "category_slug": "cashmere-loungewear",
        "base_price": 11499.0,
        "discount_price": 9699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 49,
        "sales_count": 38,
        "primary_image": "https://images.pexels.com/photos/2220315/pexels-photo-2220315.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CAS-128-OBS-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CAS-128-OBS-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CAS-128-OBS-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CAS-128-OBS-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-CAS-128-OBS-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CAS-128-IVO-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CAS-128-IVO-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CAS-128-IVO-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CAS-128-IVO-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-CAS-128-IVO-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Half-Zip French Terry Track Pullover",
        "slug": "half-zip-french-terry-track-pullover-129",
        "description": "Sleek athletic-luxe pullover with silver RiRi quarter-zipper, stand collar, and banded hem.",
        "category_slug": "cashmere-loungewear",
        "base_price": 6799.0,
        "discount_price": 5699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 55,
        "sales_count": 39,
        "primary_image": "https://images.pexels.com/photos/3775131/pexels-photo-3775131.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CAS-129-CAM-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CAS-129-CAM-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CAS-129-CAM-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CAS-129-CAM-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-CAS-129-CAM-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CAS-129-ESP-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CAS-129-ESP-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CAS-129-ESP-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CAS-129-ESP-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-CAS-129-ESP-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cashmere Robe-Cardigan Lounge Coat",
        "slug": "cashmere-robe-cardigan-lounge-coat-130",
        "description": "Open-front belted long cardigan knit in lofty cashmere to wrap up in sheer luxury at home.",
        "category_slug": "cashmere-loungewear",
        "base_price": 15999.0,
        "discount_price": 13499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 61,
        "sales_count": 40,
        "primary_image": "https://images.pexels.com/photos/2613260/pexels-photo-2613260.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CAS-130-BUR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CAS-130-BUR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CAS-130-BUR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CAS-130-BUR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-CAS-130-BUR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CAS-130-CLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CAS-130-CLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CAS-130-CLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CAS-130-CLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-CAS-130-CLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "22-Momme Mulberry Silk Pajama Set",
        "slug": "22-momme-mulberry-silk-pajama-set-131",
        "description": "Classic button-down pajama set featuring notch lapels, chest pocket, and mother-of-pearl buttons in pure silk.",
        "category_slug": "silk-sleepwear-robes",
        "base_price": 14999.0,
        "discount_price": 12499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 17,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SIL-131-MID-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SIL-131-MID-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SIL-131-MID-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SIL-131-MID-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SIL-131-MID-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SIL-131-CHA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SIL-131-CHA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SIL-131-CHA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SIL-131-CHA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SIL-131-CHA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Floor-Length Silk Charmeuse Kimono Robe",
        "slug": "floor-length-silk-charmeuse-kimono-robe-132",
        "description": "Dramatic belted kimono robe crafted from fluid 22-momme silk charmeuse with wide sleeves.",
        "category_slug": "silk-sleepwear-robes",
        "base_price": 16999.0,
        "discount_price": 13999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 23,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SIL-132-FOR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SIL-132-FOR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SIL-132-FOR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SIL-132-FOR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SIL-132-FOR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SIL-132-SLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SIL-132-SLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SIL-132-SLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SIL-132-SLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SIL-132-SLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Bias-Cut Mulberry Silk Sleep Slip",
        "slug": "bias-cut-mulberry-silk-sleep-slip-133",
        "description": "Sensuous nightgown with delicate adjustable straps, V-neckline, and French seam construction.",
        "category_slug": "silk-sleepwear-robes",
        "base_price": 8999.0,
        "discount_price": 7499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 22,
        "sales_count": 43,
        "primary_image": "https://images.pexels.com/photos/7782138/pexels-photo-7782138.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SIL-133-OBS-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SIL-133-OBS-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SIL-133-OBS-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SIL-133-OBS-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SIL-133-OBS-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SIL-133-IVO-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SIL-133-IVO-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SIL-133-IVO-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SIL-133-IVO-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SIL-133-IVO-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Silk Satin Camisole & Tap Shorts Set",
        "slug": "silk-satin-camisole-tap-shorts-set-134",
        "description": "Two-piece sleep set featuring a lace-trimmed silk cami and matching elastic-waist shorts.",
        "category_slug": "silk-sleepwear-robes",
        "base_price": 7999.0,
        "discount_price": 6799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 28,
        "sales_count": 44,
        "primary_image": "https://images.pexels.com/photos/1385472/pexels-photo-1385472.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SIL-134-CAM-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SIL-134-CAM-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SIL-134-CAM-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SIL-134-CAM-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SIL-134-CAM-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SIL-134-ESP-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SIL-134-ESP-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SIL-134-ESP-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SIL-134-ESP-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SIL-134-ESP-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Men's Silk Pajama Set with Contrast Piping",
        "slug": "men-s-silk-pajama-set-with-contrast-piping-135",
        "description": "Sartorial menswear sleep set in navy silk with crisp white piping and drawstring trousers.",
        "category_slug": "silk-sleepwear-robes",
        "base_price": 15499.0,
        "discount_price": 12999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 34,
        "sales_count": 45,
        "primary_image": "https://images.pexels.com/photos/10484488/pexels-photo-10484488.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SIL-135-BUR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SIL-135-BUR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SIL-135-BUR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SIL-135-BUR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SIL-135-BUR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SIL-135-CLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SIL-135-CLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SIL-135-CLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SIL-135-CLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SIL-135-CLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Lace-Trimmed Silk Robe in Rose Quartz",
        "slug": "lace-trimmed-silk-robe-in-rose-quartz-136",
        "description": "Romantic knee-length robe detailed with eyelash Chantilly lace along the cuffs and hem.",
        "category_slug": "silk-sleepwear-robes",
        "base_price": 13999.0,
        "discount_price": 11799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 40,
        "sales_count": 46,
        "primary_image": "https://images.pexels.com/photos/297933/pexels-photo-297933.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SIL-136-MID-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SIL-136-MID-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SIL-136-MID-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SIL-136-MID-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-SIL-136-MID-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SIL-136-CHA-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SIL-136-CHA-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SIL-136-CHA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SIL-136-CHA-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-SIL-136-CHA-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Long-Sleeve Silk Nightshirt in Champagne",
        "slug": "long-sleeve-silk-nightshirt-in-champagne-137",
        "description": "Relaxed menswear-inspired nightshirt tailored from washable silk with curved shirttail hem.",
        "category_slug": "silk-sleepwear-robes",
        "base_price": 9499.0,
        "discount_price": 7999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 46,
        "sales_count": 47,
        "primary_image": "https://images.pexels.com/photos/11830106/pexels-photo-11830106.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SIL-137-FOR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SIL-137-FOR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SIL-137-FOR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SIL-137-FOR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-SIL-137-FOR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SIL-137-SLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SIL-137-SLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SIL-137-SLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SIL-137-SLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-SIL-137-SLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Heavyweight 30-Momme Silk Velvet Smoking Robe",
        "slug": "heavyweight-30-momme-silk-velvet-smoking-robe-138",
        "description": "Lush silk-velvet lounging robe with quilted satin lapels, sash belt, and deep pockets.",
        "category_slug": "silk-sleepwear-robes",
        "base_price": 21999.0,
        "discount_price": 18499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 52,
        "sales_count": 48,
        "primary_image": "https://images.pexels.com/photos/1656684/pexels-photo-1656684.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SIL-138-OBS-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SIL-138-OBS-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SIL-138-OBS-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SIL-138-OBS-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-SIL-138-OBS-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SIL-138-IVO-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SIL-138-IVO-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SIL-138-IVO-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SIL-138-IVO-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-SIL-138-IVO-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Short Silk Robe with Belt",
        "slug": "short-silk-robe-with-belt-139",
        "description": "Everyday luxury wrap robe with internal tie and wide outer belt in timeless black silk.",
        "category_slug": "silk-sleepwear-robes",
        "base_price": 11999.0,
        "discount_price": 9999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 58,
        "sales_count": 49,
        "primary_image": "https://images.pexels.com/photos/4056723/pexels-photo-4056723.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SIL-139-CAM-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SIL-139-CAM-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SIL-139-CAM-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SIL-139-CAM-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-SIL-139-CAM-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SIL-139-ESP-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SIL-139-ESP-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SIL-139-ESP-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SIL-139-ESP-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-SIL-139-ESP-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Silk-Cotton Knit Thermal Sleepwear Set",
        "slug": "silk-cotton-knit-thermal-sleepwear-set-140",
        "description": "Ultra-breathable knit pajama set combining thermal cotton ribs with smooth silk fibers.",
        "category_slug": "silk-sleepwear-robes",
        "base_price": 8499.0,
        "discount_price": 7199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 57,
        "sales_count": 30,
        "primary_image": "https://images.pexels.com/photos/3823039/pexels-photo-3823039.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SIL-140-BUR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SIL-140-BUR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SIL-140-BUR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SIL-140-BUR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-SIL-140-BUR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SIL-140-CLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SIL-140-CLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SIL-140-CLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SIL-140-CLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-SIL-140-CLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Sculpting High-Waist Performance Leggings",
        "slug": "sculpting-high-waist-performance-leggings-141",
        "description": "Seamless four-way stretch compression tights with targeted core support and moisture-wicking technology.",
        "category_slug": "haute-activewear",
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 13,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1607914660217-754fdd90041d?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-HAU-141-MID-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-HAU-141-MID-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-HAU-141-MID-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-HAU-141-MID-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-HAU-141-MID-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-HAU-141-CHA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-HAU-141-CHA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-HAU-141-CHA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-HAU-141-CHA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-HAU-141-CHA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "AeroSpeed Compression Training Top",
        "slug": "aerospeed-compression-training-top-142",
        "description": "Aerodynamic compression shirt with laser-cut breathability zones and antimicrobial silver finish.",
        "category_slug": "haute-activewear",
        "base_price": 4999.0,
        "discount_price": 4199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 19,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-HAU-142-FOR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-HAU-142-FOR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-HAU-142-FOR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-HAU-142-FOR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-HAU-142-FOR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-HAU-142-SLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-HAU-142-SLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-HAU-142-SLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-HAU-142-SLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-HAU-142-SLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cross-Back Longline Sports Bra",
        "slug": "cross-back-longline-sports-bra-143",
        "description": "High-support sculpt bra featuring crossover back straps and removable breathable cups.",
        "category_slug": "haute-activewear",
        "base_price": 3999.0,
        "discount_price": 3399.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 25,
        "sales_count": 33,
        "primary_image": "https://images.unsplash.com/photo-1584166452535-40e62109c3f6?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-HAU-143-OBS-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-HAU-143-OBS-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-HAU-143-OBS-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-HAU-143-OBS-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-HAU-143-OBS-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-HAU-143-IVO-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-HAU-143-IVO-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-HAU-143-IVO-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-HAU-143-IVO-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-HAU-143-IVO-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Performance Quarter-Zip Thermal Pullover",
        "slug": "performance-quarter-zip-thermal-pullover-144",
        "description": "Brushed-interior thermal running pullover with thumbhole cuffs and hidden zip pocket.",
        "category_slug": "haute-activewear",
        "base_price": 5499.0,
        "discount_price": 4599.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 31,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-HAU-144-CAM-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-HAU-144-CAM-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-HAU-144-CAM-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-HAU-144-CAM-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-HAU-144-CAM-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-HAU-144-ESP-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-HAU-144-ESP-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-HAU-144-ESP-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-HAU-144-ESP-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-HAU-144-ESP-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Technical 2-in-1 Lined Training Shorts",
        "slug": "technical-2-in-1-lined-training-shorts-145",
        "description": "Lightweight four-way stretch shorts with built-in compression liner and bounce-free phone pocket.",
        "category_slug": "haute-activewear",
        "base_price": 4499.0,
        "discount_price": 3799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 37,
        "sales_count": 35,
        "primary_image": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-HAU-145-BUR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-HAU-145-BUR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-HAU-145-BUR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-HAU-145-BUR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-HAU-145-BUR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-HAU-145-CLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-HAU-145-CLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-HAU-145-CLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-HAU-145-CLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-HAU-145-CLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Seamless Ribbed Workout Bodysuit",
        "slug": "seamless-ribbed-workout-bodysuit-146",
        "description": "Form-fitting one-piece unitard designed for studio yoga, pilates, and functional training.",
        "category_slug": "haute-activewear",
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 43,
        "sales_count": 36,
        "primary_image": "https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-HAU-146-MID-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-HAU-146-MID-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-HAU-146-MID-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-HAU-146-MID-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-HAU-146-MID-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-HAU-146-CHA-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-HAU-146-CHA-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-HAU-146-CHA-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-HAU-146-CHA-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-HAU-146-CHA-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Water-Repellent Packable Windbreaker",
        "slug": "water-repellent-packable-windbreaker-147",
        "description": "Ultra-lightweight ripstop running jacket with reflective taping and packable pocket pouch.",
        "category_slug": "haute-activewear",
        "base_price": 6999.0,
        "discount_price": 5899.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 42,
        "sales_count": 37,
        "primary_image": "https://images.pexels.com/photos/3768916/pexels-photo-3768916.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-HAU-147-FOR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-HAU-147-FOR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-HAU-147-FOR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-HAU-147-FOR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-HAU-147-FOR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-HAU-147-SLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-HAU-147-SLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-HAU-147-SLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-HAU-147-SLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-HAU-147-SLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Ribbed Seamless Long-Sleeve Crop Top",
        "slug": "ribbed-seamless-long-sleeve-crop-top-148",
        "description": "Breathable crop top with engineered underbust support and thumbhole sleeves.",
        "category_slug": "haute-activewear",
        "base_price": 4299.0,
        "discount_price": 3599.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 48,
        "sales_count": 38,
        "primary_image": "https://images.pexels.com/photos/3757376/pexels-photo-3757376.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-HAU-148-OBS-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-HAU-148-OBS-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-HAU-148-OBS-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-HAU-148-OBS-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-HAU-148-OBS-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-HAU-148-IVO-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-HAU-148-IVO-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-HAU-148-IVO-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-HAU-148-IVO-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-HAU-148-IVO-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Lightweight Track Pants with Ankle Zips",
        "slug": "lightweight-track-pants-with-ankle-zips-149",
        "description": "Tapered technical woven track pants with water-resistant coating and zippered ankles.",
        "category_slug": "haute-activewear",
        "base_price": 5799.0,
        "discount_price": 4899.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 54,
        "sales_count": 39,
        "primary_image": "https://images.pexels.com/photos/4602025/pexels-photo-4602025.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-HAU-149-CAM-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-HAU-149-CAM-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-HAU-149-CAM-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-HAU-149-CAM-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-HAU-149-CAM-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-HAU-149-ESP-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-HAU-149-ESP-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-HAU-149-ESP-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-HAU-149-ESP-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-HAU-149-ESP-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Merino-Poly Hybrid Performance Tee",
        "slug": "merino-poly-hybrid-performance-tee-150",
        "description": "Naturally odor-resistant athletic t-shirt blending merino wool and quick-dry recycled poly.",
        "category_slug": "haute-activewear",
        "base_price": 3799.0,
        "discount_price": 3199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 60,
        "sales_count": 40,
        "primary_image": "https://images.pexels.com/photos/4056535/pexels-photo-4056535.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-HAU-150-BUR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-HAU-150-BUR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-HAU-150-BUR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-HAU-150-BUR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-HAU-150-BUR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-HAU-150-CLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-HAU-150-CLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-HAU-150-CLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-HAU-150-CLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-HAU-150-CLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "3-Layer GORE-TEX Storm-Proof Shell Jacket",
        "slug": "3-layer-gore-tex-storm-proof-shell-jacket-151",
        "description": "Fully taped three-layer membrane jacket featuring waterproof YKK Aquaguard zips and storm hood.",
        "category_slug": "technical-performance",
        "base_price": 17999.0,
        "discount_price": 14999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 16,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1516257984-b1b4d707412e?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TEC-151-MID-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TEC-151-MID-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TEC-151-MID-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TEC-151-MID-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TEC-151-MID-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TEC-151-CHA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TEC-151-CHA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TEC-151-CHA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TEC-151-CHA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TEC-151-CHA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Ultralight Packable Technical Windbreaker",
        "slug": "ultralight-packable-technical-windbreaker-152",
        "description": "Featherweight Japanese micro-ripstop windbreaker with DWR coating and articulated raglan sleeves.",
        "category_slug": "technical-performance",
        "base_price": 8999.0,
        "discount_price": 7499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 22,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1509041282410-ef44f92a193f?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TEC-152-FOR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TEC-152-FOR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TEC-152-FOR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TEC-152-FOR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TEC-152-FOR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TEC-152-SLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TEC-152-SLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TEC-152-SLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TEC-152-SLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TEC-152-SLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Modular Technical Utility Chest Vest",
        "slug": "modular-technical-utility-chest-vest-153",
        "description": "Weather-resistant tactical vest with Cordura reinforcement and quick-release Fidlock buckles.",
        "category_slug": "technical-performance",
        "base_price": 9999.0,
        "discount_price": 8499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 28,
        "sales_count": 43,
        "primary_image": "https://images.unsplash.com/photo-1542736619-c0911cb5eb12?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TEC-153-OBS-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TEC-153-OBS-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TEC-153-OBS-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TEC-153-OBS-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TEC-153-OBS-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TEC-153-IVO-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TEC-153-IVO-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TEC-153-IVO-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TEC-153-IVO-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TEC-153-IVO-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Bonded Softshell All-Weather Alpine Jacket",
        "slug": "bonded-softshell-all-weather-alpine-jacket-154",
        "description": "Fleece-backed stretch softshell jacket providing windproof protection and temperature regulation.",
        "category_slug": "technical-performance",
        "base_price": 12499.0,
        "discount_price": 10499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 27,
        "sales_count": 44,
        "primary_image": "https://images.pexels.com/photos/11124949/pexels-photo-11124949.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TEC-154-CAM-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TEC-154-CAM-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TEC-154-CAM-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TEC-154-CAM-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TEC-154-CAM-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TEC-154-ESP-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TEC-154-ESP-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TEC-154-ESP-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TEC-154-ESP-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TEC-154-ESP-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Waterproof Hooded Commuter Rain Anorak",
        "slug": "waterproof-hooded-commuter-rain-anorak-155",
        "description": "Half-zip pullover anorak with large kangaroo pocket and side zip for easy temperature venting.",
        "category_slug": "technical-performance",
        "base_price": 10999.0,
        "discount_price": 9199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 33,
        "sales_count": 45,
        "primary_image": "https://images.pexels.com/photos/8532616/pexels-photo-8532616.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TEC-155-BUR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TEC-155-BUR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TEC-155-BUR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TEC-155-BUR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TEC-155-BUR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TEC-155-CLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TEC-155-CLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TEC-155-CLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TEC-155-CLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TEC-155-CLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Technical Insulated Hybrid Mid-Layer Jacket",
        "slug": "technical-insulated-hybrid-mid-layer-jacket-156",
        "description": "Primaloft-insulated core jacket with breathable stretch fleece side panels for high activity.",
        "category_slug": "technical-performance",
        "base_price": 11499.0,
        "discount_price": 9699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 39,
        "sales_count": 46,
        "primary_image": "https://images.pexels.com/photos/6625914/pexels-photo-6625914.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TEC-156-MID-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TEC-156-MID-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TEC-156-MID-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TEC-156-MID-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-TEC-156-MID-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TEC-156-CHA-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TEC-156-CHA-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TEC-156-CHA-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TEC-156-CHA-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-TEC-156-CHA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Laser-Cut Taped Waterproof Rain Poncho",
        "slug": "laser-cut-taped-waterproof-rain-poncho-157",
        "description": "Architectural minimalist rain cape featuring welded seam construction and storm peak hood.",
        "category_slug": "technical-performance",
        "base_price": 13999.0,
        "discount_price": 11799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 45,
        "sales_count": 47,
        "primary_image": "https://images.pexels.com/photos/837140/pexels-photo-837140.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TEC-157-FOR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TEC-157-FOR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TEC-157-FOR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TEC-157-FOR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-TEC-157-FOR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TEC-157-SLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TEC-157-SLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TEC-157-SLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TEC-157-SLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-TEC-157-SLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cordura-Reinforced Technical Cargo Pants",
        "slug": "cordura-reinforced-technical-cargo-pants-158",
        "description": "Weatherproof technical pants with articulated knee darts and adjustable magnetic cuffs.",
        "category_slug": "technical-performance",
        "base_price": 9499.0,
        "discount_price": 7999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 51,
        "sales_count": 48,
        "primary_image": "https://images.pexels.com/photos/1687720/pexels-photo-1687720.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TEC-158-OBS-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TEC-158-OBS-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TEC-158-OBS-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TEC-158-OBS-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-TEC-158-OBS-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TEC-158-IVO-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TEC-158-IVO-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TEC-158-IVO-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TEC-158-IVO-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-TEC-158-IVO-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Storm-System Waterproof Shell Trench Coat",
        "slug": "storm-system-waterproof-shell-trench-coat-159",
        "description": "Tailored formal raincoat in technical 3-layer laminated fabric with clean concealed placket.",
        "category_slug": "technical-performance",
        "base_price": 15999.0,
        "discount_price": 13499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 57,
        "sales_count": 49,
        "primary_image": "https://images.pexels.com/photos/2905238/pexels-photo-2905238.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TEC-159-CAM-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TEC-159-CAM-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TEC-159-CAM-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TEC-159-CAM-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-TEC-159-CAM-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TEC-159-ESP-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TEC-159-ESP-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TEC-159-ESP-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TEC-159-ESP-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-TEC-159-ESP-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Reflective Technical Trail Shell",
        "slug": "reflective-technical-trail-shell-160",
        "description": "High-visibility technical running shell with 360-degree reflective print and waterproof zips.",
        "category_slug": "technical-performance",
        "base_price": 8499.0,
        "discount_price": 7199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 63,
        "sales_count": 30,
        "primary_image": "https://images.pexels.com/photos/4066289/pexels-photo-4066289.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TEC-160-BUR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TEC-160-BUR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TEC-160-BUR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TEC-160-BUR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-TEC-160-BUR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TEC-160-CLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TEC-160-CLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TEC-160-CLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TEC-160-CLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-TEC-160-CLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Signature Italian Lambskin Biker Jacket",
        "slug": "signature-italian-lambskin-biker-jacket-161",
        "description": "Asymmetric cafe biker jacket crafted from supple hand-waxed Italian lambskin with silver hardware.",
        "category_slug": "leather-suede-jackets",
        "base_price": 24999.0,
        "discount_price": 21499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 12,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-161-MID-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-161-MID-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-161-MID-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-161-MID-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-161-MID-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-161-CHA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-161-CHA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-161-CHA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-161-CHA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-161-CHA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Caf\u00e9 Racer Goat Suede Leather Jacket",
        "slug": "caf-racer-goat-suede-leather-jacket-162",
        "description": "Minimalist stand-collar racer jacket tailored in buttery-soft tobacco goat suede with cupro lining.",
        "category_slug": "leather-suede-jackets",
        "base_price": 22999.0,
        "discount_price": 19499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 18,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1487222477894-8943e31ef7b2?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-162-FOR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-162-FOR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-162-FOR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-162-FOR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-162-FOR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-162-SLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-162-SLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-162-SLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-162-SLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-162-SLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Shearling-Lined Aviator B-3 Flight Jacket",
        "slug": "shearling-lined-aviator-b-3-flight-jacket-163",
        "description": "Substantial sheepskin bomber jacket with thick shearling wool interior, twin buckle collar straps.",
        "category_slug": "leather-suede-jackets",
        "base_price": 27999.0,
        "discount_price": 23999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 24,
        "sales_count": 33,
        "primary_image": "https://images.unsplash.com/photo-1621827443067-daebb5331882?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-163-OBS-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-163-OBS-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-163-OBS-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-163-OBS-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-163-OBS-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-163-IVO-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-163-IVO-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-163-IVO-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-163-IVO-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-163-IVO-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Suede Trucker Jacket with Horn Buttons",
        "slug": "suede-trucker-jacket-with-horn-buttons-164",
        "description": "Iconic Type III silhouette reinterpreted in olive calf suede with tonal stitching and horn buttons.",
        "category_slug": "leather-suede-jackets",
        "base_price": 21499.0,
        "discount_price": 18299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 30,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1646799935652-c25cae07a720?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-164-CAM-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-164-CAM-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-164-CAM-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-164-CAM-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-164-CAM-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-164-ESP-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-164-ESP-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-164-ESP-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-164-ESP-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-164-ESP-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Double-Rider Leather Moto Jacket",
        "slug": "double-rider-leather-moto-jacket-165",
        "description": "Heavyweight vegetable-tanned steerhide motorcycle jacket with action back and nickel zippers.",
        "category_slug": "leather-suede-jackets",
        "base_price": 25999.0,
        "discount_price": 22499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 36,
        "sales_count": 35,
        "primary_image": "https://images.unsplash.com/photo-1792490728552-c35853ff78a1?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-165-BUR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-165-BUR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-165-BUR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-165-BUR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-165-BUR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-165-CLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-165-CLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-165-CLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-165-CLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-165-CLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Vintage Distressed Leather Bomber Jacket",
        "slug": "vintage-distressed-leather-bomber-jacket-166",
        "description": "Hand-patinated brown leather bomber with ribbed wool cuffs, hem, and antique brass zips.",
        "category_slug": "leather-suede-jackets",
        "base_price": 23499.0,
        "discount_price": 19999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 42,
        "sales_count": 36,
        "primary_image": "https://images.pexels.com/photos/7679720/pexels-photo-7679720.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-166-MID-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-166-MID-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-166-MID-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-166-MID-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-166-MID-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-166-CHA-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-166-CHA-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-166-CHA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-166-CHA-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-166-CHA-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Belted Suede Safari Over-Shirt Jacket",
        "slug": "belted-suede-safari-over-shirt-jacket-167",
        "description": "Casual sartorial jacket in sand suede with four front bellows pockets and a waist belt.",
        "category_slug": "leather-suede-jackets",
        "base_price": 19999.0,
        "discount_price": 16999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 48,
        "sales_count": 37,
        "primary_image": "https://images.pexels.com/photos/2085380/pexels-photo-2085380.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-167-FOR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-167-FOR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-167-FOR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-167-FOR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-167-FOR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-167-SLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-167-SLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-167-SLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-167-SLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-167-SLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Perforated Leather Summer Racer Jacket",
        "slug": "perforated-leather-summer-racer-jacket-168",
        "description": "Lightweight perforated lambskin jacket engineered for warm-weather rides and breathable style.",
        "category_slug": "leather-suede-jackets",
        "base_price": 20999.0,
        "discount_price": 17999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 47,
        "sales_count": 38,
        "primary_image": "https://images.pexels.com/photos/1926769/pexels-photo-1926769.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-168-OBS-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-168-OBS-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-168-OBS-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-168-OBS-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-168-OBS-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-168-IVO-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-168-IVO-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-168-IVO-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-168-IVO-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-168-IVO-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Leather Chore Coat with Contrast Collar",
        "slug": "leather-chore-coat-with-contrast-collar-169",
        "description": "Workwear-inspired chore coat in black full-grain leather with brown corduroy collar.",
        "category_slug": "leather-suede-jackets",
        "base_price": 22499.0,
        "discount_price": 18999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 53,
        "sales_count": 39,
        "primary_image": "https://images.pexels.com/photos/1381556/pexels-photo-1381556.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-169-CAM-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-169-CAM-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-169-CAM-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-169-CAM-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-169-CAM-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-169-ESP-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-169-ESP-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-169-ESP-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-169-ESP-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-169-ESP-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Hooded Leather Jacket with Removable Fleece",
        "slug": "hooded-leather-jacket-with-removable-fleece-170",
        "description": "Versatile urban leather jacket with a detachable zippered fleece inner hood and bib.",
        "category_slug": "leather-suede-jackets",
        "base_price": 21999.0,
        "discount_price": 18799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 59,
        "sales_count": 40,
        "primary_image": "https://images.pexels.com/photos/1040886/pexels-photo-1040886.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-170-BUR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-170-BUR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-170-BUR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-170-BUR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-170-BUR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-170-CLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-170-CLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-170-CLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-170-CLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-170-CLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "StormShield 750-Fill Down Expedition Parka",
        "slug": "stormshield-750-fill-down-expedition-parka-171",
        "description": "Substantial winter parka insulated with 750-fill power down, fleece-lined hand pockets, and fur-trimmed hood.",
        "category_slug": "parkas-puffers",
        "base_price": 19999.0,
        "discount_price": 16999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 15,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1547406683-690698712a08?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-PAR-171-MID-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-PAR-171-MID-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-PAR-171-MID-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-PAR-171-MID-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-PAR-171-MID-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-PAR-171-CHA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-PAR-171-CHA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-PAR-171-CHA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-PAR-171-CHA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-PAR-171-CHA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Diamond-Quilted Ultralight Down Bomber",
        "slug": "diamond-quilted-ultralight-down-bomber-172",
        "description": "Packable water-resistant nylon puffer jacket insulated with 800-fill down and knitted bomber collar.",
        "category_slug": "parkas-puffers",
        "base_price": 14499.0,
        "discount_price": 12499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 21,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1633075708071-14c4406ef497?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-PAR-172-FOR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-PAR-172-FOR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-PAR-172-FOR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-PAR-172-FOR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-PAR-172-FOR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-PAR-172-SLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-PAR-172-SLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-PAR-172-SLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-PAR-172-SLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-PAR-172-SLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Longline Down Puffer Coat with Funnel Collar",
        "slug": "longline-down-puffer-coat-with-funnel-collar-173",
        "description": "Full-length cocoon puffer coat with magnetic closures, interior backpack straps, and storm cuffs.",
        "category_slug": "parkas-puffers",
        "base_price": 18499.0,
        "discount_price": 15499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 27,
        "sales_count": 43,
        "primary_image": "https://images.unsplash.com/photo-1516647221-2087c5f12608?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-PAR-173-OBS-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-PAR-173-OBS-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-PAR-173-OBS-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-PAR-173-OBS-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-PAR-173-OBS-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-PAR-173-IVO-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-PAR-173-IVO-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-PAR-173-IVO-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-PAR-173-IVO-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-PAR-173-IVO-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Hooded Mountain Down Parka in Olive",
        "slug": "hooded-mountain-down-parka-in-olive-174",
        "description": "Rugged alpine parka featuring water-repellent ripstop shell, storm flap, and two-way zipper.",
        "category_slug": "parkas-puffers",
        "base_price": 17499.0,
        "discount_price": 14999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 33,
        "sales_count": 44,
        "primary_image": "https://images.unsplash.com/photo-1544012173-31786a75da48?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-PAR-174-CAM-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-PAR-174-CAM-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-PAR-174-CAM-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-PAR-174-CAM-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-PAR-174-CAM-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-PAR-174-ESP-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-PAR-174-ESP-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-PAR-174-ESP-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-PAR-174-ESP-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-PAR-174-ESP-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Seamless Channel-Quilted Down Jacket",
        "slug": "seamless-channel-quilted-down-jacket-175",
        "description": "Bonded seamless construction preventing down leakage and wind penetration in sleek obsidian black.",
        "category_slug": "parkas-puffers",
        "base_price": 15999.0,
        "discount_price": 13499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 32,
        "sales_count": 45,
        "primary_image": "https://images.unsplash.com/photo-1514976575739-7902e7066844?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-PAR-175-BUR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-PAR-175-BUR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-PAR-175-BUR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-PAR-175-BUR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-PAR-175-BUR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-PAR-175-CLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-PAR-175-CLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-PAR-175-CLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-PAR-175-CLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-PAR-175-CLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Waterproof Down-Filled Trench Mac Coat",
        "slug": "waterproof-down-filled-trench-mac-coat-176",
        "description": "Sartorial raincoat packed with concealed down insulation for clean warmth over business suits.",
        "category_slug": "parkas-puffers",
        "base_price": 18999.0,
        "discount_price": 15999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 38,
        "sales_count": 46,
        "primary_image": "https://images.unsplash.com/photo-1581813471657-c4d36c09d221?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-PAR-176-MID-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-PAR-176-MID-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-PAR-176-MID-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-PAR-176-MID-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-PAR-176-MID-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-PAR-176-CHA-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-PAR-176-CHA-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-PAR-176-CHA-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-PAR-176-CHA-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-PAR-176-CHA-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cropped Metallic High-Shine Puffer Jacket",
        "slug": "cropped-metallic-high-shine-puffer-jacket-177",
        "description": "Statement high-gloss lacquered puffer with dramatic stand collar and bungee hem cinch.",
        "category_slug": "parkas-puffers",
        "base_price": 13999.0,
        "discount_price": 11999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 44,
        "sales_count": 47,
        "primary_image": "https://images.unsplash.com/photo-1607708121955-e44b3dce5067?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-PAR-177-FOR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-PAR-177-FOR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-PAR-177-FOR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-PAR-177-FOR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-PAR-177-FOR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-PAR-177-SLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-PAR-177-SLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-PAR-177-SLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-PAR-177-SLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-PAR-177-SLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Fleece-Lined Storm Puffer Parka",
        "slug": "fleece-lined-storm-puffer-parka-178",
        "description": "Heavyweight weather-shield parka with plush sherpa fleece upper lining and waterproof zip chests.",
        "category_slug": "parkas-puffers",
        "base_price": 16499.0,
        "discount_price": 13999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 50,
        "sales_count": 48,
        "primary_image": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-PAR-178-OBS-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-PAR-178-OBS-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-PAR-178-OBS-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-PAR-178-OBS-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-PAR-178-OBS-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-PAR-178-IVO-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-PAR-178-IVO-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-PAR-178-IVO-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-PAR-178-IVO-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-PAR-178-IVO-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Lightweight Packable Down Gilet Vest",
        "slug": "lightweight-packable-down-gilet-vest-179",
        "description": "Sleeveless down puffer vest ideal for layering under tailored overcoats and blazers.",
        "category_slug": "parkas-puffers",
        "base_price": 9999.0,
        "discount_price": 8499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 56,
        "sales_count": 49,
        "primary_image": "https://images.unsplash.com/photo-1548883354-7622d03aca27?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-PAR-179-CAM-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-PAR-179-CAM-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-PAR-179-CAM-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-PAR-179-CAM-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-PAR-179-CAM-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-PAR-179-ESP-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-PAR-179-ESP-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-PAR-179-ESP-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-PAR-179-ESP-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-PAR-179-ESP-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Arctic Explorer Fur-Trimmed Down Coat",
        "slug": "arctic-explorer-fur-trimmed-down-coat-180",
        "description": "Heavy-duty cold-weather coat tested for sub-zero temperatures with internal storm skirt.",
        "category_slug": "parkas-puffers",
        "base_price": 22999.0,
        "discount_price": 19499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 62,
        "sales_count": 30,
        "primary_image": "https://images.pexels.com/photos/6311392/pexels-photo-6311392.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-PAR-180-BUR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-PAR-180-BUR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-PAR-180-BUR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-PAR-180-BUR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-PAR-180-BUR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-PAR-180-CLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-PAR-180-CLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-PAR-180-CLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-PAR-180-CLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-PAR-180-CLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Normandy Flax Pure Linen Button-Down Shirt",
        "slug": "normandy-flax-pure-linen-button-down-shirt-181",
        "description": "Airy relaxed shirt tailored from 100% French Normandy flax with a soft camp collar and shell buttons.",
        "category_slug": "linen-shirts",
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 18,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1578932750294-f5075e85f44a?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-181-MID-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-181-MID-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-181-MID-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-181-MID-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-181-MID-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-181-CHA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-181-CHA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-181-CHA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-181-CHA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-181-CHA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Band-Collar Linen Popover Vacation Shirt",
        "slug": "band-collar-linen-popover-vacation-shirt-182",
        "description": "Minimalist grandad-collar popover shirt with a three-button placket and rolled button-tab sleeves.",
        "category_slug": "linen-shirts",
        "base_price": 5499.0,
        "discount_price": 4599.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 17,
        "sales_count": 32,
        "primary_image": "https://images.pexels.com/photos/10484489/pexels-photo-10484489.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-182-FOR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-182-FOR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-182-FOR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-182-FOR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-182-FOR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-182-SLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-182-SLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-182-SLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-182-SLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-182-SLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Garment-Washed White Linen Beach Shirt",
        "slug": "garment-washed-white-linen-beach-shirt-183",
        "description": "Pre-washed for effortless crinkle texture, this breathable white shirt is the ultimate resort staple.",
        "category_slug": "linen-shirts",
        "base_price": 5799.0,
        "discount_price": 4799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 23,
        "sales_count": 33,
        "primary_image": "https://images.pexels.com/photos/10484490/pexels-photo-10484490.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-183-OBS-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-183-OBS-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-183-OBS-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-183-OBS-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-183-OBS-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-183-IVO-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-183-IVO-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-183-IVO-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-183-IVO-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-183-IVO-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Striped Coastal Linen Camp-Collar Shirt",
        "slug": "striped-coastal-linen-camp-collar-shirt-184",
        "description": "Vintage-inspired navy and cream vertical stripe linen shirt with straight hem and side slits.",
        "category_slug": "linen-shirts",
        "base_price": 6299.0,
        "discount_price": 5299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 29,
        "sales_count": 34,
        "primary_image": "https://images.pexels.com/photos/11830107/pexels-photo-11830107.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-184-CAM-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-184-CAM-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-184-CAM-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-184-CAM-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-184-CAM-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-184-ESP-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-184-ESP-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-184-ESP-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-184-ESP-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-184-ESP-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Oversized Boyfriend Linen Shirt",
        "slug": "oversized-boyfriend-linen-shirt-185",
        "description": "Slouchy relaxed linen shirt for women with dropped shoulders and elongated cuffs.",
        "category_slug": "linen-shirts",
        "base_price": 5699.0,
        "discount_price": 4799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 35,
        "sales_count": 35,
        "primary_image": "https://images.pexels.com/photos/1656685/pexels-photo-1656685.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-185-BUR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-185-BUR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-185-BUR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-185-BUR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-185-BUR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-185-CLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-185-CLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-185-CLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-185-CLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-185-CLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cuban-Collar Linen Resort Shirt in Olive",
        "slug": "cuban-collar-linen-resort-shirt-in-olive-186",
        "description": "Open-neck holiday shirt in garment-dyed olive green linen with chest patch pocket.",
        "category_slug": "linen-shirts",
        "base_price": 5899.0,
        "discount_price": 4899.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 41,
        "sales_count": 36,
        "primary_image": "https://images.pexels.com/photos/1300550/pexels-photo-1300550.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-186-MID-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-186-MID-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-186-MID-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-186-MID-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-186-MID-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-186-CHA-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-186-CHA-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-186-CHA-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-186-CHA-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-186-CHA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Longline Linen Tunic with Side Slits",
        "slug": "longline-linen-tunic-with-side-slits-187",
        "description": "Modern breezy tunic top cut from pure flax linen with a deep V-neckline and relaxed fit.",
        "category_slug": "linen-shirts",
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 47,
        "sales_count": 37,
        "primary_image": "https://images.pexels.com/photos/934063/pexels-photo-934063.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-187-FOR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-187-FOR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-187-FOR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-187-FOR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-187-FOR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-187-SLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-187-SLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-187-SLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-187-SLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-187-SLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Chambray Linen Casual Button-Down",
        "slug": "chambray-linen-casual-button-down-188",
        "description": "Woven with white and sky-blue yarns for a nuanced chambray finish in pure breathable linen.",
        "category_slug": "linen-shirts",
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 53,
        "sales_count": 38,
        "primary_image": "https://images.pexels.com/photos/934070/pexels-photo-934070.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-188-OBS-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-188-OBS-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-188-OBS-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-188-OBS-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-188-OBS-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-188-IVO-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-188-IVO-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-188-IVO-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-188-IVO-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-188-IVO-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Short-Sleeve Safari Linen Utility Shirt",
        "slug": "short-sleeve-safari-linen-utility-shirt-189",
        "description": "Double-pocket safari shirt in khaki linen with horn buttons and epaulette shoulder details.",
        "category_slug": "linen-shirts",
        "base_price": 5299.0,
        "discount_price": 4399.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 52,
        "sales_count": 39,
        "primary_image": "https://images.pexels.com/photos/2235071/pexels-photo-2235071.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-189-CAM-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-189-CAM-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-189-CAM-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-189-CAM-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-189-CAM-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-189-ESP-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-189-ESP-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-189-ESP-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-189-ESP-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-189-ESP-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Embroidered Bohemian Linen Blouse",
        "slug": "embroidered-bohemian-linen-blouse-190",
        "description": "Artisanal linen top featuring delicate tonal embroidery along the neckline and balloon sleeves.",
        "category_slug": "linen-shirts",
        "base_price": 6799.0,
        "discount_price": 5699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 58,
        "sales_count": 40,
        "primary_image": "https://images.pexels.com/photos/1755428/pexels-photo-1755428.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-190-BUR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-190-BUR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-190-BUR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-190-BUR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-190-BUR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-190-CLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-190-CLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-190-CLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-190-CLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-190-CLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Relaxed Drawstring Linen Beach Trousers",
        "slug": "relaxed-drawstring-linen-beach-trousers-191",
        "description": "Breezy wide-leg trousers tailored from 100% French linen with an elasticated drawcord waist.",
        "category_slug": "linen-resortwear",
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 14,
        "sales_count": 41,
        "primary_image": "https://images.pexels.com/photos/19090/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-191-MID-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-191-MID-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-191-MID-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-191-MID-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-191-MID-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-191-CHA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-191-CHA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-191-CHA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-191-CHA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-191-CHA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Tailored Pleated Linen-Cotton Trousers",
        "slug": "tailored-pleated-linen-cotton-trousers-192",
        "description": "Sartorial summer trousers with double front pleats and side tabs, woven in a crisp linen-cotton blend.",
        "category_slug": "linen-resortwear",
        "base_price": 7499.0,
        "discount_price": 6299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 20,
        "sales_count": 42,
        "primary_image": "https://images.pexels.com/photos/298863/pexels-photo-298863.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-192-FOR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-192-FOR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-192-FOR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-192-FOR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-192-FOR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-192-SLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-192-SLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-192-SLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-192-SLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-192-SLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Drawstring Linen Resort Shorts",
        "slug": "drawstring-linen-resort-shorts-193",
        "description": "Casual warm-weather shorts with internal cotton drawcord, mesh-lined pockets, and 7-inch inseam.",
        "category_slug": "linen-resortwear",
        "base_price": 4499.0,
        "discount_price": 3799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 26,
        "sales_count": 43,
        "primary_image": "https://images.pexels.com/photos/298864/pexels-photo-298864.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-193-OBS-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-193-OBS-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-193-OBS-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-193-OBS-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-193-OBS-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-193-IVO-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-193-IVO-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-193-IVO-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-193-IVO-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-193-IVO-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Wide-Leg High-Rise Women's Linen Pants",
        "slug": "wide-leg-high-rise-women-s-linen-pants-194",
        "description": "Flowing palazzo trousers cut from premium washed linen with deep side pockets and clean waistband.",
        "category_slug": "linen-resortwear",
        "base_price": 6999.0,
        "discount_price": 5899.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 32,
        "sales_count": 44,
        "primary_image": "https://images.pexels.com/photos/3760612/pexels-photo-3760612.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-194-CAM-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-194-CAM-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-194-CAM-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-194-CAM-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-194-CAM-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-194-ESP-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-194-ESP-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-194-ESP-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-194-ESP-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-194-ESP-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cropped Tapered Linen Easy Pants",
        "slug": "cropped-tapered-linen-easy-pants-195",
        "description": "Japanese-inspired relaxed crop trousers with elastic waist and single pleat detailing in sand.",
        "category_slug": "linen-resortwear",
        "base_price": 6299.0,
        "discount_price": 5299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 38,
        "sales_count": 45,
        "primary_image": "https://images.pexels.com/photos/3760613/pexels-photo-3760613.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-195-BUR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-195-BUR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-195-BUR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-195-BUR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-195-BUR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-195-CLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-195-CLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-195-CLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-195-CLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-195-CLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Gurkha-Style Linen Belted Shorts",
        "slug": "gurkha-style-linen-belted-shorts-196",
        "description": "High-rise tailored shorts featuring double buckled waist straps and deep front pleats.",
        "category_slug": "linen-resortwear",
        "base_price": 5299.0,
        "discount_price": 4399.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 37,
        "sales_count": 46,
        "primary_image": "https://images.pexels.com/photos/1478442/pexels-photo-1478442.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-196-MID-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-196-MID-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-196-MID-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-196-MID-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LIN-196-MID-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-196-CHA-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-196-CHA-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-196-CHA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-196-CHA-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LIN-196-CHA-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Striped Seersucker-Linen Lounge Pants",
        "slug": "striped-seersucker-linen-lounge-pants-197",
        "description": "Textured seersucker linen pants with nautical stripes and relaxed beachside drape.",
        "category_slug": "linen-resortwear",
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 43,
        "sales_count": 47,
        "primary_image": "https://images.pexels.com/photos/1537492/pexels-photo-1537492.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-197-FOR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-197-FOR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-197-FOR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-197-FOR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LIN-197-FOR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-197-SLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-197-SLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-197-SLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-197-SLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LIN-197-SLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Tailored Linen Suit Trousers in Tobacco",
        "slug": "tailored-linen-suit-trousers-in-tobacco-198",
        "description": "Sharp summer formal trousers designed to pair with matching sport coats for garden weddings.",
        "category_slug": "linen-resortwear",
        "base_price": 7999.0,
        "discount_price": 6799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 49,
        "sales_count": 48,
        "primary_image": "https://images.pexels.com/photos/1082529/pexels-photo-1082529.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-198-OBS-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-198-OBS-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-198-OBS-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-198-OBS-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LIN-198-OBS-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-198-IVO-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-198-IVO-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-198-IVO-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-198-IVO-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LIN-198-IVO-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Linen Bermuda Shorts with Turn-Up Hems",
        "slug": "linen-bermuda-shorts-with-turn-up-hems-199",
        "description": "Knee-length structured linen shorts with cuffed hems and rear button welt pockets.",
        "category_slug": "linen-resortwear",
        "base_price": 4999.0,
        "discount_price": 4199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 55,
        "sales_count": 49,
        "primary_image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-199-CAM-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-199-CAM-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-199-CAM-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-199-CAM-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LIN-199-CAM-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-199-ESP-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-199-ESP-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-199-ESP-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-199-ESP-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LIN-199-ESP-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Linen-Tencel Fluid Lounge Joggers",
        "slug": "linen-tencel-fluid-lounge-joggers-200",
        "description": "Silky-soft relaxed resort joggers combining the breathability of linen with the drape of Tencel.",
        "category_slug": "linen-resortwear",
        "base_price": 6799.0,
        "discount_price": 5699.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 61,
        "sales_count": 30,
        "primary_image": "https://images.pexels.com/photos/1346187/pexels-photo-1346187.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-200-BUR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-200-BUR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-200-BUR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-200-BUR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LIN-200-BUR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-200-CLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-200-CLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-200-CLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-200-CLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LIN-200-CLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Goodyear-Welted Tuscan Calfskin Chelsea Boots",
        "slug": "goodyear-welted-tuscan-calfskin-chelsea-boots-201",
        "description": "Handcrafted in Florence using full-grain Italian box calf, elastic gussets, and leather sole.",
        "category_slug": "leather-boots",
        "base_price": 17999.0,
        "discount_price": 14999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 17,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1628193104037-3590917fb66e?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-201-MID-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-201-MID-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-201-MID-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-201-MID-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-201-MID-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-201-CHA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-201-CHA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-201-CHA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-201-CHA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-201-CHA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Roughout Waxed Suede Combat Boots",
        "slug": "roughout-waxed-suede-combat-boots-202",
        "description": "Rugged military boots crafted from heavyweight waterproof roughout suede with Vibram lug soles.",
        "category_slug": "leather-boots",
        "base_price": 16999.0,
        "discount_price": 13999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 23,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1625435617897-ae39fec53c35?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-202-FOR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-202-FOR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-202-FOR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-202-FOR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-202-FOR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-202-SLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-202-SLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-202-SLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-202-SLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-202-SLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Hand-Burnished Leather Brogue Boots",
        "slug": "hand-burnished-leather-brogue-boots-203",
        "description": "Wingtip lace-up boots featuring intricate perforations, storm welt, and hand-rubbed chestnut patina.",
        "category_slug": "leather-boots",
        "base_price": 18499.0,
        "discount_price": 15499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 22,
        "sales_count": 33,
        "primary_image": "https://images.unsplash.com/photo-1608256301056-3806c4970e64?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-203-OBS-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-203-OBS-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-203-OBS-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-203-OBS-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-203-OBS-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-203-IVO-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-203-IVO-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-203-IVO-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-203-IVO-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-203-IVO-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Snuff Suede Chelsea Boots with Crepe Sole",
        "slug": "snuff-suede-chelsea-boots-with-crepe-sole-204",
        "description": "Classic casual Chelsea boots in velvety snuff suede with natural plantation crepe soles.",
        "category_slug": "leather-boots",
        "base_price": 15499.0,
        "discount_price": 12999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 28,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1610888941359-d33e2cda5bb3?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-204-CAM-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-204-CAM-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-204-CAM-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-204-CAM-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-204-CAM-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-204-ESP-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-204-ESP-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-204-ESP-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-204-ESP-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-204-ESP-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cap-Toe Service Boots in Horween Chromexcel",
        "slug": "cap-toe-service-boots-in-horween-chromexcel-205",
        "description": "Iconic work-dress boot crafted from Chicago Horween Chromexcel leather with Dainite studded soles.",
        "category_slug": "leather-boots",
        "base_price": 19999.0,
        "discount_price": 16999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 34,
        "sales_count": 35,
        "primary_image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-205-BUR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-205-BUR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-205-BUR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-205-BUR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-205-BUR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-205-CLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-205-CLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-205-CLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-205-CLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-205-CLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Side-Zip Leather Harness Boots",
        "slug": "side-zip-leather-harness-boots-206",
        "description": "Rock-and-roll inspired sleek ankle boots with antique brass harness ring and side zipper.",
        "category_slug": "leather-boots",
        "base_price": 16499.0,
        "discount_price": 13999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 40,
        "sales_count": 36,
        "primary_image": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-206-MID-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-206-MID-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-206-MID-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-206-MID-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-206-MID-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-206-CHA-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-206-CHA-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-206-CHA-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-206-CHA-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-206-CHA-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Norwegian-Welted Mountain Hiking Boots",
        "slug": "norwegian-welted-mountain-hiking-boots-207",
        "description": "Heavy-duty heritage hiking boots with Norwegian storm welt, padded leather collar, and red laces.",
        "category_slug": "leather-boots",
        "base_price": 18999.0,
        "discount_price": 15999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 46,
        "sales_count": 37,
        "primary_image": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-207-FOR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-207-FOR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-207-FOR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-207-FOR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-207-FOR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-207-SLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-207-SLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-207-SLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-207-SLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-207-SLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Knee-High Slouchy Suede Riding Boots",
        "slug": "knee-high-slouchy-suede-riding-boots-208",
        "description": "Sophisticated women's tall boots in buttery chocolate suede with low stacked leather heel.",
        "category_slug": "leather-boots",
        "base_price": 21499.0,
        "discount_price": 17999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 52,
        "sales_count": 38,
        "primary_image": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-208-OBS-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-208-OBS-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-208-OBS-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-208-OBS-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-208-OBS-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-208-IVO-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-208-IVO-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-208-IVO-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-208-IVO-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-208-IVO-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Chukka Desert Boots in Kudu Antelope Suede",
        "slug": "chukka-desert-boots-in-kudu-antelope-suede-209",
        "description": "Supple unlined desert boots made from African kudu reverse suede with brass eyelets.",
        "category_slug": "leather-boots",
        "base_price": 14999.0,
        "discount_price": 12499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 58,
        "sales_count": 39,
        "primary_image": "https://images.pexels.com/photos/267301/pexels-photo-267301.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-209-CAM-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-209-CAM-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-209-CAM-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-209-CAM-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-209-CAM-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-209-ESP-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-209-ESP-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-209-ESP-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-209-ESP-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-209-ESP-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Black Leather Moto Engineer Boots",
        "slug": "black-leather-moto-engineer-boots-210",
        "description": "Heavyweight pull-up leather boots with nickel roller buckles and oil-resistant Goodyear welt.",
        "category_slug": "leather-boots",
        "base_price": 17499.0,
        "discount_price": 14499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 57,
        "sales_count": 40,
        "primary_image": "https://images.pexels.com/photos/1464625/pexels-photo-1464625.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-210-BUR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-210-BUR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-210-BUR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-210-BUR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-210-BUR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-210-CLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-210-CLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-210-CLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-210-CLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-210-CLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Blake-Stitched Italian Penny Loafers",
        "slug": "blake-stitched-italian-penny-loafers-211",
        "description": "Timeless slip-on shoes handcrafted from French calfskin with hand-sewn apron and leather soles.",
        "category_slug": "dress-shoes-loafers",
        "base_price": 14999.0,
        "discount_price": 12499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 13,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1490114538077-0a7f8cb49891?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DRE-211-MID-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DRE-211-MID-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DRE-211-MID-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DRE-211-MID-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DRE-211-MID-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DRE-211-CHA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DRE-211-CHA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DRE-211-CHA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DRE-211-CHA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DRE-211-CHA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Hand-Patinated Wholecut Oxford Shoes",
        "slug": "hand-patinated-wholecut-oxford-shoes-212",
        "description": "Masterpiece formal dress shoes cut from a single flawless piece of calfskin with museum patina.",
        "category_slug": "dress-shoes-loafers",
        "base_price": 17999.0,
        "discount_price": 14999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 19,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1616663308968-58162d332720?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DRE-212-FOR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DRE-212-FOR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DRE-212-FOR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DRE-212-FOR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DRE-212-FOR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DRE-212-SLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DRE-212-SLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DRE-212-SLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DRE-212-SLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DRE-212-SLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Double Monk-Strap Dress Shoes in Cognac",
        "slug": "double-monk-strap-dress-shoes-in-cognac-213",
        "description": "Sartorial cap-toe monk straps with twin palladium buckles and hand-beveled waist soles.",
        "category_slug": "dress-shoes-loafers",
        "base_price": 15999.0,
        "discount_price": 13499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 25,
        "sales_count": 43,
        "primary_image": "https://images.unsplash.com/photo-1621665422129-a03cc387bc7d?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DRE-213-OBS-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DRE-213-OBS-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DRE-213-OBS-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DRE-213-OBS-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DRE-213-OBS-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DRE-213-IVO-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DRE-213-IVO-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DRE-213-IVO-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DRE-213-IVO-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DRE-213-IVO-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Horsebit Loafers with Antique Brass Buckle",
        "slug": "horsebit-loafers-with-antique-brass-buckle-214",
        "description": "Equestrian-inspired loafers in soft calfskin with iconic brass horsebit hardware.",
        "category_slug": "dress-shoes-loafers",
        "base_price": 15499.0,
        "discount_price": 12999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 31,
        "sales_count": 44,
        "primary_image": "https://images.unsplash.com/photo-1443130128240-22fb98ca70a4?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DRE-214-CAM-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DRE-214-CAM-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DRE-214-CAM-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DRE-214-CAM-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DRE-214-CAM-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DRE-214-ESP-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DRE-214-ESP-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DRE-214-ESP-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DRE-214-ESP-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DRE-214-ESP-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Quarter-Brogue Oxford Shoes in Espresso",
        "slug": "quarter-brogue-oxford-shoes-in-espresso-215",
        "description": "Refined business lace-ups with delicate toe perforations and Goodyear welted sole.",
        "category_slug": "dress-shoes-loafers",
        "base_price": 16499.0,
        "discount_price": 13999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 37,
        "sales_count": 45,
        "primary_image": "https://images.unsplash.com/photo-1614253429340-98120bd6d753?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DRE-215-BUR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DRE-215-BUR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DRE-215-BUR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DRE-215-BUR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DRE-215-BUR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DRE-215-CLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DRE-215-CLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DRE-215-CLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DRE-215-CLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DRE-215-CLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Tassel Loafers in Snuff Calf Suede",
        "slug": "tassel-loafers-in-snuff-calf-suede-216",
        "description": "Hand-stitched apron loafers featuring decorative leather tassels and leather insole.",
        "category_slug": "dress-shoes-loafers",
        "base_price": 14499.0,
        "discount_price": 12199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 43,
        "sales_count": 46,
        "primary_image": "https://images.unsplash.com/photo-1668069226492-508742b03147?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DRE-216-MID-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DRE-216-MID-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DRE-216-MID-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DRE-216-MID-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-DRE-216-MID-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DRE-216-CHA-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DRE-216-CHA-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DRE-216-CHA-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DRE-216-CHA-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-DRE-216-CHA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Patent Leather Black-Tie Tuxedo Shoes",
        "slug": "patent-leather-black-tie-tuxedo-shoes-217",
        "description": "High-gloss mirror patent leather plain-toe oxfords designed for black-tie formal events.",
        "category_slug": "dress-shoes-loafers",
        "base_price": 16999.0,
        "discount_price": 14299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 42,
        "sales_count": 47,
        "primary_image": "https://images.unsplash.com/photo-1616406432452-07bc5938759d?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DRE-217-FOR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DRE-217-FOR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DRE-217-FOR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DRE-217-FOR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-DRE-217-FOR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DRE-217-SLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DRE-217-SLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DRE-217-SLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DRE-217-SLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-DRE-217-SLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Belgian Loafers with Accent Bow in Suede",
        "slug": "belgian-loafers-with-accent-bow-in-suede-218",
        "description": "Sleek low-profile slipper loafers with leather piping and miniature top bow.",
        "category_slug": "dress-shoes-loafers",
        "base_price": 13999.0,
        "discount_price": 11799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 48,
        "sales_count": 48,
        "primary_image": "https://images.unsplash.com/photo-1511283402428-355853756676?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DRE-218-OBS-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DRE-218-OBS-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DRE-218-OBS-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DRE-218-OBS-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-DRE-218-OBS-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DRE-218-IVO-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DRE-218-IVO-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DRE-218-IVO-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DRE-218-IVO-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-DRE-218-IVO-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Derby Blucher Shoes in Scotch Grain Leather",
        "slug": "derby-blucher-shoes-in-scotch-grain-leather-219",
        "description": "Robust pebble-grain derby shoes featuring double water-resistant leather soles.",
        "category_slug": "dress-shoes-loafers",
        "base_price": 15299.0,
        "discount_price": 12799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 54,
        "sales_count": 49,
        "primary_image": "https://images.pexels.com/photos/1456706/pexels-photo-1456706.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DRE-219-CAM-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DRE-219-CAM-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DRE-219-CAM-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DRE-219-CAM-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-DRE-219-CAM-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DRE-219-ESP-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DRE-219-ESP-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DRE-219-ESP-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DRE-219-ESP-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-DRE-219-ESP-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Woven Leather Summer Slip-On Shoes",
        "slug": "woven-leather-summer-slip-on-shoes-220",
        "description": "Artisanal woven calfskin loafers providing maximum ventilation for hot-weather formal elegance.",
        "category_slug": "dress-shoes-loafers",
        "base_price": 14799.0,
        "discount_price": 12399.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 60,
        "sales_count": 30,
        "primary_image": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DRE-220-BUR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DRE-220-BUR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DRE-220-BUR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DRE-220-BUR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-DRE-220-BUR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DRE-220-CLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DRE-220-CLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DRE-220-CLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DRE-220-CLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-DRE-220-CLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Full-Grain Leather Weekender Duffel Bag",
        "slug": "full-grain-leather-weekender-duffel-bag-221",
        "description": "Heritage travel bag crafted from vegetable-tanned Italian leather with brass hardware and strap.",
        "category_slug": "leather-bags-luggage",
        "base_price": 19999.0,
        "discount_price": 16999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 16,
        "sales_count": 31,
        "primary_image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-221-MID-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-221-MID-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-221-MID-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-221-MID-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-221-MID-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-221-CHA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-221-CHA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-221-CHA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-221-CHA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-221-CHA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Structured Top-Handle Leather Briefcase",
        "slug": "structured-top-handle-leather-briefcase-222",
        "description": "Executive business case with lockable clasp, laptop compartment, and burnished edge coat.",
        "category_slug": "leather-bags-luggage",
        "base_price": 17999.0,
        "discount_price": 14999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 22,
        "sales_count": 32,
        "primary_image": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-222-FOR-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-222-FOR-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-222-FOR-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-222-FOR-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-222-FOR-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-222-SLA-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-222-SLA-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-222-SLA-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-222-SLA-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-222-SLA-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Minimalist Leather Everyday Tote Bag",
        "slug": "minimalist-leather-everyday-tote-bag-223",
        "description": "Unlined vegetable-tanned tote with thick saddle-stitched shoulder handles and zip pouch.",
        "category_slug": "leather-bags-luggage",
        "base_price": 12999.0,
        "discount_price": 10999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 28,
        "sales_count": 33,
        "primary_image": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-223-OBS-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-223-OBS-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-223-OBS-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-223-OBS-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-223-OBS-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-223-IVO-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-223-IVO-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-223-IVO-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-223-IVO-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-223-IVO-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Pebbled Leather Commuter Backpack",
        "slug": "pebbled-leather-commuter-backpack-224",
        "description": "Ergonomic leather backpack featuring padded mesh back, laptop sleeve, and water bottle pocket.",
        "category_slug": "leather-bags-luggage",
        "base_price": 15999.0,
        "discount_price": 13499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 27,
        "sales_count": 34,
        "primary_image": "https://images.unsplash.com/photo-1650542218150-5e59a58d4312?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-224-CAM-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-224-CAM-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-224-CAM-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-224-CAM-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-224-CAM-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-224-ESP-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-224-ESP-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-224-ESP-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-224-ESP-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-224-ESP-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Leather Overnight Garment Duffle Hybrid",
        "slug": "leather-overnight-garment-duffle-hybrid-225",
        "description": "Intelligent travel bag that unzips completely into a hanging suit garment bag before rolling into a duffel.",
        "category_slug": "leather-bags-luggage",
        "base_price": 22999.0,
        "discount_price": 19499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 33,
        "sales_count": 35,
        "primary_image": "https://images.unsplash.com/photo-1691480150204-66dd1eb77391?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-225-BUR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-225-BUR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-225-BUR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-225-BUR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-225-BUR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-225-CLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-225-CLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-225-CLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-225-CLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-225-CLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Sling Leather Crossbody Messenger Bag",
        "slug": "sling-leather-crossbody-messenger-bag-226",
        "description": "Compact hands-free travel bag crafted from buttery soft calfskin with magnetic buckle.",
        "category_slug": "leather-bags-luggage",
        "base_price": 9999.0,
        "discount_price": 8499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 39,
        "sales_count": 36,
        "primary_image": "https://images.unsplash.com/photo-1705909237050-7a7625b47fac?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-226-MID-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-226-MID-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-226-MID-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-226-MID-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-LEA-226-MID-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-226-CHA-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-226-CHA-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-226-CHA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-226-CHA-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-LEA-226-CHA-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Vintage Leather Doctor's Travel Bag",
        "slug": "vintage-leather-doctor-s-travel-bag-227",
        "description": "Hinged frame opening travel satchel in pull-up leather that develops a rich personal patina.",
        "category_slug": "leather-bags-luggage",
        "base_price": 18499.0,
        "discount_price": 15499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 45,
        "sales_count": 37,
        "primary_image": "https://images.unsplash.com/photo-1577733966973-d680bffd2e80?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-227-FOR-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-227-FOR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-227-FOR-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-227-FOR-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-LEA-227-FOR-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-227-SLA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-227-SLA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-227-SLA-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-227-SLA-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-LEA-227-SLA-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Leather Dopp Kit Toiletry Bag",
        "slug": "leather-dopp-kit-toiletry-bag-228",
        "description": "Water-resistant nylon-lined shaving kit bag with brass zipper and leather carry handle.",
        "category_slug": "leather-bags-luggage",
        "base_price": 4999.0,
        "discount_price": 4199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 51,
        "sales_count": 38,
        "primary_image": "https://images.unsplash.com/photo-1689757875266-66446af145dc?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-228-OBS-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-228-OBS-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-228-OBS-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-228-OBS-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-LEA-228-OBS-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-228-IVO-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-228-IVO-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-228-IVO-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-228-IVO-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-LEA-228-IVO-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Slim Leather Document Portfolio Folio",
        "slug": "slim-leather-document-portfolio-folio-229",
        "description": "Sleek zippered A4 document folder in saffiano leather with card slots and pen loop.",
        "category_slug": "leather-bags-luggage",
        "base_price": 6999.0,
        "discount_price": 5899.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 57,
        "sales_count": 39,
        "primary_image": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-229-CAM-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-229-CAM-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-229-CAM-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-229-CAM-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-LEA-229-CAM-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-229-ESP-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-229-ESP-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-229-ESP-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-229-ESP-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-LEA-229-ESP-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Rolling Leather Carry-On Suitcase",
        "slug": "rolling-leather-carry-on-suitcase-230",
        "description": "Luxury spinner suitcase wrapped in full-grain bridle leather with telescopic aluminum handle.",
        "category_slug": "leather-bags-luggage",
        "base_price": 28999.0,
        "discount_price": 24999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 63,
        "sales_count": 40,
        "primary_image": "https://images.pexels.com/photos/904350/pexels-photo-904350.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-230-BUR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-230-BUR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-230-BUR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-230-BUR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-LEA-230-BUR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-230-CLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-230-CLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-230-CLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-230-CLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-LEA-230-CLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Hand-Rolled Como Silk Twill Scarf",
        "slug": "hand-rolled-como-silk-twill-scarf-231",
        "description": "Double-sided pure silk twill scarf with hand-rolled hems and intricate equestrian motif.",
        "category_slug": "accessories-fine-goods",
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 12,
        "sales_count": 41,
        "primary_image": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-ACC-231-MID-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-ACC-231-MID-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-ACC-231-MID-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-ACC-231-MID-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-ACC-231-MID-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-ACC-231-CHA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-ACC-231-CHA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-ACC-231-CHA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-ACC-231-CHA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-ACC-231-CHA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Full-Grain Italian Calfskin Dress Belt",
        "slug": "full-grain-italian-calfskin-dress-belt-232",
        "description": "Refined 32mm dress belt with feathered edge, tonal stitching, and solid brass buckle.",
        "category_slug": "accessories-fine-goods",
        "base_price": 4499.0,
        "discount_price": 3799.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 18,
        "sales_count": 42,
        "primary_image": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-ACC-232-FOR-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-ACC-232-FOR-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-ACC-232-FOR-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-ACC-232-FOR-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-ACC-232-FOR-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-ACC-232-SLA-XS",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-ACC-232-SLA-S",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-ACC-232-SLA-M",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-ACC-232-SLA-L",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-ACC-232-SLA-XL",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Woven Intrecciato Leather Belt",
        "slug": "woven-intrecciato-leather-belt-233",
        "description": "Artisanal woven leather belt without fixed holes for a custom fit, finished with brushed nickel.",
        "category_slug": "accessories-fine-goods",
        "base_price": 4999.0,
        "discount_price": 4199.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 24,
        "sales_count": 43,
        "primary_image": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-ACC-233-OBS-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-ACC-233-OBS-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-ACC-233-OBS-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-ACC-233-OBS-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-ACC-233-OBS-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-ACC-233-IVO-XS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-ACC-233-IVO-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-ACC-233-IVO-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-ACC-233-IVO-L",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-ACC-233-IVO-XL",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Pure Cashmere Winter Ribbed Beanie",
        "slug": "pure-cashmere-winter-ribbed-beanie-234",
        "description": "Ultra-soft 4-ply Mongolian cashmere watch cap beanie with snug ribbed fold-over cuff.",
        "category_slug": "accessories-fine-goods",
        "base_price": 3999.0,
        "discount_price": 3399.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 30,
        "sales_count": 44,
        "primary_image": "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-ACC-234-CAM-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-ACC-234-CAM-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-ACC-234-CAM-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-ACC-234-CAM-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-ACC-234-CAM-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-ACC-234-ESP-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-ACC-234-ESP-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-ACC-234-ESP-M",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-ACC-234-ESP-L",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-ACC-234-ESP-XL",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Cashmere & Silk Fringed Winter Scarf",
        "slug": "cashmere-silk-fringed-winter-scarf-235",
        "description": "Generously sized cold-weather scarf combining 80% cashmere and 20% silk with eyelash fringe.",
        "category_slug": "accessories-fine-goods",
        "base_price": 7499.0,
        "discount_price": 6299.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 36,
        "sales_count": 45,
        "primary_image": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-ACC-235-BUR-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-ACC-235-BUR-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-ACC-235-BUR-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-ACC-235-BUR-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-ACC-235-BUR-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-ACC-235-CLA-XS",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-ACC-235-CLA-S",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-ACC-235-CLA-M",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-ACC-235-CLA-L",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-ACC-235-CLA-XL",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Bifold Leather Cardholder Wallet",
        "slug": "bifold-leather-cardholder-wallet-236",
        "description": "Slim front-pocket wallet crafted from Horween shell cordovan with six card slots and cash slot.",
        "category_slug": "accessories-fine-goods",
        "base_price": 4799.0,
        "discount_price": 3999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 42,
        "sales_count": 46,
        "primary_image": "https://images.unsplash.com/photo-1614975058789-41316d0e2e9c?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-ACC-236-MID-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-ACC-236-MID-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-ACC-236-MID-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-ACC-236-MID-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1B2A4A",
                "sku": "AURA-ACC-236-MID-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-ACC-236-CHA-XS",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-ACC-236-CHA-S",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-ACC-236-CHA-M",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-ACC-236-CHA-L",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#333333",
                "sku": "AURA-ACC-236-CHA-XL",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Enamel & Solid Brass Cufflinks Set",
        "slug": "enamel-solid-brass-cufflinks-set-237",
        "description": "Bespoke formal cufflinks finished with hand-painted vitreous enamel and swivel T-bar clasp.",
        "category_slug": "accessories-fine-goods",
        "base_price": 3499.0,
        "discount_price": 2999.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 48,
        "sales_count": 47,
        "primary_image": "https://images.unsplash.com/photo-1790634271193-ab9fea24904a?auto=format&fit=crop&w=1000&q=80",
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-ACC-237-FOR-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-ACC-237-FOR-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-ACC-237-FOR-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-ACC-237-FOR-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B28",
                "sku": "AURA-ACC-237-FOR-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-ACC-237-SLA-XS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-ACC-237-SLA-S",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-ACC-237-SLA-M",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-ACC-237-SLA-L",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Blue",
                "color_hex": "#4A6B82",
                "sku": "AURA-ACC-237-SLA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Silk Knit Necktie in Midnight Navy",
        "slug": "silk-knit-necktie-in-midnight-navy-238",
        "description": "Textured square-end silk knit tie handcrafted in Italy for modern business-casual elegance.",
        "category_slug": "accessories-fine-goods",
        "base_price": 4299.0,
        "discount_price": 3599.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 47,
        "sales_count": 48,
        "primary_image": "https://images.pexels.com/photos/125779/pexels-photo-125779.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-ACC-238-OBS-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-ACC-238-OBS-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-ACC-238-OBS-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-ACC-238-OBS-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Obsidian Black",
                "color_hex": "#0B0C10",
                "sku": "AURA-ACC-238-OBS-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-ACC-238-IVO-XS",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-ACC-238-IVO-S",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-ACC-238-IVO-M",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-ACC-238-IVO-L",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ivory Cream",
                "color_hex": "#EAE6DF",
                "sku": "AURA-ACC-238-IVO-XL",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Leather Touchscreen Cashmere-Lined Gloves",
        "slug": "leather-touchscreen-cashmere-lined-gloves-239",
        "description": "Supple deerskin winter gloves lined in pure cashmere with touchscreen-conductive fingertips.",
        "category_slug": "accessories-fine-goods",
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 53,
        "sales_count": 49,
        "primary_image": "https://images.pexels.com/photos/277319/pexels-photo-277319.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-ACC-239-CAM-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-ACC-239-CAM-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-ACC-239-CAM-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-ACC-239-CAM-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Sand",
                "color_hex": "#C19A6B",
                "sku": "AURA-ACC-239-CAM-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-ACC-239-ESP-XS",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-ACC-239-ESP-S",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-ACC-239-ESP-M",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-ACC-239-ESP-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Espresso Brown",
                "color_hex": "#3D2B1F",
                "sku": "AURA-ACC-239-ESP-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "name": "Fine Leather Key Cloche with Brass Ring",
        "slug": "fine-leather-key-cloche-with-brass-ring-240",
        "description": "Minimalist neck lanyard key cloche in Tuscan box calfskin with screw-lock brass ring.",
        "category_slug": "accessories-fine-goods",
        "base_price": 2999.0,
        "discount_price": 2499.0,
        "brand": "AURA ATELIER",
        "material": "Luxury Natural Fibers",
        "fit_type": "Tailored Modern Fit",
        "care_instructions": "Dry clean only by luxury garment specialist",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 59,
        "sales_count": 30,
        "primary_image": "https://images.pexels.com/photos/1453008/pexels-photo-1453008.jpeg?auto=compress&cs=tinysrgb&w=800",
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-ACC-240-BUR-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-ACC-240-BUR-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-ACC-240-BUR-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-ACC-240-BUR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#581845",
                "sku": "AURA-ACC-240-BUR-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-ACC-240-CLA-XS",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-ACC-240-CLA-S",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-ACC-240-CLA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-ACC-240-CLA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic White",
                "color_hex": "#FDFDFD",
                "sku": "AURA-ACC-240-CLA-XL",
                "stock_quantity": 21,
                "additional_price": 0.0
            }
        ]
    }
]

def seed_database():
    app = create_app()
    with app.app_context():
        print("Ensuring database tables exist...")
        db.create_all()

        # Seed Admin User
        admin = User.query.filter_by(email="tanwaransh46@gmail.com").first()
        if not admin:
            admin = User(
                first_name="Ansh",
                last_name="Tanwar",
                email="tanwaransh46@gmail.com",
                role="admin",
                is_active=True
            )
            admin.set_password("Tanwar@12")
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: tanwaransh46@gmail.com / Tanwar@12")
        else:
            admin.role = "admin"
            admin.is_active = True
            admin.set_password("Tanwar@12")
            db.session.commit()
            print("Admin user verified: tanwaransh46@gmail.com")

        # Seed Categories
        cat_map = {}
        for cat_info in CATEGORIES_DATA:
            cat = Category.query.filter_by(slug=cat_info["slug"]).first()
            if not cat:
                cat = Category(
                    name=cat_info["name"],
                    slug=cat_info["slug"],
                    description=cat_info["description"],
                    image_url=cat_info["image_url"],
                    is_featured=cat_info["is_featured"]
                )
                db.session.add(cat)
                db.session.flush()
            else:
                cat.name = cat_info["name"]
                cat.description = cat_info["description"]
                cat.image_url = cat_info["image_url"]
                cat.is_featured = cat_info["is_featured"]
            cat_map[cat.slug] = cat.id
        db.session.commit()
        print(f"Seeded {len(cat_map)} categories.")

        # Seed 240 Products
        existing_slugs = set(p.slug for p in Product.query.with_entities(Product.slug).all())
        products_added = 0
        for p_info in PRODUCTS_DATA:
            cat_id = cat_map.get(p_info["category_slug"])
            if not cat_id:
                continue

            product = Product.query.filter_by(slug=p_info["slug"]).first()
            if not product:
                product = Product(
                    name=p_info["name"],
                    slug=p_info["slug"],
                    description=p_info["description"],
                    category_id=cat_id,
                    base_price=p_info["base_price"],
                    discount_price=p_info["discount_price"],
                    brand=p_info["brand"],
                    material=p_info["material"],
                    fit_type=p_info["fit_type"],
                    care_instructions=p_info["care_instructions"],
                    is_featured=bool(p_info["is_featured"]),
                    is_active=True,
                    average_rating=p_info["average_rating"],
                    review_count=p_info["review_count"],
                    sales_count=p_info["sales_count"]
                )
                db.session.add(product)
                db.session.flush()

                # Primary Image
                img = ProductImage(
                    product_id=product.id,
                    image_url=p_info["primary_image"],
                    is_primary=True,
                    display_order=0
                )
                db.session.add(img)

                # Variants
                for v_info in p_info["variants"]:
                    var = ProductVariant(
                        product_id=product.id,
                        size=v_info["size"],
                        color=v_info["color"],
                        color_hex=v_info["color_hex"],
                        sku=v_info["sku"],
                        stock_quantity=v_info["stock_quantity"],
                        additional_price=v_info["additional_price"]
                    )
                    db.session.add(var)

                products_added += 1
            else:
                # Update existing product details & primary image
                product.name = p_info["name"]
                product.category_id = cat_id
                product.base_price = p_info["base_price"]
                product.discount_price = p_info["discount_price"]
                product.is_active = True
                
                # Update primary image
                p_img = ProductImage.query.filter_by(product_id=product.id, is_primary=True).first()
                if p_img:
                    p_img.image_url = p_info["primary_image"]
                else:
                    db.session.add(ProductImage(
                        product_id=product.id,
                        image_url=p_info["primary_image"],
                        is_primary=True,
                        display_order=0
                    ))

        db.session.commit()
        print(f"Database sync complete! Products seeded/updated: {products_added}.")

if __name__ == "__main__":
    seed_database()
