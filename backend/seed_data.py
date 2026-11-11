import os
import random
import re
import uuid
from datetime import datetime, timedelta, timezone
from faker import Faker

from app import create_app
from models import (
    db, User, Address, Category, Product, ProductVariant,
    ProductImage, Coupon, Order, OrderItem, Payment,
    Review, Notification, ReturnRequest
)

fake = Faker()
Faker.seed(2026)
random.seed(2026)

CATEGORIES_DATA = [
    {
        "name": "Evening Gowns & Gala Dresses",
        "slug": "evening-gowns",
        "description": "Architectural silhouettes, silk velvet, and floor-length couture evening wear.",
        "image_url": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Cocktail & Silk Day Dresses",
        "slug": "cocktail-day-dresses",
        "description": "Mulberry silk slip dresses, linen shirt dresses, and daytime elegance.",
        "image_url": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Formal & Dress Shirts",
        "slug": "formal-dress-shirts",
        "description": "Giza 87 Egyptian cotton, Italian poplin, and tailored French-cuff dress shirts.",
        "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Luxury Polos & Resort Shirts",
        "slug": "luxury-polos-shirts",
        "description": "Silk-cotton fine knit polos, textured cabana button-downs, and open collars.",
        "image_url": "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Tailored Blazers & Sport Coats",
        "slug": "tailored-blazers",
        "description": "Biella virgin wool, English tweed, and structured double-breasted jackets.",
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Luxury Overcoats & Trench Coats",
        "slug": "overcoats-trench",
        "description": "Double-faced cashmere overcoats, weatherproof gabardine trench, and wool car coats.",
        "image_url": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Fine Knitwear",
        "slug": "fine-knitwear",
        "description": "Grade-A Mongolian cashmere crewnecks, silk-merino fine knits, and mock necks.",
        "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Luxury Sweaters & Cardigans",
        "slug": "sweaters-cardigans",
        "description": "Heavyweight cable-knit cardigans, brushed alpaca wool, and fisherman sweaters.",
        "image_url": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Tailored Dress Trousers",
        "slug": "tailored-trousers",
        "description": "Pleated tropical wool trousers, high-rise Gurkha pants, and wide-leg silhouettes.",
        "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Refined Chinos & Casual Pants",
        "slug": "chinos-casual-pants",
        "description": "Mercerized Pima stretch cotton chinos, drawstring travel pants, and officer twills.",
        "image_url": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Japanese Selvedge Denim",
        "slug": "selvedge-denim",
        "description": "Artisanal 14oz-16oz Okayama and Kuroki shuttle-loom raw selvedge denim.",
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Contemporary Jeans & Denim Wear",
        "slug": "designer-jeans",
        "description": "Refined black slim-taper jeans, vintage stonewashed cuts, and ecru denim.",
        "image_url": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Cashmere & Cotton Loungewear",
        "slug": "cashmere-loungewear",
        "description": "Heavyweight organic loopback hoodies, cashmere lounge sets, and French terry.",
        "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Silk Sleepwear & Robes",
        "slug": "silk-sleepwear-robes",
        "description": "Mulberry silk piped pajama sets, double-faced smoking robes, and lounge kimonos.",
        "image_url": "https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Haute Activewear & Training",
        "slug": "haute-activewear",
        "description": "Seamless ergonomic compression sets, micro-perforated training tees, and athletic wear.",
        "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Technical & Weather Performance",
        "slug": "technical-performance",
        "description": "AeroShield windbreakers, merino thermal baselayers, and storm-proof shells.",
        "image_url": "https://images.unsplash.com/photo-1548883354-7622d03aca27?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Leather & Suede Jackets",
        "slug": "leather-suede-jackets",
        "description": "Spanish goat suede Harringtons, full-grain calfskin cafe racers, and shearling aviators.",
        "image_url": "https://images.unsplash.com/photo-1487222477894-8943e31ef7b2?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Parkas, Puffers & Rainwear",
        "slug": "parkas-puffers",
        "description": "750-fill down expedition parkas, Loro Piana Storm-System trenches, and waxed jackets.",
        "image_url": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Pure Linen Shirts & Tops",
        "slug": "linen-shirts",
        "description": "Normandy flax band-collar shirts, relaxed popovers, and washed linen button-downs.",
        "image_url": "https://images.unsplash.com/photo-1603252109303-2751441dd157?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Linen Trousers & Resortwear",
        "slug": "linen-resortwear",
        "description": "European flax wide-leg drawstring trousers, Gurkha linen shorts, and safari outerwear.",
        "image_url": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Artisanal Leather Boots",
        "slug": "leather-boots",
        "description": "Goodyear-welted pebble leather Chelsea boots, hand-burnished Tuscan calfskin, and service boots.",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Luxury Dress Shoes & Loafers",
        "slug": "dress-shoes-loafers",
        "description": "Hand-burnished penny loafers, Italian Nappa minimalist sneakers, and Belgian suede loafers.",
        "image_url": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Leather Bags & Luggage",
        "slug": "leather-bags-luggage",
        "description": "Tuscan Vacchetta heritage duffle bags, executive pebble briefcases, and weekenders.",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    },
    {
        "name": "Fine Accessories & Silk Goods",
        "slug": "accessories-fine-goods",
        "description": "Hand-rolled mulberry silk pocket squares, Italian leather belts, and cashmere scarves.",
        "image_url": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?auto=format&fit=crop&w=800&q=85",
        "is_featured": 1
    }
]

PRODUCTS_DATA = [
    {
        "id": 1,
        "name": "Spanish Goat Suede Harrington Bomber Jacket",
        "slug": "jackets-outerwear-01-b6dcd",
        "description": "Crafted from velvety Spanish goat suede with a butter-soft hand feel. Finished with ribbed wool cuffs and hem, an antique brass two-way front zipper, and lustrous breathable cupro lining.",
        "category_id": 17,
        "base_price": 13999.0,
        "discount_price": 11999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Spanish Goat Suede Leather",
        "fit_type": "Classic Bomber Fit",
        "care_instructions": "Specialist leather clean only",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.4,
        "review_count": 22,
        "sales_count": 129,
        "created_at": "2026-11-06 17:42:14.473145",
        "updated_at": "2026-11-06 17:42:14.473145",
        "category_slug": "leather-suede-jackets",
        "images": [
            {
                "image_url": "/images/products/spanish-goat-suede-harrington-bomber-jacket-caramel-suede.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/spanish-goat-suede-harrington-bomber-jacket-noir-black-leather.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Caramel Suede",
                "color_hex": "#C19A6B",
                "sku": "AUR-001-XS-CAR",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Caramel Suede",
                "color_hex": "#C19A6B",
                "sku": "AUR-001-S-CAR",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Caramel Suede",
                "color_hex": "#C19A6B",
                "sku": "AUR-001-M-CAR",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Caramel Suede",
                "color_hex": "#C19A6B",
                "sku": "AUR-001-L-CAR",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Caramel Suede",
                "color_hex": "#C19A6B",
                "sku": "AUR-001-XL-CAR",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-001-XS-NOI",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-001-S-NOI",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-001-M-NOI",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-001-L-NOI",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-001-XL-NOI",
                "stock_quantity": 38,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 2,
        "name": "Spanish Merino Shearling Aviator Flight Jacket",
        "slug": "jackets-outerwear-02-b6892",
        "description": "Handcrafted from dense Spanish merino shearling with a thick fleece collar, adjustable buckled throat latch, and heavy-duty antiqued brass hardware.",
        "category_id": 17,
        "base_price": 18999.0,
        "discount_price": 15999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Genuine Merino Shearling & Leather",
        "fit_type": "Heritage Aviator Regular Fit",
        "care_instructions": "Specialist leather clean only",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.4,
        "review_count": 13,
        "sales_count": 85,
        "created_at": "2026-11-06 17:42:14.475148",
        "updated_at": "2026-11-06 17:42:14.475148",
        "category_slug": "leather-suede-jackets",
        "images": [
            {
                "image_url": "/images/products/spanish-merino-shearling-aviator-flight-jacket-cognac-tan-shearling.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/spanish-merino-shearling-aviator-flight-jacket-noir-black-moto.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Cognac Tan Shearling",
                "color_hex": "#9E5B32",
                "sku": "AUR-002-XS-COG",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Cognac Tan Shearling",
                "color_hex": "#9E5B32",
                "sku": "AUR-002-S-COG",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Cognac Tan Shearling",
                "color_hex": "#9E5B32",
                "sku": "AUR-002-M-COG",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Cognac Tan Shearling",
                "color_hex": "#9E5B32",
                "sku": "AUR-002-L-COG",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Cognac Tan Shearling",
                "color_hex": "#9E5B32",
                "sku": "AUR-002-XL-COG",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Noir Black Moto",
                "color_hex": "#1A1A1A",
                "sku": "AUR-002-XS-NOI",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Noir Black Moto",
                "color_hex": "#1A1A1A",
                "sku": "AUR-002-S-NOI",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Noir Black Moto",
                "color_hex": "#1A1A1A",
                "sku": "AUR-002-M-NOI",
                "stock_quantity": 40,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Noir Black Moto",
                "color_hex": "#1A1A1A",
                "sku": "AUR-002-L-NOI",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Noir Black Moto",
                "color_hex": "#1A1A1A",
                "sku": "AUR-002-XL-NOI",
                "stock_quantity": 24,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 3,
        "name": "StormShield 750-Fill Down Expedition Parka",
        "slug": "jackets-outerwear-03-76af6",
        "description": "Waterproof technical shell packed with 750 fill power RDS down. Designed with an insulated storm hood, fleece-lined hand pockets, and internal storm cuffs.",
        "category_id": 18,
        "base_price": 14499.0,
        "discount_price": 12299.0,
        "brand": "Aura Haute Collection",
        "material": "Waterproof Shell & 90/10 RDS Goose Down",
        "fit_type": "Expedition Fit",
        "care_instructions": "Machine wash cold gentle with down wash",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 17,
        "sales_count": 126,
        "created_at": "2026-11-06 17:42:14.481166",
        "updated_at": "2026-11-06 17:42:14.481166",
        "category_slug": "parkas-puffers",
        "images": [
            {
                "image_url": "/images/products/stormshield-750-fill-down-expedition-parka-forest-olive-green.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/stormshield-750-fill-down-expedition-parka-matte-black-parka.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive Green",
                "color_hex": "#3B4A3F",
                "sku": "AUR-003-XS-FOR",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive Green",
                "color_hex": "#3B4A3F",
                "sku": "AUR-003-S-FOR",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive Green",
                "color_hex": "#3B4A3F",
                "sku": "AUR-003-M-FOR",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive Green",
                "color_hex": "#3B4A3F",
                "sku": "AUR-003-L-FOR",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive Green",
                "color_hex": "#3B4A3F",
                "sku": "AUR-003-XL-FOR",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Matte Black Parka",
                "color_hex": "#1A1A1A",
                "sku": "AUR-003-XS-MAT",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Matte Black Parka",
                "color_hex": "#1A1A1A",
                "sku": "AUR-003-S-MAT",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Matte Black Parka",
                "color_hex": "#1A1A1A",
                "sku": "AUR-003-M-MAT",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Matte Black Parka",
                "color_hex": "#1A1A1A",
                "sku": "AUR-003-L-MAT",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Matte Black Parka",
                "color_hex": "#1A1A1A",
                "sku": "AUR-003-XL-MAT",
                "stock_quantity": 26,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 4,
        "name": "Cafe Racer Full-Grain Leather Moto Jacket",
        "slug": "jackets-outerwear-04-b9bdf",
        "description": "Iconic racer silhouette in full-grain cowhide leather with a mandarin snap collar, zippered cuffs, quilted shoulder detailing, and satin lining.",
        "category_id": 17,
        "base_price": 15999.0,
        "discount_price": 13499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Full-Grain Cowhide Leather",
        "fit_type": "Tailored Moto Fit",
        "care_instructions": "Condition with leather balm; specialist clean",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 23,
        "sales_count": 128,
        "created_at": "2026-11-06 17:42:14.484366",
        "updated_at": "2026-11-06 17:42:14.484366",
        "category_slug": "leather-suede-jackets",
        "images": [
            {
                "image_url": "/images/products/cafe-racer-full-grain-leather-moto-jacket-noir-black.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/cafe-racer-full-grain-leather-moto-jacket-caramel-suede.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Noir Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-004-XS-NOI",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Noir Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-004-S-NOI",
                "stock_quantity": 40,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Noir Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-004-M-NOI",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Noir Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-004-L-NOI",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Noir Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-004-XL-NOI",
                "stock_quantity": 30,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Caramel Suede",
                "color_hex": "#C19A6B",
                "sku": "AUR-004-XS-CAR",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Caramel Suede",
                "color_hex": "#C19A6B",
                "sku": "AUR-004-S-CAR",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Caramel Suede",
                "color_hex": "#C19A6B",
                "sku": "AUR-004-M-CAR",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Caramel Suede",
                "color_hex": "#C19A6B",
                "sku": "AUR-004-L-CAR",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Caramel Suede",
                "color_hex": "#C19A6B",
                "sku": "AUR-004-XL-CAR",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 5,
        "name": "Mulberry Silk Bias-Cut Slip Dress",
        "slug": "womens-dresses-05-006c3",
        "description": "Tailored from heavyweight 22-momme Mulberry silk that drapes gracefully along natural contours with a cowl neckline and adjustable straps.",
        "category_id": 2,
        "base_price": 7499.0,
        "discount_price": 6299.0,
        "brand": "Aura Haute Collection",
        "material": "100% Grade 6A Mulberry Silk",
        "fit_type": "Bias Cut / Fluid",
        "care_instructions": "Specialist dry clean",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.5,
        "review_count": 6,
        "sales_count": 70,
        "created_at": "2026-11-06 17:42:14.486885",
        "updated_at": "2026-11-06 17:42:14.486885",
        "category_slug": "cocktail-day-dresses",
        "images": [
            {
                "image_url": "/images/products/mulberry-silk-bias-cut-slip-dress-champagne-ivory.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/mulberry-silk-bias-cut-slip-dress-emerald-green.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Champagne Ivory",
                "color_hex": "#F3EDE2",
                "sku": "AUR-005-XS-CHA",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Champagne Ivory",
                "color_hex": "#F3EDE2",
                "sku": "AUR-005-S-CHA",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Champagne Ivory",
                "color_hex": "#F3EDE2",
                "sku": "AUR-005-M-CHA",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Champagne Ivory",
                "color_hex": "#F3EDE2",
                "sku": "AUR-005-L-CHA",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Champagne Ivory",
                "color_hex": "#F3EDE2",
                "sku": "AUR-005-XL-CHA",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Emerald Green",
                "color_hex": "#0E4D3E",
                "sku": "AUR-005-XS-EME",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Emerald Green",
                "color_hex": "#0E4D3E",
                "sku": "AUR-005-S-EME",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Emerald Green",
                "color_hex": "#0E4D3E",
                "sku": "AUR-005-M-EME",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Emerald Green",
                "color_hex": "#0E4D3E",
                "sku": "AUR-005-L-EME",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Emerald Green",
                "color_hex": "#0E4D3E",
                "sku": "AUR-005-XL-EME",
                "stock_quantity": 14,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 6,
        "name": "Duchess Cotton Velvet Gala Evening Gown",
        "slug": "womens-dresses-06-65c56",
        "description": "Dramatic floor-length gown crafted from plush Italian cotton velvet featuring a sculpted off-shoulder neckline and subtle side split.",
        "category_id": 1,
        "base_price": 9999.0,
        "discount_price": 8499.0,
        "brand": "Aura Haute Collection",
        "material": "98% Cotton Velvet, 2% Elastane",
        "fit_type": "Fitted Bodice / A-Line Skirt",
        "care_instructions": "Dry clean only",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.5,
        "review_count": 23,
        "sales_count": 118,
        "created_at": "2026-11-06 17:42:14.489886",
        "updated_at": "2026-11-06 17:42:14.489886",
        "category_slug": "evening-gowns",
        "images": [
            {
                "image_url": "/images/products/duchess-cotton-velvet-gala-evening-gown-burgundy-wine.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/duchess-cotton-velvet-gala-evening-gown-midnight-noir.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#6B1D2F",
                "sku": "AUR-006-XS-BUR",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#6B1D2F",
                "sku": "AUR-006-S-BUR",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#6B1D2F",
                "sku": "AUR-006-M-BUR",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#6B1D2F",
                "sku": "AUR-006-L-BUR",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#6B1D2F",
                "sku": "AUR-006-XL-BUR",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Midnight Noir",
                "color_hex": "#141416",
                "sku": "AUR-006-XS-MID",
                "stock_quantity": 40,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Noir",
                "color_hex": "#141416",
                "sku": "AUR-006-S-MID",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Noir",
                "color_hex": "#141416",
                "sku": "AUR-006-M-MID",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Noir",
                "color_hex": "#141416",
                "sku": "AUR-006-L-MID",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Noir",
                "color_hex": "#141416",
                "sku": "AUR-006-XL-MID",
                "stock_quantity": 39,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 7,
        "name": "French Flax Belted Linen Shirtdress",
        "slug": "womens-dresses-07-2fc53",
        "description": "Spun from pre-washed Normandy flax linen that softens beautifully with wear. Features natural mother-of-pearl buttons and a self-tie sash.",
        "category_id": 2,
        "base_price": 5499.0,
        "discount_price": 4699.0,
        "brand": "Aura Haute Collection",
        "material": "100% European Flax Linen",
        "fit_type": "Relaxed Fit",
        "care_instructions": "Machine wash cold delicate",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 24,
        "sales_count": 64,
        "created_at": "2026-11-06 17:42:14.491927",
        "updated_at": "2026-11-06 17:42:14.491927",
        "category_slug": "cocktail-day-dresses",
        "images": [
            {
                "image_url": "/images/products/french-flax-belted-linen-shirtdress-sage-olive.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/french-flax-belted-linen-shirtdress-oatmeal-natural.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Sage Olive",
                "color_hex": "#6B7C59",
                "sku": "AUR-007-XS-SAG",
                "stock_quantity": 30,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Sage Olive",
                "color_hex": "#6B7C59",
                "sku": "AUR-007-S-SAG",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Sage Olive",
                "color_hex": "#6B7C59",
                "sku": "AUR-007-M-SAG",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Sage Olive",
                "color_hex": "#6B7C59",
                "sku": "AUR-007-L-SAG",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Sage Olive",
                "color_hex": "#6B7C59",
                "sku": "AUR-007-XL-SAG",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Oatmeal Natural",
                "color_hex": "#DCCBB5",
                "sku": "AUR-007-XS-OAT",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Oatmeal Natural",
                "color_hex": "#DCCBB5",
                "sku": "AUR-007-S-OAT",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Oatmeal Natural",
                "color_hex": "#DCCBB5",
                "sku": "AUR-007-M-OAT",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Oatmeal Natural",
                "color_hex": "#DCCBB5",
                "sku": "AUR-007-L-OAT",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Oatmeal Natural",
                "color_hex": "#DCCBB5",
                "sku": "AUR-007-XL-OAT",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 8,
        "name": "Botanical Silk Chiffon Tiered Maxi Dress",
        "slug": "womens-dresses-08-cf93f",
        "description": "Ethereal floral silk chiffon dress with cascading micro-pleats, smocked elasticated waist, and delicate bishop sleeves.",
        "category_id": 2,
        "base_price": 8299.0,
        "discount_price": 6999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Silk Chiffon with Rayon Lining",
        "fit_type": "Flowing Tiered Fit",
        "care_instructions": "Hand wash cold or dry clean",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 9,
        "sales_count": 35,
        "created_at": "2026-11-06 17:42:14.494935",
        "updated_at": "2026-11-06 17:42:14.494935",
        "category_slug": "cocktail-day-dresses",
        "images": [
            {
                "image_url": "/images/products/botanical-silk-chiffon-tiered-maxi-dress-blush-rose-floral.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/botanical-silk-chiffon-tiered-maxi-dress-scarlet-blossom.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Blush Rose Floral",
                "color_hex": "#E29D9D",
                "sku": "AUR-008-XS-BLU",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Blush Rose Floral",
                "color_hex": "#E29D9D",
                "sku": "AUR-008-S-BLU",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Blush Rose Floral",
                "color_hex": "#E29D9D",
                "sku": "AUR-008-M-BLU",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Blush Rose Floral",
                "color_hex": "#E29D9D",
                "sku": "AUR-008-L-BLU",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Blush Rose Floral",
                "color_hex": "#E29D9D",
                "sku": "AUR-008-XL-BLU",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Scarlet Blossom",
                "color_hex": "#A52A2A",
                "sku": "AUR-008-XS-SCA",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Scarlet Blossom",
                "color_hex": "#A52A2A",
                "sku": "AUR-008-S-SCA",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Scarlet Blossom",
                "color_hex": "#A52A2A",
                "sku": "AUR-008-M-SCA",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Scarlet Blossom",
                "color_hex": "#A52A2A",
                "sku": "AUR-008-L-SCA",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Scarlet Blossom",
                "color_hex": "#A52A2A",
                "sku": "AUR-008-XL-SCA",
                "stock_quantity": 30,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 9,
        "name": "Albini Two-Ply Royal Oxford Shirt",
        "slug": "mens-shirts-09-46401",
        "description": "Woven from superfine two-ply Egyptian cotton from renowned Italian mill Albini. Features a structured semi-spread collar and mother-of-pearl buttons.",
        "category_id": 3,
        "base_price": 4499.0,
        "discount_price": 3799.0,
        "brand": "Aura Haute Collection",
        "material": "100% Egyptian Giza Cotton",
        "fit_type": "Tailored Slim Fit",
        "care_instructions": "Machine wash warm, iron medium",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 12,
        "sales_count": 45,
        "created_at": "2026-11-06 17:42:14.498454",
        "updated_at": "2026-11-06 17:42:14.498454",
        "category_slug": "formal-dress-shirts",
        "images": [
            {
                "image_url": "/images/products/albini-two-ply-royal-oxford-shirt-sky-blue-oxford.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/albini-two-ply-royal-oxford-shirt-crisp-white-poplin.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Sky Blue Oxford",
                "color_hex": "#87CEEB",
                "sku": "AUR-009-XS-SKY",
                "stock_quantity": 40,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Sky Blue Oxford",
                "color_hex": "#87CEEB",
                "sku": "AUR-009-S-SKY",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Sky Blue Oxford",
                "color_hex": "#87CEEB",
                "sku": "AUR-009-M-SKY",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Sky Blue Oxford",
                "color_hex": "#87CEEB",
                "sku": "AUR-009-L-SKY",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Sky Blue Oxford",
                "color_hex": "#87CEEB",
                "sku": "AUR-009-XL-SKY",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Crisp White Poplin",
                "color_hex": "#F8F9FA",
                "sku": "AUR-009-XS-CRI",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Crisp White Poplin",
                "color_hex": "#F8F9FA",
                "sku": "AUR-009-S-CRI",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Crisp White Poplin",
                "color_hex": "#F8F9FA",
                "sku": "AUR-009-M-CRI",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Crisp White Poplin",
                "color_hex": "#F8F9FA",
                "sku": "AUR-009-L-CRI",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Crisp White Poplin",
                "color_hex": "#F8F9FA",
                "sku": "AUR-009-XL-CRI",
                "stock_quantity": 35,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 10,
        "name": "Riviera Camp-Collar Normandy Linen Shirt",
        "slug": "mens-shirts-10-50461",
        "description": "Casual relaxed camp-collar shirt cut from pre-washed French flax linen with an airy basket weave and straight split hem.",
        "category_id": 4,
        "base_price": 3999.0,
        "discount_price": 3299.0,
        "brand": "Aura Haute Collection",
        "material": "100% French Flax Linen",
        "fit_type": "Relaxed Fit",
        "care_instructions": "Machine wash cold gentle, line dry",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 25,
        "sales_count": 107,
        "created_at": "2026-11-06 17:42:14.500453",
        "updated_at": "2026-11-06 17:42:14.500453",
        "category_slug": "luxury-polos-shirts",
        "images": [
            {
                "image_url": "/images/products/riviera-camp-collar-normandy-linen-shirt-terracotta-rust.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/riviera-camp-collar-normandy-linen-shirt-sage-olive-linen.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Terracotta Rust",
                "color_hex": "#C85A32",
                "sku": "AUR-010-XS-TER",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Terracotta Rust",
                "color_hex": "#C85A32",
                "sku": "AUR-010-S-TER",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Terracotta Rust",
                "color_hex": "#C85A32",
                "sku": "AUR-010-M-TER",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Terracotta Rust",
                "color_hex": "#C85A32",
                "sku": "AUR-010-L-TER",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Terracotta Rust",
                "color_hex": "#C85A32",
                "sku": "AUR-010-XL-TER",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Sage Olive Linen",
                "color_hex": "#667C59",
                "sku": "AUR-010-XS-SAG",
                "stock_quantity": 40,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Sage Olive Linen",
                "color_hex": "#667C59",
                "sku": "AUR-010-S-SAG",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Sage Olive Linen",
                "color_hex": "#667C59",
                "sku": "AUR-010-M-SAG",
                "stock_quantity": 40,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Sage Olive Linen",
                "color_hex": "#667C59",
                "sku": "AUR-010-L-SAG",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Sage Olive Linen",
                "color_hex": "#667C59",
                "sku": "AUR-010-XL-SAG",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 11,
        "name": "Silk-Cotton Fine Gauge Knit Polo",
        "slug": "mens-shirts-11-5eb43",
        "description": "Elevated polo shirt spun with 70% long-staple cotton and 30% silk for a luxurious hand feel, seamless collar, and ribbed hems.",
        "category_id": 4,
        "base_price": 4299.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "70% Long-Staple Cotton, 30% Silk",
        "fit_type": "Modern Tailored",
        "care_instructions": "Hand wash cold, dry flat",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 6,
        "sales_count": 47,
        "created_at": "2026-11-06 17:42:14.503426",
        "updated_at": "2026-11-06 17:42:14.503426",
        "category_slug": "luxury-polos-shirts",
        "images": [
            {
                "image_url": "/images/products/silk-cotton-fine-gauge-knit-polo-navy-melange.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/silk-cotton-fine-gauge-knit-polo-crisp-white.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Navy Melange",
                "color_hex": "#1B2A4A",
                "sku": "AUR-011-XS-NAV",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Navy Melange",
                "color_hex": "#1B2A4A",
                "sku": "AUR-011-S-NAV",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Navy Melange",
                "color_hex": "#1B2A4A",
                "sku": "AUR-011-M-NAV",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Navy Melange",
                "color_hex": "#1B2A4A",
                "sku": "AUR-011-L-NAV",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Navy Melange",
                "color_hex": "#1B2A4A",
                "sku": "AUR-011-XL-NAV",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Crisp White",
                "color_hex": "#F8F9FA",
                "sku": "AUR-011-XS-CRI",
                "stock_quantity": 40,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Crisp White",
                "color_hex": "#F8F9FA",
                "sku": "AUR-011-S-CRI",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Crisp White",
                "color_hex": "#F8F9FA",
                "sku": "AUR-011-M-CRI",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Crisp White",
                "color_hex": "#F8F9FA",
                "sku": "AUR-011-L-CRI",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Crisp White",
                "color_hex": "#F8F9FA",
                "sku": "AUR-011-XL-CRI",
                "stock_quantity": 40,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 12,
        "name": "Heavyweight Japanese Cotton Twill Overshirt",
        "slug": "mens-shirts-12-af4aa",
        "description": "Substantial 340 GSM Japanese twill overshirt engineered with dual chest flap pockets and reinforced felled seams for versatile over-layering.",
        "category_id": 4,
        "base_price": 5299.0,
        "discount_price": 4499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Japanese Cotton Twill",
        "fit_type": "Relaxed Overshirt Fit",
        "care_instructions": "Machine wash cold, inside out",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 6,
        "sales_count": 132,
        "created_at": "2026-11-06 17:42:14.505472",
        "updated_at": "2026-11-06 17:42:14.505472",
        "category_slug": "luxury-polos-shirts",
        "images": [
            {
                "image_url": "/images/products/heavyweight-japanese-cotton-twill-overshirt-midnight-navy.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/heavyweight-japanese-cotton-twill-overshirt-terracotta-clay.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1A2332",
                "sku": "AUR-012-XS-MID",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1A2332",
                "sku": "AUR-012-S-MID",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1A2332",
                "sku": "AUR-012-M-MID",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1A2332",
                "sku": "AUR-012-L-MID",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1A2332",
                "sku": "AUR-012-XL-MID",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Terracotta Clay",
                "color_hex": "#C85A32",
                "sku": "AUR-012-XS-TER",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Terracotta Clay",
                "color_hex": "#C85A32",
                "sku": "AUR-012-S-TER",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Terracotta Clay",
                "color_hex": "#C85A32",
                "sku": "AUR-012-M-TER",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Terracotta Clay",
                "color_hex": "#C85A32",
                "sku": "AUR-012-L-TER",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Terracotta Clay",
                "color_hex": "#C85A32",
                "sku": "AUR-012-XL-TER",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 13,
        "name": "Biella Virgin Wool Double-Breasted Blazer",
        "slug": "blazers-coats-13-de66f",
        "description": "Tailored from luxurious virgin wool twill from Biella, Italy. Features peak lapels, half-canvas construction, horn buttons, and double back vents.",
        "category_id": 5,
        "base_price": 12999.0,
        "discount_price": 10999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Italian Virgin Wool",
        "fit_type": "Structured Tailored",
        "care_instructions": "Specialist dry clean",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.5,
        "review_count": 16,
        "sales_count": 87,
        "created_at": "2026-11-06 17:42:14.508481",
        "updated_at": "2026-11-06 17:42:14.508481",
        "category_slug": "tailored-blazers",
        "images": [
            {
                "image_url": "/images/products/biella-virgin-wool-double-breasted-blazer-camel-tan-flannel.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/biella-virgin-wool-double-breasted-blazer-midnight-navy-twill.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Camel Tan Flannel",
                "color_hex": "#C19A6B",
                "sku": "AUR-013-XS-CAM",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Tan Flannel",
                "color_hex": "#C19A6B",
                "sku": "AUR-013-S-CAM",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Tan Flannel",
                "color_hex": "#C19A6B",
                "sku": "AUR-013-M-CAM",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Tan Flannel",
                "color_hex": "#C19A6B",
                "sku": "AUR-013-L-CAM",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Tan Flannel",
                "color_hex": "#C19A6B",
                "sku": "AUR-013-XL-CAM",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Midnight Navy Twill",
                "color_hex": "#1A2639",
                "sku": "AUR-013-XS-MID",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy Twill",
                "color_hex": "#1A2639",
                "sku": "AUR-013-S-MID",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy Twill",
                "color_hex": "#1A2639",
                "sku": "AUR-013-M-MID",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy Twill",
                "color_hex": "#1A2639",
                "sku": "AUR-013-L-MID",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy Twill",
                "color_hex": "#1A2639",
                "sku": "AUR-013-XL-MID",
                "stock_quantity": 32,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 14,
        "name": "Double-Faced Cashmere & Wool Trench Overcoat",
        "slug": "blazers-coats-14-a8630",
        "description": "Exceptional thermal warmth woven with 85% Australian merino wool and 15% Mongolian cashmere. Hand-finished double-face craftsmanship with unlined interior.",
        "category_id": 6,
        "base_price": 16999.0,
        "discount_price": 14499.0,
        "brand": "Aura Haute Collection",
        "material": "85% Merino Wool, 15% Cashmere",
        "fit_type": "Relaxed Overcoat Fit",
        "care_instructions": "Specialist dry clean",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.5,
        "review_count": 21,
        "sales_count": 88,
        "created_at": "2026-11-06 17:42:14.511060",
        "updated_at": "2026-11-06 17:42:14.511060",
        "category_slug": "overcoats-trench",
        "images": [
            {
                "image_url": "/images/products/double-faced-cashmere-wool-trench-overcoat-charcoal-black-melange.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/double-faced-cashmere-wool-trench-overcoat-camel-gabardine.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Charcoal Black Melange",
                "color_hex": "#212121",
                "sku": "AUR-014-XS-CHA",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Black Melange",
                "color_hex": "#212121",
                "sku": "AUR-014-S-CHA",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Black Melange",
                "color_hex": "#212121",
                "sku": "AUR-014-M-CHA",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Black Melange",
                "color_hex": "#212121",
                "sku": "AUR-014-L-CHA",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Black Melange",
                "color_hex": "#212121",
                "sku": "AUR-014-XL-CHA",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Camel Gabardine",
                "color_hex": "#C49E73",
                "sku": "AUR-014-XS-CAM",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Gabardine",
                "color_hex": "#C49E73",
                "sku": "AUR-014-S-CAM",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Gabardine",
                "color_hex": "#C49E73",
                "sku": "AUR-014-M-CAM",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Gabardine",
                "color_hex": "#C49E73",
                "sku": "AUR-014-L-CAM",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Gabardine",
                "color_hex": "#C49E73",
                "sku": "AUR-014-XL-CAM",
                "stock_quantity": 30,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 15,
        "name": "Unstructured Belgian Linen Sport Coat",
        "slug": "blazers-coats-15-65706",
        "description": "Breezy tailored sport coat crafted with unlined shoulders and patch pockets from breathable Belgian flax linen.",
        "category_id": 5,
        "base_price": 9499.0,
        "discount_price": 7999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Belgian Linen",
        "fit_type": "Soft Tailoring",
        "care_instructions": "Dry clean only",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.6,
        "review_count": 8,
        "sales_count": 124,
        "created_at": "2026-11-06 17:42:14.514423",
        "updated_at": "2026-11-06 17:42:14.514423",
        "category_slug": "tailored-blazers",
        "images": [
            {
                "image_url": "/images/products/unstructured-belgian-linen-sport-coat-midnight-navy.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/unstructured-belgian-linen-sport-coat-camel-tan.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#1A2639",
                "sku": "AUR-015-XS-MID",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#1A2639",
                "sku": "AUR-015-S-MID",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#1A2639",
                "sku": "AUR-015-M-MID",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#1A2639",
                "sku": "AUR-015-L-MID",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#1A2639",
                "sku": "AUR-015-XL-MID",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Camel Tan",
                "color_hex": "#C19A6B",
                "sku": "AUR-015-XS-CAM",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Tan",
                "color_hex": "#C19A6B",
                "sku": "AUR-015-S-CAM",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Tan",
                "color_hex": "#C19A6B",
                "sku": "AUR-015-M-CAM",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Tan",
                "color_hex": "#C19A6B",
                "sku": "AUR-015-L-CAM",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Tan",
                "color_hex": "#C19A6B",
                "sku": "AUR-015-XL-CAM",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 16,
        "name": "Weatherproof Cotton Gabardine Belted Trench",
        "slug": "blazers-coats-16-babfc",
        "description": "Timeless military trench coat cut from tightly woven water-repellent cotton gabardine. Features storm flap, buckled waist belt, and horn buttons.",
        "category_id": 6,
        "base_price": 14999.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% Weatherproof Cotton Gabardine",
        "fit_type": "Classic Trench Cut",
        "care_instructions": "Dry clean only",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.6,
        "review_count": 22,
        "sales_count": 96,
        "created_at": "2026-11-06 17:42:14.518363",
        "updated_at": "2026-11-06 17:42:14.518363",
        "category_slug": "overcoats-trench",
        "images": [
            {
                "image_url": "/images/products/weatherproof-cotton-gabardine-belted-trench-honey-camel-trench.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/weatherproof-cotton-gabardine-belted-trench-charcoal-slate.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Honey Camel Trench",
                "color_hex": "#C49E73",
                "sku": "AUR-016-XS-HON",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Honey Camel Trench",
                "color_hex": "#C49E73",
                "sku": "AUR-016-S-HON",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Honey Camel Trench",
                "color_hex": "#C49E73",
                "sku": "AUR-016-M-HON",
                "stock_quantity": 40,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Honey Camel Trench",
                "color_hex": "#C49E73",
                "sku": "AUR-016-L-HON",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Honey Camel Trench",
                "color_hex": "#C49E73",
                "sku": "AUR-016-XL-HON",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Slate",
                "color_hex": "#212121",
                "sku": "AUR-016-XS-CHA",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Slate",
                "color_hex": "#212121",
                "sku": "AUR-016-S-CHA",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Slate",
                "color_hex": "#212121",
                "sku": "AUR-016-M-CHA",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Slate",
                "color_hex": "#212121",
                "sku": "AUR-016-L-CHA",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Slate",
                "color_hex": "#212121",
                "sku": "AUR-016-XL-CHA",
                "stock_quantity": 17,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 17,
        "name": "Grade-A Mongolian Cashmere Crewneck",
        "slug": "knitwear-sweaters-17-178d7",
        "description": "Supreme softness spun from 2-ply 100% Grade-A inner Mongolian cashmere. Features ribbed collar, cuffs, and hem for timeless warmth.",
        "category_id": 7,
        "base_price": 8999.0,
        "discount_price": 7499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Grade-A Mongolian Cashmere",
        "fit_type": "Classic Fit",
        "care_instructions": "Hand wash cold, dry flat",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.5,
        "review_count": 20,
        "sales_count": 53,
        "created_at": "2026-11-06 17:42:14.522101",
        "updated_at": "2026-11-06 17:42:14.522101",
        "category_slug": "fine-knitwear",
        "images": [
            {
                "image_url": "/images/products/grade-a-mongolian-cashmere-crewneck-cream-oatmeal.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/grade-a-mongolian-cashmere-crewneck-charcoal-heather.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Cream Oatmeal",
                "color_hex": "#E8DFD1",
                "sku": "AUR-017-XS-CRE",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Cream Oatmeal",
                "color_hex": "#E8DFD1",
                "sku": "AUR-017-S-CRE",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Cream Oatmeal",
                "color_hex": "#E8DFD1",
                "sku": "AUR-017-M-CRE",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Cream Oatmeal",
                "color_hex": "#E8DFD1",
                "sku": "AUR-017-L-CRE",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Cream Oatmeal",
                "color_hex": "#E8DFD1",
                "sku": "AUR-017-XL-CRE",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Heather",
                "color_hex": "#343A40",
                "sku": "AUR-017-XS-CHA",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Heather",
                "color_hex": "#343A40",
                "sku": "AUR-017-S-CHA",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Heather",
                "color_hex": "#343A40",
                "sku": "AUR-017-M-CHA",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Heather",
                "color_hex": "#343A40",
                "sku": "AUR-017-L-CHA",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Heather",
                "color_hex": "#343A40",
                "sku": "AUR-017-XL-CHA",
                "stock_quantity": 30,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 18,
        "name": "Heavyweight Cable-Knit Merino Cardigan",
        "slug": "knitwear-sweaters-18-829d1",
        "description": "Chunky Aran cable knit woven from 100% Australian extra-fine merino wool with hand-stitched leather buttons and front patch pockets.",
        "category_id": 8,
        "base_price": 7299.0,
        "discount_price": 5999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Extra-Fine Merino Wool",
        "fit_type": "Relaxed Fit",
        "care_instructions": "Dry clean or gentle hand wash",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.6,
        "review_count": 10,
        "sales_count": 81,
        "created_at": "2026-11-06 17:42:14.524838",
        "updated_at": "2026-11-06 17:42:14.524838",
        "category_slug": "sweaters-cardigans",
        "images": [
            {
                "image_url": "/images/products/heavyweight-cable-knit-merino-cardigan-winter-ecru-white.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/heavyweight-cable-knit-merino-cardigan-cognac-ribbed.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Winter Ecru White",
                "color_hex": "#F4F0E8",
                "sku": "AUR-018-XS-WIN",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Winter Ecru White",
                "color_hex": "#F4F0E8",
                "sku": "AUR-018-S-WIN",
                "stock_quantity": 30,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Winter Ecru White",
                "color_hex": "#F4F0E8",
                "sku": "AUR-018-M-WIN",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Winter Ecru White",
                "color_hex": "#F4F0E8",
                "sku": "AUR-018-L-WIN",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Winter Ecru White",
                "color_hex": "#F4F0E8",
                "sku": "AUR-018-XL-WIN",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Cognac Ribbed",
                "color_hex": "#8B4513",
                "sku": "AUR-018-XS-COG",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Cognac Ribbed",
                "color_hex": "#8B4513",
                "sku": "AUR-018-S-COG",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Cognac Ribbed",
                "color_hex": "#8B4513",
                "sku": "AUR-018-M-COG",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Cognac Ribbed",
                "color_hex": "#8B4513",
                "sku": "AUR-018-L-COG",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Cognac Ribbed",
                "color_hex": "#8B4513",
                "sku": "AUR-018-XL-COG",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 19,
        "name": "Fine Gauge Merino Wool Turtleneck",
        "slug": "knitwear-sweaters-19-3bb08",
        "description": "Spun from 19.5-micron fine Australian merino wool in a silky rib knit. Designed to layer smoothly beneath tailored blazers and trench coats.",
        "category_id": 7,
        "base_price": 6299.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% Fine Merino Wool",
        "fit_type": "Slim Tailored",
        "care_instructions": "Machine wash cold on wool cycle",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.6,
        "review_count": 20,
        "sales_count": 58,
        "created_at": "2026-11-06 17:42:14.528458",
        "updated_at": "2026-11-06 17:42:14.528458",
        "category_slug": "fine-knitwear",
        "images": [
            {
                "image_url": "/images/products/fine-gauge-merino-wool-turtleneck-camel-heather.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/fine-gauge-merino-wool-turtleneck-noir-black.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Camel Heather",
                "color_hex": "#C19A6B",
                "sku": "AUR-019-XS-CAM",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Heather",
                "color_hex": "#C19A6B",
                "sku": "AUR-019-S-CAM",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Heather",
                "color_hex": "#C19A6B",
                "sku": "AUR-019-M-CAM",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Heather",
                "color_hex": "#C19A6B",
                "sku": "AUR-019-L-CAM",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Heather",
                "color_hex": "#C19A6B",
                "sku": "AUR-019-XL-CAM",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Noir Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-019-XS-NOI",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Noir Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-019-S-NOI",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Noir Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-019-M-NOI",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Noir Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-019-L-NOI",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Noir Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-019-XL-NOI",
                "stock_quantity": 15,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 20,
        "name": "Brushed Alpaca Wool Relaxed Crew",
        "slug": "knitwear-sweaters-20-b3ed4",
        "description": "Fluffy, cloud-like texture knitted from a blend of Peruvian baby alpaca and wool. Warm, breathable, and finished with a comfortable ribbed collar.",
        "category_id": 8,
        "base_price": 7899.0,
        "discount_price": 6499.0,
        "brand": "Aura Haute Collection",
        "material": "60% Baby Alpaca, 28% Wool, 12% Polyamide",
        "fit_type": "Boxy Relaxed Fit",
        "care_instructions": "Hand wash cold, reshape and dry flat",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.5,
        "review_count": 24,
        "sales_count": 83,
        "created_at": "2026-11-06 17:42:14.532264",
        "updated_at": "2026-11-06 17:42:14.532264",
        "category_slug": "sweaters-cardigans",
        "images": [
            {
                "image_url": "/images/products/brushed-alpaca-wool-relaxed-crew-charcoal-heather-melange.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/brushed-alpaca-wool-relaxed-crew-winter-ecru-white.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Charcoal Heather Melange",
                "color_hex": "#343A40",
                "sku": "AUR-020-XS-CHA",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Heather Melange",
                "color_hex": "#343A40",
                "sku": "AUR-020-S-CHA",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Heather Melange",
                "color_hex": "#343A40",
                "sku": "AUR-020-M-CHA",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Heather Melange",
                "color_hex": "#343A40",
                "sku": "AUR-020-L-CHA",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Heather Melange",
                "color_hex": "#343A40",
                "sku": "AUR-020-XL-CHA",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Winter Ecru White",
                "color_hex": "#F4F0E8",
                "sku": "AUR-020-XS-WIN",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Winter Ecru White",
                "color_hex": "#F4F0E8",
                "sku": "AUR-020-S-WIN",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Winter Ecru White",
                "color_hex": "#F4F0E8",
                "sku": "AUR-020-M-WIN",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Winter Ecru White",
                "color_hex": "#F4F0E8",
                "sku": "AUR-020-L-WIN",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Winter Ecru White",
                "color_hex": "#F4F0E8",
                "sku": "AUR-020-XL-WIN",
                "stock_quantity": 22,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 21,
        "name": "Biella Tropical Wool Pleated Trousers",
        "slug": "trousers-chinos-21-555ca",
        "description": "Tailored with single front pleats, side adjusters, and a clean taper. Woven from breathable tropical wool for a sharp fluid drape in all seasons.",
        "category_id": 9,
        "base_price": 6499.0,
        "discount_price": 5299.0,
        "brand": "Aura Haute Collection",
        "material": "100% Tropical Wool",
        "fit_type": "Tapered Pleated",
        "care_instructions": "Specialist dry clean",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.4,
        "review_count": 21,
        "sales_count": 111,
        "created_at": "2026-11-06 17:42:14.536561",
        "updated_at": "2026-11-06 17:42:14.536561",
        "category_slug": "tailored-trousers",
        "images": [
            {
                "image_url": "/images/products/biella-tropical-wool-pleated-trousers-charcoal-slate-melange.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/biella-tropical-wool-pleated-trousers-natural-oatmeal-linen.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Charcoal Slate Melange",
                "color_hex": "#343A40",
                "sku": "AUR-021-XS-CHA",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Slate Melange",
                "color_hex": "#343A40",
                "sku": "AUR-021-S-CHA",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Slate Melange",
                "color_hex": "#343A40",
                "sku": "AUR-021-M-CHA",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Slate Melange",
                "color_hex": "#343A40",
                "sku": "AUR-021-L-CHA",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Slate Melange",
                "color_hex": "#343A40",
                "sku": "AUR-021-XL-CHA",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Natural Oatmeal Linen",
                "color_hex": "#D8D2C2",
                "sku": "AUR-021-XS-NAT",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Natural Oatmeal Linen",
                "color_hex": "#D8D2C2",
                "sku": "AUR-021-S-NAT",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Natural Oatmeal Linen",
                "color_hex": "#D8D2C2",
                "sku": "AUR-021-M-NAT",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Natural Oatmeal Linen",
                "color_hex": "#D8D2C2",
                "sku": "AUR-021-L-NAT",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Natural Oatmeal Linen",
                "color_hex": "#D8D2C2",
                "sku": "AUR-021-XL-NAT",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 22,
        "name": "Pima Stretch Cotton Tailored Chinos",
        "slug": "trousers-chinos-22-c09af",
        "description": "Cut from premium 98% long-staple pima cotton twill and 2% elastane for slight give. Features horn buttons and taped interior seams.",
        "category_id": 10,
        "base_price": 4299.0,
        "discount_price": 3599.0,
        "brand": "Aura Haute Collection",
        "material": "98% Pima Cotton, 2% Elastane",
        "fit_type": "Slim Tapered",
        "care_instructions": "Machine wash cold",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 7,
        "sales_count": 76,
        "created_at": "2026-11-06 17:42:14.540269",
        "updated_at": "2026-11-06 17:42:14.540269",
        "category_slug": "chinos-casual-pants",
        "images": [
            {
                "image_url": "/images/products/pima-stretch-cotton-tailored-chinos-classic-khaki-tan.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/pima-stretch-cotton-tailored-chinos-charcoal-grey.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Classic Khaki Tan",
                "color_hex": "#C19A6B",
                "sku": "AUR-022-XS-CLA",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Classic Khaki Tan",
                "color_hex": "#C19A6B",
                "sku": "AUR-022-S-CLA",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Classic Khaki Tan",
                "color_hex": "#C19A6B",
                "sku": "AUR-022-M-CLA",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Classic Khaki Tan",
                "color_hex": "#C19A6B",
                "sku": "AUR-022-L-CLA",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Classic Khaki Tan",
                "color_hex": "#C19A6B",
                "sku": "AUR-022-XL-CLA",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Grey",
                "color_hex": "#343A40",
                "sku": "AUR-022-XS-CHA",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Grey",
                "color_hex": "#343A40",
                "sku": "AUR-022-S-CHA",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Grey",
                "color_hex": "#343A40",
                "sku": "AUR-022-M-CHA",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Grey",
                "color_hex": "#343A40",
                "sku": "AUR-022-L-CHA",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Grey",
                "color_hex": "#343A40",
                "sku": "AUR-022-XL-CHA",
                "stock_quantity": 30,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 23,
        "name": "Belgian Flax Linen Wide-Leg Trousers",
        "slug": "trousers-chinos-23-3c05a",
        "description": "High-waisted, fluid silhouette tailored with deep front pleats from heavyweight 280 GSM Belgian flax linen. Effortlessly relaxed and cool.",
        "category_id": 9,
        "base_price": 5499.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% Belgian Flax Linen",
        "fit_type": "Wide Leg Relaxed",
        "care_instructions": "Machine wash delicate, hang dry",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 19,
        "sales_count": 131,
        "created_at": "2026-11-06 17:42:14.541949",
        "updated_at": "2026-11-06 17:42:14.541949",
        "category_slug": "tailored-trousers",
        "images": [
            {
                "image_url": "/images/products/belgian-flax-linen-wide-leg-trousers-ecru-natural-linen.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/belgian-flax-linen-wide-leg-trousers-charcoal-slate.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Ecru Natural Linen",
                "color_hex": "#E8E2D5",
                "sku": "AUR-023-XS-ECR",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Ecru Natural Linen",
                "color_hex": "#E8E2D5",
                "sku": "AUR-023-S-ECR",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ecru Natural Linen",
                "color_hex": "#E8E2D5",
                "sku": "AUR-023-M-ECR",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ecru Natural Linen",
                "color_hex": "#E8E2D5",
                "sku": "AUR-023-L-ECR",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ecru Natural Linen",
                "color_hex": "#E8E2D5",
                "sku": "AUR-023-XL-ECR",
                "stock_quantity": 40,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Slate",
                "color_hex": "#343A40",
                "sku": "AUR-023-XS-CHA",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Slate",
                "color_hex": "#343A40",
                "sku": "AUR-023-S-CHA",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Slate",
                "color_hex": "#343A40",
                "sku": "AUR-023-M-CHA",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Slate",
                "color_hex": "#343A40",
                "sku": "AUR-023-L-CHA",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Slate",
                "color_hex": "#343A40",
                "sku": "AUR-023-XL-CHA",
                "stock_quantity": 36,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 24,
        "name": "Okayama 14oz Vintage Straight Jeans",
        "slug": "denim-jeans-24-cf33e",
        "description": "Crafted in Kojima, Japan from 14oz shuttle-loomed selvedge denim. Detailed with red-line selvedge ID, custom copper hardware, and genuine button fly.",
        "category_id": 11,
        "base_price": 6999.0,
        "discount_price": 5899.0,
        "brand": "Aura Haute Collection",
        "material": "100% Long-Staple Japanese Cotton",
        "fit_type": "Classic Straight Leg",
        "care_instructions": "Wash sparingly inside out in cold water",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.5,
        "review_count": 9,
        "sales_count": 109,
        "created_at": "2026-11-06 17:42:14.543959",
        "updated_at": "2026-11-06 17:42:14.543959",
        "category_slug": "selvedge-denim",
        "images": [
            {
                "image_url": "/images/products/okayama-14oz-vintage-straight-jeans-vintage-light-indigo.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/okayama-14oz-vintage-straight-jeans-dark-selvedge-indigo.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Vintage Light Indigo",
                "color_hex": "#5B84B1",
                "sku": "AUR-024-XS-VIN",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Vintage Light Indigo",
                "color_hex": "#5B84B1",
                "sku": "AUR-024-S-VIN",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Vintage Light Indigo",
                "color_hex": "#5B84B1",
                "sku": "AUR-024-M-VIN",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Vintage Light Indigo",
                "color_hex": "#5B84B1",
                "sku": "AUR-024-L-VIN",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Vintage Light Indigo",
                "color_hex": "#5B84B1",
                "sku": "AUR-024-XL-VIN",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Dark Selvedge Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-024-XS-DAR",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Dark Selvedge Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-024-S-DAR",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Dark Selvedge Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-024-M-DAR",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Dark Selvedge Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-024-L-DAR",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Dark Selvedge Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-024-XL-DAR",
                "stock_quantity": 20,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 25,
        "name": "Kuroki Raw Indigo Slim-Taper Jeans",
        "slug": "denim-jeans-25-99869",
        "description": "Tailored from 13.5oz rope-dyed Kuroki Mills raw denim. Starts crisp and molds to your body, developing personalized honeycombs and whiskers.",
        "category_id": 11,
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "Aura Haute Collection",
        "material": "99% Japanese Selvedge Cotton, 1% Comfort Stretch",
        "fit_type": "Slim Tapered",
        "care_instructions": "Cold soak, line dry",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 17,
        "sales_count": 35,
        "created_at": "2026-11-06 17:42:14.547479",
        "updated_at": "2026-11-06 17:42:14.547479",
        "category_slug": "selvedge-denim",
        "images": [
            {
                "image_url": "/images/products/kuroki-raw-indigo-slim-taper-jeans-raw-dark-indigo.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/kuroki-raw-indigo-slim-taper-jeans-washed-charcoal-black.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Raw Dark Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-025-XS-RAW",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Raw Dark Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-025-S-RAW",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Raw Dark Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-025-M-RAW",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Raw Dark Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-025-L-RAW",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Raw Dark Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-025-XL-RAW",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Washed Charcoal Black",
                "color_hex": "#2F3136",
                "sku": "AUR-025-XS-WAS",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Washed Charcoal Black",
                "color_hex": "#2F3136",
                "sku": "AUR-025-S-WAS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Washed Charcoal Black",
                "color_hex": "#2F3136",
                "sku": "AUR-025-M-WAS",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Washed Charcoal Black",
                "color_hex": "#2F3136",
                "sku": "AUR-025-L-WAS",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Washed Charcoal Black",
                "color_hex": "#2F3136",
                "sku": "AUR-025-XL-WAS",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 26,
        "name": "Relaxed 90s Heritage Stonewash Jeans",
        "slug": "denim-jeans-26-a4ee4",
        "description": "Authentic loose silhouette inspired by iconic 90s casualwear. Cut from 100% regenerative ring-spun cotton denim with vintage stonewashing.",
        "category_id": 12,
        "base_price": 5299.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% Regenerative Cotton Denim",
        "fit_type": "Relaxed 90s Straight",
        "care_instructions": "Machine wash cold",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 12,
        "sales_count": 102,
        "created_at": "2026-11-06 17:42:14.550479",
        "updated_at": "2026-11-06 17:42:14.550479",
        "category_slug": "designer-jeans",
        "images": [
            {
                "image_url": "/images/products/relaxed-90s-heritage-stonewash-jeans-stonewash-sky-blue.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/relaxed-90s-heritage-stonewash-jeans-vintage-light-indigo.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Stonewash Sky Blue",
                "color_hex": "#7DA0CA",
                "sku": "AUR-026-XS-STO",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Stonewash Sky Blue",
                "color_hex": "#7DA0CA",
                "sku": "AUR-026-S-STO",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Stonewash Sky Blue",
                "color_hex": "#7DA0CA",
                "sku": "AUR-026-M-STO",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Stonewash Sky Blue",
                "color_hex": "#7DA0CA",
                "sku": "AUR-026-L-STO",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Stonewash Sky Blue",
                "color_hex": "#7DA0CA",
                "sku": "AUR-026-XL-STO",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Vintage Light Indigo",
                "color_hex": "#5B84B1",
                "sku": "AUR-026-XS-VIN",
                "stock_quantity": 30,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Vintage Light Indigo",
                "color_hex": "#5B84B1",
                "sku": "AUR-026-S-VIN",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Vintage Light Indigo",
                "color_hex": "#5B84B1",
                "sku": "AUR-026-M-VIN",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Vintage Light Indigo",
                "color_hex": "#5B84B1",
                "sku": "AUR-026-L-VIN",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Vintage Light Indigo",
                "color_hex": "#5B84B1",
                "sku": "AUR-026-XL-VIN",
                "stock_quantity": 33,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 27,
        "name": "Heavyweight 450 GSM Organic Cotton Hoodie",
        "slug": "loungewear-27-10ca6",
        "description": "Crafted from ultra-dense 450 GSM organic French terry cotton. Features double-layered hood, flatlock stitching, and ribbed side mobility gussets.",
        "category_id": 13,
        "base_price": 4299.0,
        "discount_price": 3499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Combed Organic Cotton",
        "fit_type": "Relaxed Boxy Fit",
        "care_instructions": "Machine wash warm, tumble dry low",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 10,
        "sales_count": 38,
        "created_at": "2026-11-06 17:42:14.551994",
        "updated_at": "2026-11-06 17:42:14.551994",
        "category_slug": "cashmere-loungewear",
        "images": [
            {
                "image_url": "/images/products/heavyweight-450-gsm-organic-cotton-hoodie-heather-grey-melange.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/heavyweight-450-gsm-organic-cotton-hoodie-oatmeal-natural.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Heather Grey Melange",
                "color_hex": "#9E9E9E",
                "sku": "AUR-027-XS-HEA",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Heather Grey Melange",
                "color_hex": "#9E9E9E",
                "sku": "AUR-027-S-HEA",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Heather Grey Melange",
                "color_hex": "#9E9E9E",
                "sku": "AUR-027-M-HEA",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Heather Grey Melange",
                "color_hex": "#9E9E9E",
                "sku": "AUR-027-L-HEA",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Heather Grey Melange",
                "color_hex": "#9E9E9E",
                "sku": "AUR-027-XL-HEA",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Oatmeal Natural",
                "color_hex": "#E5DEC9",
                "sku": "AUR-027-XS-OAT",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Oatmeal Natural",
                "color_hex": "#E5DEC9",
                "sku": "AUR-027-S-OAT",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Oatmeal Natural",
                "color_hex": "#E5DEC9",
                "sku": "AUR-027-M-OAT",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Oatmeal Natural",
                "color_hex": "#E5DEC9",
                "sku": "AUR-027-L-OAT",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Oatmeal Natural",
                "color_hex": "#E5DEC9",
                "sku": "AUR-027-XL-OAT",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 28,
        "name": "Organic Loopback French Terry Sweatpants",
        "slug": "loungewear-28-46530",
        "description": "Plush loopback organic cotton joggers with a drawstring elastic waist, tailored slanted welt pockets, and comfortable ribbed cuffs.",
        "category_id": 13,
        "base_price": 3699.0,
        "discount_price": 2999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Organic French Terry Cotton",
        "fit_type": "Relaxed Tapered Fit",
        "care_instructions": "Machine wash cold with like colors",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 16,
        "sales_count": 68,
        "created_at": "2026-11-06 17:42:14.556042",
        "updated_at": "2026-11-06 17:42:14.556042",
        "category_slug": "cashmere-loungewear",
        "images": [
            {
                "image_url": "/images/products/organic-loopback-french-terry-sweatpants-oatmeal-natural.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/organic-loopback-french-terry-sweatpants-heather-grey-melange.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Oatmeal Natural",
                "color_hex": "#E5DEC9",
                "sku": "AUR-028-XS-OAT",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Oatmeal Natural",
                "color_hex": "#E5DEC9",
                "sku": "AUR-028-S-OAT",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Oatmeal Natural",
                "color_hex": "#E5DEC9",
                "sku": "AUR-028-M-OAT",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Oatmeal Natural",
                "color_hex": "#E5DEC9",
                "sku": "AUR-028-L-OAT",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Oatmeal Natural",
                "color_hex": "#E5DEC9",
                "sku": "AUR-028-XL-OAT",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Heather Grey Melange",
                "color_hex": "#9E9E9E",
                "sku": "AUR-028-XS-HEA",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Heather Grey Melange",
                "color_hex": "#9E9E9E",
                "sku": "AUR-028-S-HEA",
                "stock_quantity": 40,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Heather Grey Melange",
                "color_hex": "#9E9E9E",
                "sku": "AUR-028-M-HEA",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Heather Grey Melange",
                "color_hex": "#9E9E9E",
                "sku": "AUR-028-L-HEA",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Heather Grey Melange",
                "color_hex": "#9E9E9E",
                "sku": "AUR-028-XL-HEA",
                "stock_quantity": 20,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 29,
        "name": "Seamless Ribbed Compression Workout Set",
        "slug": "activewear-29-f47f7",
        "description": "High-performance moisture-wicking four-way stretch fabric with targeted muscle support, zero-chafe flat seams, and breathable ventilation zones.",
        "category_id": 15,
        "base_price": 4499.0,
        "discount_price": 3699.0,
        "brand": "Aura Haute Collection",
        "material": "78% Recycled Polyamide, 22% Elastane",
        "fit_type": "Athletic Compression Fit",
        "care_instructions": "Machine wash cold, line dry",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.4,
        "review_count": 21,
        "sales_count": 42,
        "created_at": "2026-11-06 17:42:14.558561",
        "updated_at": "2026-11-06 17:42:14.558561",
        "category_slug": "haute-activewear",
        "images": [
            {
                "image_url": "/images/products/seamless-ribbed-compression-workout-set-dusty-rose-pink.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/seamless-ribbed-compression-workout-set-olive-green.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Dusty Rose Pink",
                "color_hex": "#D8A47F",
                "sku": "AUR-029-XS-DUS",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Dusty Rose Pink",
                "color_hex": "#D8A47F",
                "sku": "AUR-029-S-DUS",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Dusty Rose Pink",
                "color_hex": "#D8A47F",
                "sku": "AUR-029-M-DUS",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Dusty Rose Pink",
                "color_hex": "#D8A47F",
                "sku": "AUR-029-L-DUS",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Dusty Rose Pink",
                "color_hex": "#D8A47F",
                "sku": "AUR-029-XL-DUS",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Olive Green",
                "color_hex": "#556B2F",
                "sku": "AUR-029-XS-OLI",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Olive Green",
                "color_hex": "#556B2F",
                "sku": "AUR-029-S-OLI",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Olive Green",
                "color_hex": "#556B2F",
                "sku": "AUR-029-M-OLI",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Olive Green",
                "color_hex": "#556B2F",
                "sku": "AUR-029-L-OLI",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Olive Green",
                "color_hex": "#556B2F",
                "sku": "AUR-029-XL-OLI",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 30,
        "name": "AeroShield Ultralight Performance Windbreaker",
        "slug": "activewear-30-bed78",
        "description": "Featherweight technical ripstop running jacket with DWR water-repellent coating, underarm ventilation eyelets, and packable pocket.",
        "category_id": 16,
        "base_price": 4999.0,
        "discount_price": 3999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Recycled Ripstop Nylon",
        "fit_type": "Athletic Slim Fit",
        "care_instructions": "Machine wash cold gentle",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.5,
        "review_count": 18,
        "sales_count": 63,
        "created_at": "2026-11-06 17:42:14.563832",
        "updated_at": "2026-11-06 17:42:14.563832",
        "category_slug": "technical-performance",
        "images": [
            {
                "image_url": "/images/products/aeroshield-ultralight-performance-windbreaker-olive-sage.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/aeroshield-ultralight-performance-windbreaker-midnight-stealth-black.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Olive Sage",
                "color_hex": "#556B2F",
                "sku": "AUR-030-XS-OLI",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Olive Sage",
                "color_hex": "#556B2F",
                "sku": "AUR-030-S-OLI",
                "stock_quantity": 30,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Olive Sage",
                "color_hex": "#556B2F",
                "sku": "AUR-030-M-OLI",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Olive Sage",
                "color_hex": "#556B2F",
                "sku": "AUR-030-L-OLI",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Olive Sage",
                "color_hex": "#556B2F",
                "sku": "AUR-030-XL-OLI",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Midnight Stealth Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-030-XS-MID",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Stealth Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-030-S-MID",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Stealth Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-030-M-MID",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Stealth Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-030-L-MID",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Stealth Black",
                "color_hex": "#1A1A1A",
                "sku": "AUR-030-XL-MID",
                "stock_quantity": 32,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 31,
        "name": "Pre-Washed Normandy Linen Drawstring Trousers",
        "slug": "summer-linen-31-f66bc",
        "description": "Airy, relaxed-leg trousers with an elasticated drawstring waist and breathable open weave. Garment-washed for a soft touch and effortless drape.",
        "category_id": 20,
        "base_price": 4499.0,
        "discount_price": 3799.0,
        "brand": "Aura Haute Collection",
        "material": "100% European Flax Linen",
        "fit_type": "Relaxed Straight Fit",
        "care_instructions": "Machine wash cold gentle, line dry",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 27,
        "sales_count": 93,
        "created_at": "2026-11-06 17:42:14.566489",
        "updated_at": "2026-11-06 17:42:14.566489",
        "category_slug": "linen-resortwear",
        "images": [
            {
                "image_url": "/images/products/pre-washed-normandy-linen-drawstring-trousers-natural-oatmeal-linen.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/pre-washed-normandy-linen-drawstring-trousers-belgian-ecru-linen.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Natural Oatmeal Linen",
                "color_hex": "#E5DEC9",
                "sku": "AUR-031-XS-NAT",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Natural Oatmeal Linen",
                "color_hex": "#E5DEC9",
                "sku": "AUR-031-S-NAT",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Natural Oatmeal Linen",
                "color_hex": "#E5DEC9",
                "sku": "AUR-031-M-NAT",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Natural Oatmeal Linen",
                "color_hex": "#E5DEC9",
                "sku": "AUR-031-L-NAT",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Natural Oatmeal Linen",
                "color_hex": "#E5DEC9",
                "sku": "AUR-031-XL-NAT",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Belgian Ecru Linen",
                "color_hex": "#D8D2C2",
                "sku": "AUR-031-XS-BEL",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Belgian Ecru Linen",
                "color_hex": "#D8D2C2",
                "sku": "AUR-031-S-BEL",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Belgian Ecru Linen",
                "color_hex": "#D8D2C2",
                "sku": "AUR-031-M-BEL",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Belgian Ecru Linen",
                "color_hex": "#D8D2C2",
                "sku": "AUR-031-L-BEL",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Belgian Ecru Linen",
                "color_hex": "#D8D2C2",
                "sku": "AUR-031-XL-BEL",
                "stock_quantity": 31,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 32,
        "name": "European Flax Sleeveless Linen Jumpsuit",
        "slug": "summer-linen-32-3728f",
        "description": "Wide-leg minimalist jumpsuit cut from 100% French flax linen. Features a flattering square neckline, removable belt, and concealed back zip.",
        "category_id": 20,
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Certified European Flax Linen",
        "fit_type": "Wide-Leg Jumpsuit",
        "care_instructions": "Machine wash cold delicate",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.6,
        "review_count": 16,
        "sales_count": 109,
        "created_at": "2026-11-06 17:42:14.569212",
        "updated_at": "2026-11-06 17:42:14.569212",
        "category_slug": "linen-resortwear",
        "images": [
            {
                "image_url": "/images/products/european-flax-sleeveless-linen-jumpsuit-oatmeal-natural.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/european-flax-sleeveless-linen-jumpsuit-sage-olive.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Oatmeal Natural",
                "color_hex": "#D8CBB5",
                "sku": "AUR-032-XS-OAT",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Oatmeal Natural",
                "color_hex": "#D8CBB5",
                "sku": "AUR-032-S-OAT",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Oatmeal Natural",
                "color_hex": "#D8CBB5",
                "sku": "AUR-032-M-OAT",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Oatmeal Natural",
                "color_hex": "#D8CBB5",
                "sku": "AUR-032-L-OAT",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Oatmeal Natural",
                "color_hex": "#D8CBB5",
                "sku": "AUR-032-XL-OAT",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Sage Olive",
                "color_hex": "#6B7C59",
                "sku": "AUR-032-XS-SAG",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Sage Olive",
                "color_hex": "#6B7C59",
                "sku": "AUR-032-S-SAG",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Sage Olive",
                "color_hex": "#6B7C59",
                "sku": "AUR-032-M-SAG",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Sage Olive",
                "color_hex": "#6B7C59",
                "sku": "AUR-032-L-SAG",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Sage Olive",
                "color_hex": "#6B7C59",
                "sku": "AUR-032-XL-SAG",
                "stock_quantity": 20,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 33,
        "name": "Tuscan Calfskin Blake-Stitched Chelsea Boots",
        "slug": "footwear-33-43550",
        "description": "Artisan-crafted in Tuscany from vegetable-tanned Italian calfskin. Features flexible elastic side gussets, woven pull loops, and a resoleable Vibram rubber sole.",
        "category_id": 21,
        "base_price": 11499.0,
        "discount_price": 9499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Full-Grain Tuscan Calfskin",
        "fit_type": "Standard D Width / True to Size",
        "care_instructions": "Condition with leather balm regularly",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 22,
        "sales_count": 91,
        "created_at": "2026-11-06 17:42:14.573032",
        "updated_at": "2026-11-06 17:42:14.573032",
        "category_slug": "leather-boots",
        "images": [
            {
                "image_url": "/images/products/tuscan-calfskin-blake-stitched-chelsea-boots-cognac-tan-leather.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/tuscan-calfskin-blake-stitched-chelsea-boots-noir-black-leather.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Cognac Tan Leather",
                "color_hex": "#9E5B32",
                "sku": "AUR-033-XS-COG",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Cognac Tan Leather",
                "color_hex": "#9E5B32",
                "sku": "AUR-033-S-COG",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Cognac Tan Leather",
                "color_hex": "#9E5B32",
                "sku": "AUR-033-M-COG",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Cognac Tan Leather",
                "color_hex": "#9E5B32",
                "sku": "AUR-033-L-COG",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Cognac Tan Leather",
                "color_hex": "#9E5B32",
                "sku": "AUR-033-XL-COG",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-033-XS-NOI",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-033-S-NOI",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-033-M-NOI",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-033-L-NOI",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-033-XL-NOI",
                "stock_quantity": 18,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 34,
        "name": "Minimalist Full-Grain Italian Nappa Sneakers",
        "slug": "footwear-34-3023a",
        "description": "Clean, understated court sneaker handmade from buttery Italian nappa leather with soft calfskin lining, waxed laces, and durable Margom cupsole.",
        "category_id": 22,
        "base_price": 7999.0,
        "discount_price": 6499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Italian Nappa Leather",
        "fit_type": "True to Size",
        "care_instructions": "Wipe clean with a damp cloth",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.6,
        "review_count": 22,
        "sales_count": 41,
        "created_at": "2026-11-06 17:42:14.579195",
        "updated_at": "2026-11-06 17:42:14.579195",
        "category_slug": "dress-shoes-loafers",
        "images": [
            {
                "image_url": "/images/products/minimalist-full-grain-italian-nappa-sneakers-optic-white-nappa.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/minimalist-full-grain-italian-nappa-sneakers-noir-black-leather.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Optic White Nappa",
                "color_hex": "#F8F9FA",
                "sku": "AUR-034-XS-OPT",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Optic White Nappa",
                "color_hex": "#F8F9FA",
                "sku": "AUR-034-S-OPT",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Optic White Nappa",
                "color_hex": "#F8F9FA",
                "sku": "AUR-034-M-OPT",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Optic White Nappa",
                "color_hex": "#F8F9FA",
                "sku": "AUR-034-L-OPT",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Optic White Nappa",
                "color_hex": "#F8F9FA",
                "sku": "AUR-034-XL-OPT",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-034-XS-NOI",
                "stock_quantity": 36,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-034-S-NOI",
                "stock_quantity": 39,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-034-M-NOI",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-034-L-NOI",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-034-XL-NOI",
                "stock_quantity": 16,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 35,
        "name": "Tuscan Vacchetta Leather Heritage Weekend Tote",
        "slug": "accessories-35-fade0",
        "description": "Spacious travel tote crafted from full-grain vegetable-tanned vacchetta leather that develops rich patina. Rolled handles and heavy solid brass hardware.",
        "category_id": 23,
        "base_price": 9999.0,
        "discount_price": 8299.0,
        "brand": "Aura Haute Collection",
        "material": "100% Full-Grain Tuscan Vacchetta Leather",
        "fit_type": "42cm x 36cm x 16cm",
        "care_instructions": "Protect from standing water; condition periodically",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 16,
        "sales_count": 71,
        "created_at": "2026-11-06 17:42:14.582230",
        "updated_at": "2026-11-06 17:42:14.582230",
        "category_slug": "leather-bags-luggage",
        "images": [
            {
                "image_url": "/images/products/tuscan-vacchetta-leather-heritage-weekend-tote-cognac-saddle-leather.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/tuscan-vacchetta-leather-heritage-weekend-tote-noir-black-leather.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Cognac Saddle Leather",
                "color_hex": "#8B4513",
                "sku": "AUR-035-XS-COG",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Cognac Saddle Leather",
                "color_hex": "#8B4513",
                "sku": "AUR-035-S-COG",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Cognac Saddle Leather",
                "color_hex": "#8B4513",
                "sku": "AUR-035-M-COG",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Cognac Saddle Leather",
                "color_hex": "#8B4513",
                "sku": "AUR-035-L-COG",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Cognac Saddle Leather",
                "color_hex": "#8B4513",
                "sku": "AUR-035-XL-COG",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-035-XS-NOI",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-035-S-NOI",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-035-M-NOI",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-035-L-NOI",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-035-XL-NOI",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 36,
        "name": "Full-Grain Pebble Leather Executive Briefcase",
        "slug": "accessories-36-8eb7e",
        "description": "Refined slim briefcase constructed from scratch-resistant full-grain pebble leather. Features padded 15-inch laptop compartment and detachable shoulder strap.",
        "category_id": 23,
        "base_price": 10999.0,
        "discount_price": 8999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Full-Grain Pebble Cowhide",
        "fit_type": "40cm x 30cm x 8cm",
        "care_instructions": "Wipe clean with microfiber cloth",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 10,
        "sales_count": 118,
        "created_at": "2026-11-06 17:42:14.585748",
        "updated_at": "2026-11-06 17:42:14.585748",
        "category_slug": "leather-bags-luggage",
        "images": [
            {
                "image_url": "/images/products/full-grain-pebble-leather-executive-briefcase-noir-black-leather.jpg",
                "is_primary": 1,
                "display_order": 1
            },
            {
                "image_url": "/images/products/full-grain-pebble-leather-executive-briefcase-cognac-saddle-leather.jpg",
                "is_primary": 0,
                "display_order": 2
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-036-XS-NOI",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-036-S-NOI",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-036-M-NOI",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-036-L-NOI",
                "stock_quantity": 38,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Noir Black Leather",
                "color_hex": "#1A1A1A",
                "sku": "AUR-036-XL-NOI",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Cognac Saddle Leather",
                "color_hex": "#8B4513",
                "sku": "AUR-036-XS-COG",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Cognac Saddle Leather",
                "color_hex": "#8B4513",
                "sku": "AUR-036-S-COG",
                "stock_quantity": 30,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Cognac Saddle Leather",
                "color_hex": "#8B4513",
                "sku": "AUR-036-M-COG",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Cognac Saddle Leather",
                "color_hex": "#8B4513",
                "sku": "AUR-036-L-COG",
                "stock_quantity": 37,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Cognac Saddle Leather",
                "color_hex": "#8B4513",
                "sku": "AUR-036-XL-COG",
                "stock_quantity": 33,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 37,
        "name": "Pleated Silk Georgette Evening Gown",
        "slug": "womens-dresses-pleated-silk-georgette-evening-534",
        "description": "Floor-sweeping gown in airy 100% silk georgette with hand-pressed sunburst pleating, an open architectural back, and internal silk habotai slip lining.",
        "category_id": 1,
        "base_price": 14999.0,
        "discount_price": 12999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Silk Georgette, 100% Silk Habotai Lining",
        "fit_type": "Fluid Empire Silhouette",
        "care_instructions": "Specialist luxury dry clean only",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 8,
        "sales_count": 108,
        "created_at": "2026-11-11 10:38:51.931521",
        "updated_at": "2026-11-11 10:38:51.931521",
        "category_slug": "evening-gowns",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Emerald Green",
                "color_hex": "#1B4D3E",
                "sku": "AUR-0037-XS-EME",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Emerald Green",
                "color_hex": "#1B4D3E",
                "sku": "AUR-0037-S-EME",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Emerald Green",
                "color_hex": "#1B4D3E",
                "sku": "AUR-0037-M-EME",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Emerald Green",
                "color_hex": "#1B4D3E",
                "sku": "AUR-0037-L-EME",
                "stock_quantity": 30,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Emerald Green",
                "color_hex": "#1B4D3E",
                "sku": "AUR-0037-XL-EME",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Midnight Noir",
                "color_hex": "#0A0A0A",
                "sku": "AUR-0037-XS-MID",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Noir",
                "color_hex": "#0A0A0A",
                "sku": "AUR-0037-S-MID",
                "stock_quantity": 30,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Noir",
                "color_hex": "#0A0A0A",
                "sku": "AUR-0037-M-MID",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Noir",
                "color_hex": "#0A0A0A",
                "sku": "AUR-0037-L-MID",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Noir",
                "color_hex": "#0A0A0A",
                "sku": "AUR-0037-XL-MID",
                "stock_quantity": 26,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 38,
        "name": "Sculptural Structured Crepe Midi Dress",
        "slug": "womens-dresses-sculptural-structured-crepe-mi-596",
        "description": "Sleek column midi dress crafted from double-weave bonded stretch crepe with asymmetric split neckline, bustier interior boning, and deep side slit.",
        "category_id": 2,
        "base_price": 11499.0,
        "discount_price": 9899.0,
        "brand": "Aura Haute Collection",
        "material": "68% Wool Crepe, 28% Silk, 4% Elastane",
        "fit_type": "Architectural Tailored Fit",
        "care_instructions": "Dry clean only",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 22,
        "sales_count": 90,
        "created_at": "2026-11-11 10:38:51.941825",
        "updated_at": "2026-11-11 10:38:51.941825",
        "category_slug": "cocktail-day-dresses",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Alabaster Ivory",
                "color_hex": "#F8F6F0",
                "sku": "AUR-0038-XS-ALA",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Alabaster Ivory",
                "color_hex": "#F8F6F0",
                "sku": "AUR-0038-S-ALA",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Alabaster Ivory",
                "color_hex": "#F8F6F0",
                "sku": "AUR-0038-M-ALA",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Alabaster Ivory",
                "color_hex": "#F8F6F0",
                "sku": "AUR-0038-L-ALA",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Alabaster Ivory",
                "color_hex": "#F8F6F0",
                "sku": "AUR-0038-XL-ALA",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Noir Black",
                "color_hex": "#141414",
                "sku": "AUR-0038-XS-NOI",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Noir Black",
                "color_hex": "#141414",
                "sku": "AUR-0038-S-NOI",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Noir Black",
                "color_hex": "#141414",
                "sku": "AUR-0038-M-NOI",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Noir Black",
                "color_hex": "#141414",
                "sku": "AUR-0038-L-NOI",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Noir Black",
                "color_hex": "#141414",
                "sku": "AUR-0038-XL-NOI",
                "stock_quantity": 22,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 39,
        "name": "Broderie Anglaise Tiered Linen Sun Dress",
        "slug": "womens-dresses-broderie-anglaise-tiered-linen-621",
        "description": "Artisan sun dress in certified European flax with delicate floral eyelet cutwork embroidery, gathered tiered skirt, and mother-of-pearl back button closure.",
        "category_id": 2,
        "base_price": 8999.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% European Flax Linen with Cotton Embroidery",
        "fit_type": "Relaxed Tiered Silhouette",
        "care_instructions": "Machine wash delicate cycle in garment bag; line dry",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 22,
        "sales_count": 96,
        "created_at": "2026-11-11 10:38:51.945304",
        "updated_at": "2026-11-11 10:38:51.945304",
        "category_slug": "cocktail-day-dresses",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Optic White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-0039-XS-OPT",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Optic White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-0039-S-OPT",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Optic White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-0039-M-OPT",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Optic White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-0039-L-OPT",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Optic White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-0039-XL-OPT",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Warm Sandstone",
                "color_hex": "#D2B48C",
                "sku": "AUR-0039-XS-WAR",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Warm Sandstone",
                "color_hex": "#D2B48C",
                "sku": "AUR-0039-S-WAR",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Warm Sandstone",
                "color_hex": "#D2B48C",
                "sku": "AUR-0039-M-WAR",
                "stock_quantity": 11,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Warm Sandstone",
                "color_hex": "#D2B48C",
                "sku": "AUR-0039-L-WAR",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Warm Sandstone",
                "color_hex": "#D2B48C",
                "sku": "AUR-0039-XL-WAR",
                "stock_quantity": 25,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 40,
        "name": "Giza 87 Egyptian Cotton Spread Collar Shirt",
        "slug": "mens-shirts-giza-87-egyptian-cotton-spread-453",
        "description": "Exquisitely tailored from extra-long staple Egyptian Giza 87 cotton with 140s two-ply yarn, Australian mother-of-pearl buttons, and hand-turned semi-spread collar.",
        "category_id": 3,
        "base_price": 5499.0,
        "discount_price": 4699.0,
        "brand": "Aura Haute Collection",
        "material": "100% Giza 87 Egyptian Cotton",
        "fit_type": "Tailored Contemporary Fit",
        "care_instructions": "Machine wash warm, hang dry, warm steam iron",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 16,
        "sales_count": 139,
        "created_at": "2026-11-11 10:38:51.947495",
        "updated_at": "2026-11-11 10:38:51.947495",
        "category_slug": "formal-dress-shirts",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Sky Blue Oxford",
                "color_hex": "#B0C4DE",
                "sku": "AUR-0040-XS-SKY",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Sky Blue Oxford",
                "color_hex": "#B0C4DE",
                "sku": "AUR-0040-S-SKY",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Sky Blue Oxford",
                "color_hex": "#B0C4DE",
                "sku": "AUR-0040-M-SKY",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Sky Blue Oxford",
                "color_hex": "#B0C4DE",
                "sku": "AUR-0040-L-SKY",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Sky Blue Oxford",
                "color_hex": "#B0C4DE",
                "sku": "AUR-0040-XL-SKY",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Crisp White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-0040-XS-CRI",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Crisp White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-0040-S-CRI",
                "stock_quantity": 11,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Crisp White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-0040-M-CRI",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Crisp White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-0040-L-CRI",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Crisp White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-0040-XL-CRI",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 41,
        "name": "Tuscan Silk-Linen Textured Resort Shirt",
        "slug": "mens-shirts-tuscan-silk-linen-textured-res-865",
        "description": "Breathable blend of mulberry silk and slubbed Italian linen featuring an open camp collar, side vents, and a tactile honeycomb micro-texture.",
        "category_id": 4,
        "base_price": 4899.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "55% Italian Linen, 45% Mulberry Silk",
        "fit_type": "Relaxed Resort Fit",
        "care_instructions": "Hand wash or gentle cold cycle",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 24,
        "sales_count": 102,
        "created_at": "2026-11-11 10:38:51.949762",
        "updated_at": "2026-11-11 10:38:51.949762",
        "category_slug": "luxury-polos-shirts",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Terracotta Clay",
                "color_hex": "#C05A46",
                "sku": "AUR-0041-XS-TER",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Terracotta Clay",
                "color_hex": "#C05A46",
                "sku": "AUR-0041-S-TER",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Terracotta Clay",
                "color_hex": "#C05A46",
                "sku": "AUR-0041-M-TER",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Terracotta Clay",
                "color_hex": "#C05A46",
                "sku": "AUR-0041-L-TER",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Terracotta Clay",
                "color_hex": "#C05A46",
                "sku": "AUR-0041-XL-TER",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Olive Sage",
                "color_hex": "#556B2F",
                "sku": "AUR-0041-XS-OLI",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Olive Sage",
                "color_hex": "#556B2F",
                "sku": "AUR-0041-S-OLI",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Olive Sage",
                "color_hex": "#556B2F",
                "sku": "AUR-0041-M-OLI",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Olive Sage",
                "color_hex": "#556B2F",
                "sku": "AUR-0041-L-OLI",
                "stock_quantity": 8,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Olive Sage",
                "color_hex": "#556B2F",
                "sku": "AUR-0041-XL-OLI",
                "stock_quantity": 13,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 42,
        "name": "Mercerized Sea Island Cotton Polo",
        "slug": "mens-shirts-mercerized-sea-island-cotton-p-860",
        "description": "Spun from genuine West Indian Sea Island cotton treated with double mercerization for a luminous silk sheen, resistance to pilling, and enduring softness.",
        "category_id": 4,
        "base_price": 3999.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% Certified Sea Island Cotton",
        "fit_type": "Classic Athletic Fit",
        "care_instructions": "Machine wash cold inside out",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 17,
        "sales_count": 75,
        "created_at": "2026-11-11 10:38:51.952018",
        "updated_at": "2026-11-11 10:38:51.952018",
        "category_slug": "luxury-polos-shirts",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#800020",
                "sku": "AUR-0042-XS-BUR",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#800020",
                "sku": "AUR-0042-S-BUR",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#800020",
                "sku": "AUR-0042-M-BUR",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#800020",
                "sku": "AUR-0042-L-BUR",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Burgundy Wine",
                "color_hex": "#800020",
                "sku": "AUR-0042-XL-BUR",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Forest Green",
                "color_hex": "#228B22",
                "sku": "AUR-0042-XS-FOR",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Green",
                "color_hex": "#228B22",
                "sku": "AUR-0042-S-FOR",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Green",
                "color_hex": "#228B22",
                "sku": "AUR-0042-M-FOR",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Green",
                "color_hex": "#228B22",
                "sku": "AUR-0042-L-FOR",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Green",
                "color_hex": "#228B22",
                "sku": "AUR-0042-XL-FOR",
                "stock_quantity": 28,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 43,
        "name": "Houndstooth Harris Tweed Heritage Blazer",
        "slug": "blazers-coats-houndstooth-harris-tweed-herit-305",
        "description": "Handwoven pure virgin wool from the Outer Hebrides of Scotland. Tailored with soft Neapolitan shoulders, horn buttons, elbow patches, and dual back vents.",
        "category_id": 5,
        "base_price": 16999.0,
        "discount_price": 14499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Genuine Harris Tweed Virgin Wool",
        "fit_type": "Tailored Heritage Fit",
        "care_instructions": "Specialist wool dry clean only",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 34,
        "sales_count": 28,
        "created_at": "2026-11-11 10:38:51.954020",
        "updated_at": "2026-11-11 10:38:51.954020",
        "category_slug": "tailored-blazers",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Chestnut Houndstooth",
                "color_hex": "#8B4513",
                "sku": "AUR-0043-XS-CHE",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Chestnut Houndstooth",
                "color_hex": "#8B4513",
                "sku": "AUR-0043-S-CHE",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Chestnut Houndstooth",
                "color_hex": "#8B4513",
                "sku": "AUR-0043-M-CHE",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Chestnut Houndstooth",
                "color_hex": "#8B4513",
                "sku": "AUR-0043-L-CHE",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Chestnut Houndstooth",
                "color_hex": "#8B4513",
                "sku": "AUR-0043-XL-CHE",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Tweed",
                "color_hex": "#36454F",
                "sku": "AUR-0043-XS-CHA",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Tweed",
                "color_hex": "#36454F",
                "sku": "AUR-0043-S-CHA",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Tweed",
                "color_hex": "#36454F",
                "sku": "AUR-0043-M-CHA",
                "stock_quantity": 9,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Tweed",
                "color_hex": "#36454F",
                "sku": "AUR-0043-L-CHA",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Tweed",
                "color_hex": "#36454F",
                "sku": "AUR-0043-XL-CHA",
                "stock_quantity": 8,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 44,
        "name": "Double-Breasted Linen-Silk Peak Lapel Jacket",
        "slug": "blazers-coats-double-breasted-linen-silk-pea-863",
        "description": "Impeccably tailored 6-on-2 double-breasted sport coat with wide peak lapels, barchetta chest pocket, and half-canvas unlined construction for warm climates.",
        "category_id": 5,
        "base_price": 15499.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "58% Belgian Linen, 42% Mulberry Silk",
        "fit_type": "Neapolitan Slim Fit",
        "care_instructions": "Professional dry clean",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 17,
        "sales_count": 76,
        "created_at": "2026-11-11 10:38:51.957024",
        "updated_at": "2026-11-11 10:38:51.957024",
        "category_slug": "tailored-blazers",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Natural Oatmeal",
                "color_hex": "#E8DFD0",
                "sku": "AUR-0044-XS-NAT",
                "stock_quantity": 8,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Natural Oatmeal",
                "color_hex": "#E8DFD0",
                "sku": "AUR-0044-S-NAT",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Natural Oatmeal",
                "color_hex": "#E8DFD0",
                "sku": "AUR-0044-M-NAT",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Natural Oatmeal",
                "color_hex": "#E8DFD0",
                "sku": "AUR-0044-L-NAT",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Natural Oatmeal",
                "color_hex": "#E8DFD0",
                "sku": "AUR-0044-XL-NAT",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Midnight Navy",
                "color_hex": "#000080",
                "sku": "AUR-0044-XS-MID",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Navy",
                "color_hex": "#000080",
                "sku": "AUR-0044-S-MID",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Navy",
                "color_hex": "#000080",
                "sku": "AUR-0044-M-MID",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Navy",
                "color_hex": "#000080",
                "sku": "AUR-0044-L-MID",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Navy",
                "color_hex": "#000080",
                "sku": "AUR-0044-XL-MID",
                "stock_quantity": 11,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 45,
        "name": "Cashmere-Blend Belted Wrap Overcoat",
        "slug": "blazers-coats-cashmere-blend-belted-wrap-ove-174",
        "description": "Sumptuous full-length wrap overcoat crafted in double-faced Italian cashmere-wool with exaggerated notched collar, kimono sleeves, and sash waist belt.",
        "category_id": 6,
        "base_price": 21999.0,
        "discount_price": 18999.0,
        "brand": "Aura Haute Collection",
        "material": "60% Mongolian Cashmere, 40% Fine Wool",
        "fit_type": "Relaxed Wrap Silhouette",
        "care_instructions": "Dry clean only; store with cedar hanger",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.6,
        "review_count": 11,
        "sales_count": 93,
        "created_at": "2026-11-11 10:38:51.959107",
        "updated_at": "2026-11-11 10:38:51.959107",
        "category_slug": "overcoats-trench",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Honey Camel",
                "color_hex": "#C19A6B",
                "sku": "AUR-0045-XS-HON",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Honey Camel",
                "color_hex": "#C19A6B",
                "sku": "AUR-0045-S-HON",
                "stock_quantity": 11,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Honey Camel",
                "color_hex": "#C19A6B",
                "sku": "AUR-0045-M-HON",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Honey Camel",
                "color_hex": "#C19A6B",
                "sku": "AUR-0045-L-HON",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Honey Camel",
                "color_hex": "#C19A6B",
                "sku": "AUR-0045-XL-HON",
                "stock_quantity": 10,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Charcoal Melange",
                "color_hex": "#2F4F4F",
                "sku": "AUR-0045-XS-CHA",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Melange",
                "color_hex": "#2F4F4F",
                "sku": "AUR-0045-S-CHA",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Melange",
                "color_hex": "#2F4F4F",
                "sku": "AUR-0045-M-CHA",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Melange",
                "color_hex": "#2F4F4F",
                "sku": "AUR-0045-L-CHA",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Melange",
                "color_hex": "#2F4F4F",
                "sku": "AUR-0045-XL-CHA",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 46,
        "name": "Waffle-Knit Cashmere Mock Neck Sweater",
        "slug": "knitwear-sweaters-waffle-knit-cashmere-mock-neck-346",
        "description": "Chunky tactile 5-gauge knit in 100% Grade-A Mongolian cashmere with ribbed mock neck, raglan sleeves, and tubular knitted cuffs.",
        "category_id": 8,
        "base_price": 11999.0,
        "discount_price": 9999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Grade-A Mongolian Cashmere",
        "fit_type": "Modern Relaxed Fit",
        "care_instructions": "Hand wash cold with cashmere wash; dry flat",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 13,
        "sales_count": 110,
        "created_at": "2026-11-11 10:38:51.960114",
        "updated_at": "2026-11-11 10:38:51.960114",
        "category_slug": "sweaters-cardigans",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Winter Ecru",
                "color_hex": "#F5F5DC",
                "sku": "AUR-0046-XS-WIN",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Winter Ecru",
                "color_hex": "#F5F5DC",
                "sku": "AUR-0046-S-WIN",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Winter Ecru",
                "color_hex": "#F5F5DC",
                "sku": "AUR-0046-M-WIN",
                "stock_quantity": 10,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Winter Ecru",
                "color_hex": "#F5F5DC",
                "sku": "AUR-0046-L-WIN",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Winter Ecru",
                "color_hex": "#F5F5DC",
                "sku": "AUR-0046-XL-WIN",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Heather Grey",
                "color_hex": "#808080",
                "sku": "AUR-0046-XS-HEA",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Heather Grey",
                "color_hex": "#808080",
                "sku": "AUR-0046-S-HEA",
                "stock_quantity": 9,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Heather Grey",
                "color_hex": "#808080",
                "sku": "AUR-0046-M-HEA",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Heather Grey",
                "color_hex": "#808080",
                "sku": "AUR-0046-L-HEA",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Heather Grey",
                "color_hex": "#808080",
                "sku": "AUR-0046-XL-HEA",
                "stock_quantity": 18,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 47,
        "name": "Cable-Stitch Fisherman Cardigan with Horn Buttons",
        "slug": "knitwear-sweaters-cable-stitch-fisherman-cardiga-348",
        "description": "Traditional Aran honeycomb and cable knit in heavy British lambswool. Finished with genuine water buffalo horn buttons and shawl collar.",
        "category_id": 8,
        "base_price": 8499.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% British Pure Lambswool",
        "fit_type": "Heritage Regular Fit",
        "care_instructions": "Hand wash cold; do not wring; dry flat",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 36,
        "sales_count": 87,
        "created_at": "2026-11-11 10:38:51.963414",
        "updated_at": "2026-11-11 10:38:51.963414",
        "category_slug": "sweaters-cardigans",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Oatmeal Melange",
                "color_hex": "#D8C7B5",
                "sku": "AUR-0047-XS-OAT",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Oatmeal Melange",
                "color_hex": "#D8C7B5",
                "sku": "AUR-0047-S-OAT",
                "stock_quantity": 30,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Oatmeal Melange",
                "color_hex": "#D8C7B5",
                "sku": "AUR-0047-M-OAT",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Oatmeal Melange",
                "color_hex": "#D8C7B5",
                "sku": "AUR-0047-L-OAT",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Oatmeal Melange",
                "color_hex": "#D8C7B5",
                "sku": "AUR-0047-XL-OAT",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Navy Twill",
                "color_hex": "#0B162A",
                "sku": "AUR-0047-XS-NAV",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Navy Twill",
                "color_hex": "#0B162A",
                "sku": "AUR-0047-S-NAV",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Navy Twill",
                "color_hex": "#0B162A",
                "sku": "AUR-0047-M-NAV",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Navy Twill",
                "color_hex": "#0B162A",
                "sku": "AUR-0047-L-NAV",
                "stock_quantity": 30,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Navy Twill",
                "color_hex": "#0B162A",
                "sku": "AUR-0047-XL-NAV",
                "stock_quantity": 10,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 48,
        "name": "Ultra-Fine Merino Silk Crewneck",
        "slug": "knitwear-sweaters-ultra-fine-merino-silk-crewnec-153",
        "description": "Featherweight 18-gauge luxury knit combining extra-fine Australian merino wool and mulberry silk. Smooth as second skin under tailored suiting.",
        "category_id": 7,
        "base_price": 6499.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "70% Extra-Fine Merino Wool, 30% Mulberry Silk",
        "fit_type": "Tailored Slim Fit",
        "care_instructions": "Hand wash or gentle wool cycle",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 9,
        "sales_count": 79,
        "created_at": "2026-11-11 10:38:51.965866",
        "updated_at": "2026-11-11 10:38:51.965866",
        "category_slug": "fine-knitwear",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1614975058789-41316d0e2e9c?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Bordeaux Wine",
                "color_hex": "#5B0E2D",
                "sku": "AUR-0048-XS-BOR",
                "stock_quantity": 11,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Bordeaux Wine",
                "color_hex": "#5B0E2D",
                "sku": "AUR-0048-S-BOR",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Bordeaux Wine",
                "color_hex": "#5B0E2D",
                "sku": "AUR-0048-M-BOR",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Bordeaux Wine",
                "color_hex": "#5B0E2D",
                "sku": "AUR-0048-L-BOR",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Bordeaux Wine",
                "color_hex": "#5B0E2D",
                "sku": "AUR-0048-XL-BOR",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Sage Olive",
                "color_hex": "#708238",
                "sku": "AUR-0048-XS-SAG",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Sage Olive",
                "color_hex": "#708238",
                "sku": "AUR-0048-S-SAG",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Sage Olive",
                "color_hex": "#708238",
                "sku": "AUR-0048-M-SAG",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Sage Olive",
                "color_hex": "#708238",
                "sku": "AUR-0048-L-SAG",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Sage Olive",
                "color_hex": "#708238",
                "sku": "AUR-0048-XL-SAG",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 49,
        "name": "Double-Pleated Biella Wool Wide-Leg Trousers",
        "slug": "trousers-chinos-double-pleated-biella-wool-wid-167",
        "description": "High-rise architectural trousers woven in Biella, Italy from 120s virgin wool. Features double reverse forward pleats, extended tab waistband, and side adjusters.",
        "category_id": 9,
        "base_price": 7999.0,
        "discount_price": 6799.0,
        "brand": "Aura Haute Collection",
        "material": "100% Biella Virgin Tropical Wool",
        "fit_type": "High-Rise Wide-Leg Drape",
        "care_instructions": "Dry clean only",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 10,
        "sales_count": 36,
        "created_at": "2026-11-11 10:38:51.966866",
        "updated_at": "2026-11-11 10:38:51.966866",
        "category_slug": "tailored-trousers",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Slate Grey Melange",
                "color_hex": "#708090",
                "sku": "AUR-0049-XS-SLA",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Grey Melange",
                "color_hex": "#708090",
                "sku": "AUR-0049-S-SLA",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Grey Melange",
                "color_hex": "#708090",
                "sku": "AUR-0049-M-SLA",
                "stock_quantity": 10,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Grey Melange",
                "color_hex": "#708090",
                "sku": "AUR-0049-L-SLA",
                "stock_quantity": 10,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Grey Melange",
                "color_hex": "#708090",
                "sku": "AUR-0049-XL-SLA",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Warm Taupe",
                "color_hex": "#B38B6D",
                "sku": "AUR-0049-XS-WAR",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Warm Taupe",
                "color_hex": "#B38B6D",
                "sku": "AUR-0049-S-WAR",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Warm Taupe",
                "color_hex": "#B38B6D",
                "sku": "AUR-0049-M-WAR",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Warm Taupe",
                "color_hex": "#B38B6D",
                "sku": "AUR-0049-L-WAR",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Warm Taupe",
                "color_hex": "#B38B6D",
                "sku": "AUR-0049-XL-WAR",
                "stock_quantity": 11,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 50,
        "name": "High-Rise Belgian Linen Gurkha Trousers",
        "slug": "trousers-chinos-high-rise-belgian-linen-gurkha-710",
        "description": "Military-heritage Gurkha trousers in pre-washed heavy Belgian linen with crossover buckled cummerbund waistband, deep pleats, and coin pocket.",
        "category_id": 9,
        "base_price": 6999.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% Normandy & Belgian Flax Linen",
        "fit_type": "Gurkha Relaxed Taper",
        "care_instructions": "Wash cold on gentle; warm iron while damp",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 34,
        "sales_count": 72,
        "created_at": "2026-11-11 10:38:51.970217",
        "updated_at": "2026-11-11 10:38:51.970217",
        "category_slug": "tailored-trousers",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Sand Khaki",
                "color_hex": "#C3B091",
                "sku": "AUR-0050-XS-SAN",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Sand Khaki",
                "color_hex": "#C3B091",
                "sku": "AUR-0050-S-SAN",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Sand Khaki",
                "color_hex": "#C3B091",
                "sku": "AUR-0050-M-SAN",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Sand Khaki",
                "color_hex": "#C3B091",
                "sku": "AUR-0050-L-SAN",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Sand Khaki",
                "color_hex": "#C3B091",
                "sku": "AUR-0050-XL-SAN",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Olive Fatigue",
                "color_hex": "#4B5320",
                "sku": "AUR-0050-XS-OLI",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Olive Fatigue",
                "color_hex": "#4B5320",
                "sku": "AUR-0050-S-OLI",
                "stock_quantity": 8,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Olive Fatigue",
                "color_hex": "#4B5320",
                "sku": "AUR-0050-M-OLI",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Olive Fatigue",
                "color_hex": "#4B5320",
                "sku": "AUR-0050-L-OLI",
                "stock_quantity": 8,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Olive Fatigue",
                "color_hex": "#4B5320",
                "sku": "AUR-0050-XL-OLI",
                "stock_quantity": 35,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 51,
        "name": "Kuroki Mills 16oz Selvedge Denim Jacket",
        "slug": "denim-jeans-kuroki-mills-16oz-selvedge-den-672",
        "description": "Heavyweight Type III trucker jacket woven on vintage shuttle looms in Okayama. Features pink selvedge ID, custom brass doughnut buttons, and felled chainstitch seams.",
        "category_id": 11,
        "base_price": 9999.0,
        "discount_price": 8499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Japanese Selvedge Cotton (16oz)",
        "fit_type": "Heritage Boxy Trucker Fit",
        "care_instructions": "Soak inside-out in cold water; hang dry",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 22,
        "sales_count": 89,
        "created_at": "2026-11-11 10:38:51.971231",
        "updated_at": "2026-11-11 10:38:51.971231",
        "category_slug": "selvedge-denim",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Raw Deep Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-0051-XS-RAW",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Raw Deep Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-0051-S-RAW",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Raw Deep Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-0051-M-RAW",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Raw Deep Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-0051-L-RAW",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Raw Deep Indigo",
                "color_hex": "#1B2A4A",
                "sku": "AUR-0051-XL-RAW",
                "stock_quantity": 8,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 52,
        "name": "Relaxed Tapered Japanese Ecru Denim",
        "slug": "denim-jeans-relaxed-tapered-japanese-ecru--796",
        "description": "Unbleached and undyed 13.5oz selvedge denim displaying natural cotton seed flecks. High rise with roomy thighs tapering gently to 15-inch leg openings.",
        "category_id": 12,
        "base_price": 6799.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% Unbleached Organic Cotton",
        "fit_type": "Relaxed Tapered Fit",
        "care_instructions": "Machine wash cold; hang dry",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 21,
        "sales_count": 72,
        "created_at": "2026-11-11 10:38:51.971231",
        "updated_at": "2026-11-11 10:38:51.971231",
        "category_slug": "designer-jeans",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Natural Seeded Ecru",
                "color_hex": "#F2ECE1",
                "sku": "AUR-0052-XS-NAT",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Natural Seeded Ecru",
                "color_hex": "#F2ECE1",
                "sku": "AUR-0052-S-NAT",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Natural Seeded Ecru",
                "color_hex": "#F2ECE1",
                "sku": "AUR-0052-M-NAT",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Natural Seeded Ecru",
                "color_hex": "#F2ECE1",
                "sku": "AUR-0052-L-NAT",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Natural Seeded Ecru",
                "color_hex": "#F2ECE1",
                "sku": "AUR-0052-XL-NAT",
                "stock_quantity": 28,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 53,
        "name": "Mulberry Silk Pajama & Robe Set",
        "slug": "loungewear-mulberry-silk-pajama-robe-set-524",
        "description": "Loungewear perfection in pure 22-momme Mulberry silk with contrast ivory piping, notch lapels, elastic drawstring trousers, and matching belted kimono robe.",
        "category_id": 14,
        "base_price": 12499.0,
        "discount_price": 10499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Grade 6A Mulberry Silk",
        "fit_type": "Relaxed Tailored Lounge Fit",
        "care_instructions": "Hand wash cold with silk detergent; air dry",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 9,
        "sales_count": 40,
        "created_at": "2026-11-11 10:38:51.975544",
        "updated_at": "2026-11-11 10:38:51.975544",
        "category_slug": "silk-sleepwear-robes",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1518049362265-d5b2a6467637?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Noir",
                "color_hex": "#111111",
                "sku": "AUR-0053-XS-MID",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Noir",
                "color_hex": "#111111",
                "sku": "AUR-0053-S-MID",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Noir",
                "color_hex": "#111111",
                "sku": "AUR-0053-M-MID",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Noir",
                "color_hex": "#111111",
                "sku": "AUR-0053-L-MID",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Midnight Noir",
                "color_hex": "#111111",
                "sku": "AUR-0053-XL-MID",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Pearl Champagne",
                "color_hex": "#F3EAD8",
                "sku": "AUR-0053-XS-PEA",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Pearl Champagne",
                "color_hex": "#F3EAD8",
                "sku": "AUR-0053-S-PEA",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Pearl Champagne",
                "color_hex": "#F3EAD8",
                "sku": "AUR-0053-M-PEA",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Pearl Champagne",
                "color_hex": "#F3EAD8",
                "sku": "AUR-0053-L-PEA",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Pearl Champagne",
                "color_hex": "#F3EAD8",
                "sku": "AUR-0053-XL-PEA",
                "stock_quantity": 19,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 54,
        "name": "Superfine Cashmere Jogger & Hoodie Lounge Set",
        "slug": "loungewear-superfine-cashmere-jogger-hood-190",
        "description": "Double-knitted pure cashmere hoodie with kangaroo pocket paired with tapered cuffed joggers featuring flat woven drawstrings and slash pockets.",
        "category_id": 13,
        "base_price": 14999.0,
        "discount_price": 12999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Superfine Mongolian Cashmere",
        "fit_type": "Modern Tapered Lounge Fit",
        "care_instructions": "Hand wash cold; dry flat",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 18,
        "sales_count": 31,
        "created_at": "2026-11-11 10:38:51.978149",
        "updated_at": "2026-11-11 10:38:51.978149",
        "category_slug": "cashmere-loungewear",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Heather Oatmeal",
                "color_hex": "#D2C29D",
                "sku": "AUR-0054-XS-HEA",
                "stock_quantity": 12,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Heather Oatmeal",
                "color_hex": "#D2C29D",
                "sku": "AUR-0054-S-HEA",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Heather Oatmeal",
                "color_hex": "#D2C29D",
                "sku": "AUR-0054-M-HEA",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Heather Oatmeal",
                "color_hex": "#D2C29D",
                "sku": "AUR-0054-L-HEA",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Heather Oatmeal",
                "color_hex": "#D2C29D",
                "sku": "AUR-0054-XL-HEA",
                "stock_quantity": 9,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 55,
        "name": "Merino Thermal Base Layer Compression Set",
        "slug": "activewear-merino-thermal-base-layer-comp-953",
        "description": "Zoned compression top and tights crafted from 200 GSM core-spun merino wool with flatlock anti-chafing seams, ergonomic panelling, and natural odor resistance.",
        "category_id": 16,
        "base_price": 6999.0,
        "discount_price": 5899.0,
        "brand": "Aura Haute Collection",
        "material": "88% Merino Wool, 9% Nylon, 3% Elastane",
        "fit_type": "Ergonomic Performance Compression",
        "care_instructions": "Machine wash cold delicate; air dry",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 40,
        "sales_count": 65,
        "created_at": "2026-11-11 10:38:51.980444",
        "updated_at": "2026-11-11 10:38:51.980444",
        "category_slug": "technical-performance",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Stealth Black",
                "color_hex": "#1C1C1C",
                "sku": "AUR-0055-XS-STE",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Stealth Black",
                "color_hex": "#1C1C1C",
                "sku": "AUR-0055-S-STE",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Stealth Black",
                "color_hex": "#1C1C1C",
                "sku": "AUR-0055-M-STE",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Stealth Black",
                "color_hex": "#1C1C1C",
                "sku": "AUR-0055-L-STE",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Stealth Black",
                "color_hex": "#1C1C1C",
                "sku": "AUR-0055-XL-STE",
                "stock_quantity": 18,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 56,
        "name": "Aero-Vent Seamless Performance Half-Zip",
        "slug": "activewear-aero-vent-seamless-performance-493",
        "description": "Engineered technical knit with targeted mesh perforation zones along the back and underarms. Features waterproof chin-guarded YKK half zipper and thumb loops.",
        "category_id": 15,
        "base_price": 4499.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "62% Recycled Polyamide, 30% Polyester, 8% Spandex",
        "fit_type": "Athletic Aerodynamic Fit",
        "care_instructions": "Machine wash cold; do not use fabric softener",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 34,
        "sales_count": 136,
        "created_at": "2026-11-11 10:38:51.981445",
        "updated_at": "2026-11-11 10:38:51.981445",
        "category_slug": "haute-activewear",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1506152983158-b4a74a01c721?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Forest Olive",
                "color_hex": "#2E3B2E",
                "sku": "AUR-0056-XS-FOR",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Forest Olive",
                "color_hex": "#2E3B2E",
                "sku": "AUR-0056-S-FOR",
                "stock_quantity": 10,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Forest Olive",
                "color_hex": "#2E3B2E",
                "sku": "AUR-0056-M-FOR",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Forest Olive",
                "color_hex": "#2E3B2E",
                "sku": "AUR-0056-L-FOR",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Forest Olive",
                "color_hex": "#2E3B2E",
                "sku": "AUR-0056-XL-FOR",
                "stock_quantity": 16,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 57,
        "name": "Loro Piana Storm-System Wool Trench",
        "slug": "jackets-outerwear-loro-piana-storm-system-wool-t-681",
        "description": "Architectural double-breasted trench crafted from water-repellent, windproof Loro Piana Rain & Storm System virgin wool with storm flaps and horn buckles.",
        "category_id": 18,
        "base_price": 24999.0,
        "discount_price": 21499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Loro Piana Treated Virgin Wool",
        "fit_type": "Tailored Trench Silhouette",
        "care_instructions": "Specialist wool dry clean only",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 22,
        "sales_count": 113,
        "created_at": "2026-11-11 10:38:51.983446",
        "updated_at": "2026-11-11 10:38:51.983446",
        "category_slug": "parkas-puffers",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            },
            {
                "image_url": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 0,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Charcoal Melange",
                "color_hex": "#343434",
                "sku": "AUR-0057-XS-CHA",
                "stock_quantity": 9,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Charcoal Melange",
                "color_hex": "#343434",
                "sku": "AUR-0057-S-CHA",
                "stock_quantity": 9,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Melange",
                "color_hex": "#343434",
                "sku": "AUR-0057-M-CHA",
                "stock_quantity": 9,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Melange",
                "color_hex": "#343434",
                "sku": "AUR-0057-L-CHA",
                "stock_quantity": 32,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Melange",
                "color_hex": "#343434",
                "sku": "AUR-0057-XL-CHA",
                "stock_quantity": 11,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Warm Camel",
                "color_hex": "#C19A6B",
                "sku": "AUR-0057-XS-WAR",
                "stock_quantity": 31,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Warm Camel",
                "color_hex": "#C19A6B",
                "sku": "AUR-0057-S-WAR",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Warm Camel",
                "color_hex": "#C19A6B",
                "sku": "AUR-0057-M-WAR",
                "stock_quantity": 28,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Warm Camel",
                "color_hex": "#C19A6B",
                "sku": "AUR-0057-L-WAR",
                "stock_quantity": 25,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Warm Camel",
                "color_hex": "#C19A6B",
                "sku": "AUR-0057-XL-WAR",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 58,
        "name": "Vintage Oilskin Waxed Field Jacket",
        "slug": "jackets-outerwear-vintage-oilskin-waxed-field-ja-265",
        "description": "Weatherproof 8oz dry-waxed cotton field coat with corduroy collar, bellows cartridge pockets, brass snaps, and warm brushed cotton tartan lining.",
        "category_id": 18,
        "base_price": 13499.0,
        "discount_price": 11499.0,
        "brand": "Aura Haute Collection",
        "material": "100% Waxed British Cotton Canvas, Tartan Lining",
        "fit_type": "Traditional Country Field Fit",
        "care_instructions": "Sponge clean with cold water; re-wax as needed",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 28,
        "sales_count": 66,
        "created_at": "2026-11-11 10:38:51.985443",
        "updated_at": "2026-11-11 10:38:51.985443",
        "category_slug": "parkas-puffers",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1548883354-7622d03aca27?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Dark Olive Canvas",
                "color_hex": "#3D4839",
                "sku": "AUR-0058-XS-DAR",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Dark Olive Canvas",
                "color_hex": "#3D4839",
                "sku": "AUR-0058-S-DAR",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Dark Olive Canvas",
                "color_hex": "#3D4839",
                "sku": "AUR-0058-M-DAR",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Dark Olive Canvas",
                "color_hex": "#3D4839",
                "sku": "AUR-0058-L-DAR",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Dark Olive Canvas",
                "color_hex": "#3D4839",
                "sku": "AUR-0058-XL-DAR",
                "stock_quantity": 33,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 59,
        "name": "Bespoke Normandy Linen Drawstring Overshirt",
        "slug": "summer-linen-bespoke-normandy-linen-drawstr-585",
        "description": "Relaxed casual overshirt with dual patch chest pockets, drawstring waist hem, and corozo nut buttons. Cut from breathable washed French Normandy flax.",
        "category_id": 19,
        "base_price": 5299.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% Normandy Flax Linen",
        "fit_type": "Boxy Overshirt Fit",
        "care_instructions": "Machine wash cold; hang dry",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 38,
        "sales_count": 42,
        "created_at": "2026-11-11 10:38:51.987442",
        "updated_at": "2026-11-11 10:38:51.987442",
        "category_slug": "linen-shirts",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Flax Ecru",
                "color_hex": "#E5D9C5",
                "sku": "AUR-0059-XS-FLA",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Flax Ecru",
                "color_hex": "#E5D9C5",
                "sku": "AUR-0059-S-FLA",
                "stock_quantity": 33,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Flax Ecru",
                "color_hex": "#E5D9C5",
                "sku": "AUR-0059-M-FLA",
                "stock_quantity": 19,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Flax Ecru",
                "color_hex": "#E5D9C5",
                "sku": "AUR-0059-L-FLA",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Flax Ecru",
                "color_hex": "#E5D9C5",
                "sku": "AUR-0059-XL-FLA",
                "stock_quantity": 34,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 60,
        "name": "Relaxed Linen Safari Jacket",
        "slug": "summer-linen-relaxed-linen-safari-jacket-265",
        "description": "Classic colonial safari silhouette with four expandable bellow cargo pockets, waist belt, shoulder epaulets, and unlined garment-dyed linen weave.",
        "category_id": 20,
        "base_price": 9499.0,
        "discount_price": 7999.0,
        "brand": "Aura Haute Collection",
        "material": "100% European Flax Linen (320 GSM)",
        "fit_type": "Relaxed Belted Fit",
        "care_instructions": "Dry clean or gentle cold wash",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 8,
        "sales_count": 53,
        "created_at": "2026-11-11 10:38:51.988947",
        "updated_at": "2026-11-11 10:38:51.988947",
        "category_slug": "linen-resortwear",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1479064555552-3ef4979f8908?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Desert Sand",
                "color_hex": "#EDC9AF",
                "sku": "AUR-0060-XS-DES",
                "stock_quantity": 14,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Desert Sand",
                "color_hex": "#EDC9AF",
                "sku": "AUR-0060-S-DES",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Desert Sand",
                "color_hex": "#EDC9AF",
                "sku": "AUR-0060-M-DES",
                "stock_quantity": 34,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Desert Sand",
                "color_hex": "#EDC9AF",
                "sku": "AUR-0060-L-DES",
                "stock_quantity": 11,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Desert Sand",
                "color_hex": "#EDC9AF",
                "sku": "AUR-0060-XL-DES",
                "stock_quantity": 28,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 61,
        "name": "Goodyear-Welted Pebble Leather Chelsea Boots",
        "slug": "footwear-goodyear-welted-pebble-leather-208",
        "description": "Constructed with French pebble-grain calfskin on an English Goodyear-welted Dainite rubber sole. Features dual elasticated side gussets and leather pull tabs.",
        "category_id": 21,
        "base_price": 14999.0,
        "discount_price": 12499.0,
        "brand": "Aura Haute Collection",
        "material": "French Pebble-Grain Calfskin & Dainite Sole",
        "fit_type": "Classic English Last (Standard D)",
        "care_instructions": "Clean with damp cloth; apply saphir cream",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 23,
        "sales_count": 53,
        "created_at": "2026-11-11 10:38:51.989882",
        "updated_at": "2026-11-11 10:38:51.989882",
        "category_slug": "leather-boots",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "40 EU",
                "color": "Espresso Brown",
                "color_hex": "#362B28",
                "sku": "AUR-0061-40-ESP",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "41 EU",
                "color": "Espresso Brown",
                "color_hex": "#362B28",
                "sku": "AUR-0061-41-ESP",
                "stock_quantity": 17,
                "additional_price": 0.0
            },
            {
                "size": "42 EU",
                "color": "Espresso Brown",
                "color_hex": "#362B28",
                "sku": "AUR-0061-42-ESP",
                "stock_quantity": 13,
                "additional_price": 0.0
            },
            {
                "size": "43 EU",
                "color": "Espresso Brown",
                "color_hex": "#362B28",
                "sku": "AUR-0061-43-ESP",
                "stock_quantity": 16,
                "additional_price": 0.0
            },
            {
                "size": "44 EU",
                "color": "Espresso Brown",
                "color_hex": "#362B28",
                "sku": "AUR-0061-44-ESP",
                "stock_quantity": 8,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 62,
        "name": "Hand-Burnished Italian Penny Loafers",
        "slug": "footwear-hand-burnished-italian-penny-l-436",
        "description": "Hand-lasted Italian penny loafers cut from full-grain vegetable-tanned crust leather with channeled oak-bark tanned leather soles and hand-stitched apron.",
        "category_id": 22,
        "base_price": 12999.0,
        "discount_price": 10999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Italian Crust Leather & Leather Soles",
        "fit_type": "Italian Almond Toe Last",
        "care_instructions": "Store with cedar shoe trees; buff with beeswax",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 35,
        "sales_count": 69,
        "created_at": "2026-11-11 10:38:51.992914",
        "updated_at": "2026-11-11 10:38:51.992914",
        "category_slug": "dress-shoes-loafers",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "40 EU",
                "color": "Cognac Calfskin",
                "color_hex": "#9A5328",
                "sku": "AUR-0062-40-COG",
                "stock_quantity": 35,
                "additional_price": 0.0
            },
            {
                "size": "41 EU",
                "color": "Cognac Calfskin",
                "color_hex": "#9A5328",
                "sku": "AUR-0062-41-COG",
                "stock_quantity": 22,
                "additional_price": 0.0
            },
            {
                "size": "42 EU",
                "color": "Cognac Calfskin",
                "color_hex": "#9A5328",
                "sku": "AUR-0062-42-COG",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "43 EU",
                "color": "Cognac Calfskin",
                "color_hex": "#9A5328",
                "sku": "AUR-0062-43-COG",
                "stock_quantity": 11,
                "additional_price": 0.0
            },
            {
                "size": "44 EU",
                "color": "Cognac Calfskin",
                "color_hex": "#9A5328",
                "sku": "AUR-0062-44-COG",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 63,
        "name": "Full-Grain Italian Vacchetta Leather Duffle Bag",
        "slug": "accessories-full-grain-italian-vacchetta-l-600",
        "description": "Heirloom travel duffle hand-constructed in Florence from Tuscan vacchetta leather that patinas beautifully with journeying. Features solid brass Raccagni hardware and detachable strap.",
        "category_id": 23,
        "base_price": 19999.0,
        "discount_price": 16999.0,
        "brand": "Aura Haute Collection",
        "material": "100% Certified Tuscan Vegetable-Tanned Leather",
        "fit_type": "Cabin Overhead Size (48L)",
        "care_instructions": "Treat with organic leather balsam yearly",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 37,
        "sales_count": 83,
        "created_at": "2026-11-11 10:38:51.993914",
        "updated_at": "2026-11-11 10:38:51.993914",
        "category_slug": "leather-bags-luggage",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "One Size",
                "color": "Saddle Brown",
                "color_hex": "#724C27",
                "sku": "AUR-0063-On-SAD",
                "stock_quantity": 30,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 64,
        "name": "Hand-Rolled Mulberry Silk Pocket Square & Scarf Set",
        "slug": "accessories-hand-rolled-mulberry-silk-pock-244",
        "description": "Double-sided twill silk pocket square and matching neckerchief with hand-rolled artisan hems and archival baroque hand-screened motifs.",
        "category_id": 24,
        "base_price": 3499.0,
        "discount_price": null,
        "brand": "Aura Haute Collection",
        "material": "100% 16-Momme Mulberry Silk Twill",
        "fit_type": "42cm x 42cm Artisan Square",
        "care_instructions": "Dry clean only",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 40,
        "sales_count": 29,
        "created_at": "2026-11-11 10:38:51.994914",
        "updated_at": "2026-11-11 10:38:51.994914",
        "category_slug": "accessories-fine-goods",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?auto=format&fit=crop&w=1000&q=80",
                "is_primary": 1,
                "display_order": 0
            }
        ],
        "variants": [
            {
                "size": "One Size",
                "color": "Royal Gold & Navy",
                "color_hex": "#C5A059",
                "sku": "AUR-0064-On-ROY",
                "stock_quantity": 33,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 65,
        "name": "Crystal-Embellished Silk Satin Column Gown",
        "slug": "crystal-embellished-silk-satin-column-gown",
        "description": "Hand-draped column gown crafted in Lake Como heavy silk satin with micro-crystal contour lines along the neckline.",
        "category_id": 1,
        "base_price": 24999.0,
        "discount_price": 21999.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Heavy Silk Satin (28-Momme)",
        "fit_type": "Architectural Column Fit",
        "care_instructions": "Specialist luxury dry clean only. Store in breathable garment cover.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 28,
        "sales_count": 112,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "evening-gowns",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Obsidian Noir",
                "color_hex": "#111111",
                "sku": "AUR-CRYSTALEM-OB-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Obsidian Noir",
                "color_hex": "#111111",
                "sku": "AUR-CRYSTALEM-OB-S",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Obsidian Noir",
                "color_hex": "#111111",
                "sku": "AUR-CRYSTALEM-OB-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Obsidian Noir",
                "color_hex": "#111111",
                "sku": "AUR-CRYSTALEM-OB-L",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Champagne Ivory",
                "color_hex": "#F7E7CE",
                "sku": "AUR-CRYSTALEM-CH-XS",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Champagne Ivory",
                "color_hex": "#F7E7CE",
                "sku": "AUR-CRYSTALEM-CH-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Champagne Ivory",
                "color_hex": "#F7E7CE",
                "sku": "AUR-CRYSTALEM-CH-M",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Champagne Ivory",
                "color_hex": "#F7E7CE",
                "sku": "AUR-CRYSTALEM-CH-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 66,
        "name": "French Chantilly Lace Off-Shoulder Gala Dress",
        "slug": "french-chantilly-lace-off-shoulder-gala-dress",
        "description": "Dramatic off-shoulder neckline tailored with authentic Calais-Caudry French lace over sheer silk organza lining.",
        "category_id": 1,
        "base_price": 26999.0,
        "discount_price": 23499.0,
        "brand": "Aura Haute Atelier",
        "material": "French Chantilly Lace & Silk Organza",
        "fit_type": "Fitted Bodice with Fluted Skirt",
        "care_instructions": "Specialist dry clean only. Protect lace trims.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 19,
        "sales_count": 76,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "evening-gowns",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Midnight Black",
                "color_hex": "#0A0A0A",
                "sku": "AUR-FRENCHCHA-MI-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Midnight Black",
                "color_hex": "#0A0A0A",
                "sku": "AUR-FRENCHCHA-MI-S",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Midnight Black",
                "color_hex": "#0A0A0A",
                "sku": "AUR-FRENCHCHA-MI-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Midnight Black",
                "color_hex": "#0A0A0A",
                "sku": "AUR-FRENCHCHA-MI-L",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Burgundy Wine",
                "color_hex": "#4A0E17",
                "sku": "AUR-FRENCHCHA-BU-XS",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Burgundy Wine",
                "color_hex": "#4A0E17",
                "sku": "AUR-FRENCHCHA-BU-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Burgundy Wine",
                "color_hex": "#4A0E17",
                "sku": "AUR-FRENCHCHA-BU-M",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Burgundy Wine",
                "color_hex": "#4A0E17",
                "sku": "AUR-FRENCHCHA-BU-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 67,
        "name": "Sea Island Cotton Pleated Tuxedo Shirt",
        "slug": "sea-island-cotton-pleated-tuxedo-shirt",
        "description": "Artisan black-tie tuxedo shirt with razor-sharp bib pleating, removable stud placket, and double French cuffs.",
        "category_id": 3,
        "base_price": 9999.0,
        "discount_price": 8499.0,
        "brand": "Aura Haute Atelier",
        "material": "100% West Indian Sea Island Cotton (140/2)",
        "fit_type": "Tailored Slim",
        "care_instructions": "Professional warm launder, press damp.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 34,
        "sales_count": 136,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "formal-dress-shirts",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Pure White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-SEAISLAND-PU-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Pure White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-SEAISLAND-PU-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Pure White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-SEAISLAND-PU-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Pure White",
                "color_hex": "#FFFFFF",
                "sku": "AUR-SEAISLAND-PU-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Crisp Ecru",
                "color_hex": "#F9F6EE",
                "sku": "AUR-SEAISLAND-CR-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Crisp Ecru",
                "color_hex": "#F9F6EE",
                "sku": "AUR-SEAISLAND-CR-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Crisp Ecru",
                "color_hex": "#F9F6EE",
                "sku": "AUR-SEAISLAND-CR-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Crisp Ecru",
                "color_hex": "#F9F6EE",
                "sku": "AUR-SEAISLAND-CR-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 68,
        "name": "Dobby Weave Semi-Spread Collar Shirt",
        "slug": "dobby-weave-semi-spread-collar-shirt",
        "description": "Subtle diamond geometric dobby weave delivering rich tactile micro-texture under business tailoring.",
        "category_id": 3,
        "base_price": 6499.0,
        "discount_price": 5499.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Egyptian Giza Cotton",
        "fit_type": "Contemporary Regular",
        "care_instructions": "Machine wash gentle cold, medium iron.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 42,
        "sales_count": 168,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "formal-dress-shirts",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Sky Blue Dobby",
                "color_hex": "#D0E0EC",
                "sku": "AUR-DOBBYWEAV-SK-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Sky Blue Dobby",
                "color_hex": "#D0E0EC",
                "sku": "AUR-DOBBYWEAV-SK-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Sky Blue Dobby",
                "color_hex": "#D0E0EC",
                "sku": "AUR-DOBBYWEAV-SK-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Sky Blue Dobby",
                "color_hex": "#D0E0EC",
                "sku": "AUR-DOBBYWEAV-SK-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "XXL",
                "color": "Sky Blue Dobby",
                "color_hex": "#D0E0EC",
                "sku": "AUR-DOBBYWEAV-SK-XXL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "White Dobby",
                "color_hex": "#FAFAFA",
                "sku": "AUR-DOBBYWEAV-WH-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "White Dobby",
                "color_hex": "#FAFAFA",
                "sku": "AUR-DOBBYWEAV-WH-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "White Dobby",
                "color_hex": "#FAFAFA",
                "sku": "AUR-DOBBYWEAV-WH-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "White Dobby",
                "color_hex": "#FAFAFA",
                "sku": "AUR-DOBBYWEAV-WH-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XXL",
                "color": "White Dobby",
                "color_hex": "#FAFAFA",
                "sku": "AUR-DOBBYWEAV-WH-XXL",
                "stock_quantity": 32,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 69,
        "name": "Loro Piana Rain-System Cashmere Car Coat",
        "slug": "loro-piana-rain-system-cashmere-car-coat",
        "description": "Pure cashmere overcoat treated with invisible nano-membrane protection for zero water permeation and supreme warmth.",
        "category_id": 6,
        "base_price": 28999.0,
        "discount_price": 25999.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Mongolian Cashmere with Rain & Wind System",
        "fit_type": "Relaxed Overcoat Fit",
        "care_instructions": "Specialist luxury dry clean only.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 22,
        "sales_count": 88,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "overcoats-trench",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Charcoal Melange",
                "color_hex": "#2B2B2B",
                "sku": "AUR-LOROPIANA-CH-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Charcoal Melange",
                "color_hex": "#2B2B2B",
                "sku": "AUR-LOROPIANA-CH-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Charcoal Melange",
                "color_hex": "#2B2B2B",
                "sku": "AUR-LOROPIANA-CH-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Charcoal Melange",
                "color_hex": "#2B2B2B",
                "sku": "AUR-LOROPIANA-CH-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Camel Vicuna",
                "color_hex": "#C19A6B",
                "sku": "AUR-LOROPIANA-CA-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Camel Vicuna",
                "color_hex": "#C19A6B",
                "sku": "AUR-LOROPIANA-CA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Camel Vicuna",
                "color_hex": "#C19A6B",
                "sku": "AUR-LOROPIANA-CA-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Camel Vicuna",
                "color_hex": "#C19A6B",
                "sku": "AUR-LOROPIANA-CA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 70,
        "name": "Double-Breasted Camel Wool Polo Coat",
        "slug": "double-breasted-camel-wool-polo-coat",
        "description": "Iconic double-breasted polo coat with Ulster collar, turn-back cuffs, and deep tortoiseshell buttons.",
        "category_id": 6,
        "base_price": 21999.0,
        "discount_price": 18999.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Baby Camel Hair (620 GSM)",
        "fit_type": "Architectural Tailored Fit",
        "care_instructions": "Dry clean only. Brush with soft horsehair brush.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 17,
        "sales_count": 68,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "overcoats-trench",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Golden Camel",
                "color_hex": "#B58A55",
                "sku": "AUR-DOUBLEBRE-GO-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Golden Camel",
                "color_hex": "#B58A55",
                "sku": "AUR-DOUBLEBRE-GO-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Golden Camel",
                "color_hex": "#B58A55",
                "sku": "AUR-DOUBLEBRE-GO-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Golden Camel",
                "color_hex": "#B58A55",
                "sku": "AUR-DOUBLEBRE-GO-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Navy Cast",
                "color_hex": "#182232",
                "sku": "AUR-DOUBLEBRE-NA-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Navy Cast",
                "color_hex": "#182232",
                "sku": "AUR-DOUBLEBRE-NA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Navy Cast",
                "color_hex": "#182232",
                "sku": "AUR-DOUBLEBRE-NA-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Navy Cast",
                "color_hex": "#182232",
                "sku": "AUR-DOUBLEBRE-NA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 71,
        "name": "Silk-Cashmere Long Sleeve Knit Polo",
        "slug": "silk-cashmere-long-sleeve-knit-polo",
        "description": "18-gauge featherweight fine knit polo with seamless fashioned collar and mother-of-pearl buttons.",
        "category_id": 7,
        "base_price": 10999.0,
        "discount_price": 8999.0,
        "brand": "Aura Haute Atelier",
        "material": "70% Mulberry Silk, 30% Grade-A Cashmere",
        "fit_type": "Tailored Knit Fit",
        "care_instructions": "Hand wash cold with wool detergent, dry flat.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 38,
        "sales_count": 152,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "fine-knitwear",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1617137984095-74e4e5e3613f?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Dark Espresso",
                "color_hex": "#2B1E1A",
                "sku": "AUR-SILKCASHM-DA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Dark Espresso",
                "color_hex": "#2B1E1A",
                "sku": "AUR-SILKCASHM-DA-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Dark Espresso",
                "color_hex": "#2B1E1A",
                "sku": "AUR-SILKCASHM-DA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Dark Espresso",
                "color_hex": "#2B1E1A",
                "sku": "AUR-SILKCASHM-DA-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Sage Green",
                "color_hex": "#8A9A86",
                "sku": "AUR-SILKCASHM-SA-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Sage Green",
                "color_hex": "#8A9A86",
                "sku": "AUR-SILKCASHM-SA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Sage Green",
                "color_hex": "#8A9A86",
                "sku": "AUR-SILKCASHM-SA-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Sage Green",
                "color_hex": "#8A9A86",
                "sku": "AUR-SILKCASHM-SA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 72,
        "name": "Superfine Merino Wool V-Neck Sweater",
        "slug": "superfine-merino-wool-v-neck-sweater",
        "description": "Ultra-lightweight layering v-neck tailored with ribbed cuffs and subtle jersey knit drape.",
        "category_id": 7,
        "base_price": 8499.0,
        "discount_price": 6999.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Australian 16.5 Micron Extra-Fine Merino",
        "fit_type": "Slim Knit",
        "care_instructions": "Hand wash cold, dry flat.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 51,
        "sales_count": 204,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "fine-knitwear",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Oatmeal Heather",
                "color_hex": "#D3C5B4",
                "sku": "AUR-SUPERFINE-OA-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Oatmeal Heather",
                "color_hex": "#D3C5B4",
                "sku": "AUR-SUPERFINE-OA-S",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Oatmeal Heather",
                "color_hex": "#D3C5B4",
                "sku": "AUR-SUPERFINE-OA-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Oatmeal Heather",
                "color_hex": "#D3C5B4",
                "sku": "AUR-SUPERFINE-OA-L",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Oatmeal Heather",
                "color_hex": "#D3C5B4",
                "sku": "AUR-SUPERFINE-OA-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Deep Midnight",
                "color_hex": "#101826",
                "sku": "AUR-SUPERFINE-DE-XS",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Deep Midnight",
                "color_hex": "#101826",
                "sku": "AUR-SUPERFINE-DE-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Deep Midnight",
                "color_hex": "#101826",
                "sku": "AUR-SUPERFINE-DE-M",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Deep Midnight",
                "color_hex": "#101826",
                "sku": "AUR-SUPERFINE-DE-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Deep Midnight",
                "color_hex": "#101826",
                "sku": "AUR-SUPERFINE-DE-XL",
                "stock_quantity": 32,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 73,
        "name": "Chunky Ribbed Lambswool Half-Zip Sweater",
        "slug": "chunky-ribbed-lambswool-half-zip-sweater",
        "description": "Substantial 5-gauge brioche knit half-zip featuring Swiss RiRi antique brass zipper and stand collar.",
        "category_id": 8,
        "base_price": 12999.0,
        "discount_price": 10999.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Geelong First-Shearing Lambswool (5-Gauge)",
        "fit_type": "Relaxed Chunky Knit",
        "care_instructions": "Dry clean or hand wash cold inside out.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 46,
        "sales_count": 184,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "sweaters-cardigans",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Ecru Cream",
                "color_hex": "#F5F2EB",
                "sku": "AUR-CHUNKYRIB-EC-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Ecru Cream",
                "color_hex": "#F5F2EB",
                "sku": "AUR-CHUNKYRIB-EC-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Ecru Cream",
                "color_hex": "#F5F2EB",
                "sku": "AUR-CHUNKYRIB-EC-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Ecru Cream",
                "color_hex": "#F5F2EB",
                "sku": "AUR-CHUNKYRIB-EC-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Heather Charcoal",
                "color_hex": "#333333",
                "sku": "AUR-CHUNKYRIB-HE-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Heather Charcoal",
                "color_hex": "#333333",
                "sku": "AUR-CHUNKYRIB-HE-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Heather Charcoal",
                "color_hex": "#333333",
                "sku": "AUR-CHUNKYRIB-HE-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Heather Charcoal",
                "color_hex": "#333333",
                "sku": "AUR-CHUNKYRIB-HE-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 74,
        "name": "Washed Canvas Officer Chinos",
        "slug": "washed-canvas-officer-chinos",
        "description": "Garment-washed officer trousers with reinforced coin pocket, bound seams, and clean front rise.",
        "category_id": 10,
        "base_price": 6499.0,
        "discount_price": 5299.0,
        "brand": "Aura Haute Atelier",
        "material": "98% Combed Cotton Canvas, 2% Elastane",
        "fit_type": "Tapered Officer Fit",
        "care_instructions": "Machine wash cold inside out, tumble low.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 39,
        "sales_count": 156,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "chinos-casual-pants",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "30",
                "color": "British Khaki",
                "color_hex": "#C3B091",
                "sku": "AUR-WASHEDCAN-BR-30",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "British Khaki",
                "color_hex": "#C3B091",
                "sku": "AUR-WASHEDCAN-BR-32",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "British Khaki",
                "color_hex": "#C3B091",
                "sku": "AUR-WASHEDCAN-BR-34",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "British Khaki",
                "color_hex": "#C3B091",
                "sku": "AUR-WASHEDCAN-BR-36",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "30",
                "color": "Dark Olive",
                "color_hex": "#3B4D3C",
                "sku": "AUR-WASHEDCAN-DA-30",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "Dark Olive",
                "color_hex": "#3B4D3C",
                "sku": "AUR-WASHEDCAN-DA-32",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Dark Olive",
                "color_hex": "#3B4D3C",
                "sku": "AUR-WASHEDCAN-DA-34",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Dark Olive",
                "color_hex": "#3B4D3C",
                "sku": "AUR-WASHEDCAN-DA-36",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 75,
        "name": "Drawstring Cotton-Modal Travel Trousers",
        "slug": "drawstring-cotton-modal-travel-trousers",
        "description": "Wrinkle-resistant tailored loungewear pant with internal luxury grosgrain drawstring and zipped pocket.",
        "category_id": 10,
        "base_price": 7299.0,
        "discount_price": 5999.0,
        "brand": "Aura Haute Atelier",
        "material": "60% Pima Cotton, 35% MicroModal, 5% Spandex",
        "fit_type": "Relaxed Tapered",
        "care_instructions": "Machine wash cold gentle, air dry.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 48,
        "sales_count": 192,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "chinos-casual-pants",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1517445312882-bc9910d016b7?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Graphite Grey",
                "color_hex": "#383E42",
                "sku": "AUR-DRAWSTRING-GR-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Graphite Grey",
                "color_hex": "#383E42",
                "sku": "AUR-DRAWSTRING-GR-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Graphite Grey",
                "color_hex": "#383E42",
                "sku": "AUR-DRAWSTRING-GR-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Graphite Grey",
                "color_hex": "#383E42",
                "sku": "AUR-DRAWSTRING-GR-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Navy Blue",
                "color_hex": "#1B2A4A",
                "sku": "AUR-DRAWSTRING-NA-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Navy Blue",
                "color_hex": "#1B2A4A",
                "sku": "AUR-DRAWSTRING-NA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Navy Blue",
                "color_hex": "#1B2A4A",
                "sku": "AUR-DRAWSTRING-NA-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Navy Blue",
                "color_hex": "#1B2A4A",
                "sku": "AUR-DRAWSTRING-NA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 76,
        "name": "Pleated Italian Cotton Cavalry Twill Trousers",
        "slug": "pleated-italian-cotton-cavalry-twill-trousers",
        "description": "High-density steep twill weave producing structured drape with extended waistband and horn button closure.",
        "category_id": 10,
        "base_price": 8999.0,
        "discount_price": 7499.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Italian Moleskin Cavalry Twill",
        "fit_type": "Mid-Rise Single Pleat",
        "care_instructions": "Dry clean recommended.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 23,
        "sales_count": 92,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "chinos-casual-pants",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "30",
                "color": "Sand Dune",
                "color_hex": "#D8C7B5",
                "sku": "AUR-PLEATEDIT-SA-30",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "Sand Dune",
                "color_hex": "#D8C7B5",
                "sku": "AUR-PLEATEDIT-SA-32",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Sand Dune",
                "color_hex": "#D8C7B5",
                "sku": "AUR-PLEATEDIT-SA-34",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Sand Dune",
                "color_hex": "#D8C7B5",
                "sku": "AUR-PLEATEDIT-SA-36",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "30",
                "color": "Tobacco Brown",
                "color_hex": "#5C3A21",
                "sku": "AUR-PLEATEDIT-TO-30",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "Tobacco Brown",
                "color_hex": "#5C3A21",
                "sku": "AUR-PLEATEDIT-TO-32",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Tobacco Brown",
                "color_hex": "#5C3A21",
                "sku": "AUR-PLEATEDIT-TO-34",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Tobacco Brown",
                "color_hex": "#5C3A21",
                "sku": "AUR-PLEATEDIT-TO-36",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 77,
        "name": "15.5oz Kaihara Japanese Selvedge Denim",
        "slug": "15-5oz-kaihara-japanese-selvedge-denim",
        "description": "Vintage Toyoda shuttle-loom woven denim with classic red-line selvedge ID and copper punched rivets.",
        "category_id": 11,
        "base_price": 14999.0,
        "discount_price": 12499.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Kaihara Mill Selvedge Cotton",
        "fit_type": "Classic Straight Leg",
        "care_instructions": "Wash cold inside out after 6 months wear. Hang dry.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 31,
        "sales_count": 124,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "selvedge-denim",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "30",
                "color": "Raw Indigo",
                "color_hex": "#1B263B",
                "sku": "AUR-155OZKAI-RA-30",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "Raw Indigo",
                "color_hex": "#1B263B",
                "sku": "AUR-155OZKAI-RA-32",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Raw Indigo",
                "color_hex": "#1B263B",
                "sku": "AUR-155OZKAI-RA-34",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Raw Indigo",
                "color_hex": "#1B263B",
                "sku": "AUR-155OZKAI-RA-36",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "30",
                "color": "One-Wash Indigo",
                "color_hex": "#14213D",
                "sku": "AUR-155OZKAI-ON-30",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "One-Wash Indigo",
                "color_hex": "#14213D",
                "sku": "AUR-155OZKAI-ON-32",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "One-Wash Indigo",
                "color_hex": "#14213D",
                "sku": "AUR-155OZKAI-ON-34",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "One-Wash Indigo",
                "color_hex": "#14213D",
                "sku": "AUR-155OZKAI-ON-36",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 78,
        "name": "Washed Black Slim Stretch Designer Jeans",
        "slug": "washed-black-slim-stretch-designer-jeans",
        "description": "Sleek washed sulfur black denim with engineered flex recovery and tonal matte hardware.",
        "category_id": 12,
        "base_price": 7999.0,
        "discount_price": 6499.0,
        "brand": "Aura Haute Atelier",
        "material": "94% Turkish Cotton, 5% Poly, 1% Elastane",
        "fit_type": "Slim Tapered",
        "care_instructions": "Machine wash cold inside out with like darks.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 65,
        "sales_count": 260,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "designer-jeans",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "30",
                "color": "Faded Obsidian",
                "color_hex": "#222222",
                "sku": "AUR-WASHEDBLA-FA-30",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "Faded Obsidian",
                "color_hex": "#222222",
                "sku": "AUR-WASHEDBLA-FA-32",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Faded Obsidian",
                "color_hex": "#222222",
                "sku": "AUR-WASHEDBLA-FA-34",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Faded Obsidian",
                "color_hex": "#222222",
                "sku": "AUR-WASHEDBLA-FA-36",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "30",
                "color": "Mineral Black",
                "color_hex": "#151515",
                "sku": "AUR-WASHEDBLA-MI-30",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "Mineral Black",
                "color_hex": "#151515",
                "sku": "AUR-WASHEDBLA-MI-32",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Mineral Black",
                "color_hex": "#151515",
                "sku": "AUR-WASHEDBLA-MI-34",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Mineral Black",
                "color_hex": "#151515",
                "sku": "AUR-WASHEDBLA-MI-36",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 79,
        "name": "Vintage Fade Distressed Italian Jeans",
        "slug": "vintage-fade-distressed-italian-jeans",
        "description": "Authentic stone-wash distressing crafted by hand in Veneto, Italy with subtle whiskering.",
        "category_id": 12,
        "base_price": 8499.0,
        "discount_price": 6999.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Ring-Spun Italian Denim (12.5oz)",
        "fit_type": "Relaxed Straight",
        "care_instructions": "Machine wash gentle cold, hang dry.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.7,
        "review_count": 40,
        "sales_count": 160,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "designer-jeans",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "30",
                "color": "Light Vintage Indigo",
                "color_hex": "#7A9EB8",
                "sku": "AUR-VINTAGEFA-LI-30",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "Light Vintage Indigo",
                "color_hex": "#7A9EB8",
                "sku": "AUR-VINTAGEFA-LI-32",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Light Vintage Indigo",
                "color_hex": "#7A9EB8",
                "sku": "AUR-VINTAGEFA-LI-34",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Light Vintage Indigo",
                "color_hex": "#7A9EB8",
                "sku": "AUR-VINTAGEFA-LI-36",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "30",
                "color": "Mid Vintage Blue",
                "color_hex": "#4B6B94",
                "sku": "AUR-VINTAGEFA-MI-30",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "Mid Vintage Blue",
                "color_hex": "#4B6B94",
                "sku": "AUR-VINTAGEFA-MI-32",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Mid Vintage Blue",
                "color_hex": "#4B6B94",
                "sku": "AUR-VINTAGEFA-MI-34",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Mid Vintage Blue",
                "color_hex": "#4B6B94",
                "sku": "AUR-VINTAGEFA-MI-36",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 80,
        "name": "Ribbed Cashmere Lounge Pants",
        "slug": "ribbed-cashmere-lounge-pants",
        "description": "Supreme comfort lounge pants in wide ribbed cashmere with knitted drawstring and seamless pockets.",
        "category_id": 13,
        "base_price": 13999.0,
        "discount_price": 11499.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Grade-A Mongolian Cashmere",
        "fit_type": "Tapered Relaxed Leg",
        "care_instructions": "Hand wash cold with wool wash, dry flat.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 29,
        "sales_count": 116,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "cashmere-loungewear",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Bisque Beige",
                "color_hex": "#E8D8C8",
                "sku": "AUR-RIBBEDCAS-BI-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Bisque Beige",
                "color_hex": "#E8D8C8",
                "sku": "AUR-RIBBEDCAS-BI-S",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Bisque Beige",
                "color_hex": "#E8D8C8",
                "sku": "AUR-RIBBEDCAS-BI-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Bisque Beige",
                "color_hex": "#E8D8C8",
                "sku": "AUR-RIBBEDCAS-BI-L",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Bisque Beige",
                "color_hex": "#E8D8C8",
                "sku": "AUR-RIBBEDCAS-BI-XL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Slate Heather",
                "color_hex": "#5A6570",
                "sku": "AUR-RIBBEDCAS-SL-XS",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Slate Heather",
                "color_hex": "#5A6570",
                "sku": "AUR-RIBBEDCAS-SL-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Slate Heather",
                "color_hex": "#5A6570",
                "sku": "AUR-RIBBEDCAS-SL-M",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Slate Heather",
                "color_hex": "#5A6570",
                "sku": "AUR-RIBBEDCAS-SL-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Slate Heather",
                "color_hex": "#5A6570",
                "sku": "AUR-RIBBEDCAS-SL-XL",
                "stock_quantity": 32,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 81,
        "name": "22-Momme Silk Contrast-Piped Smoking Robe",
        "slug": "22-momme-silk-contrast-piped-smoking-robe",
        "description": "Floor-length smoking robe tailored with contrast ivory silk satin piping, patch pockets, and sash belt.",
        "category_id": 14,
        "base_price": 18999.0,
        "discount_price": 15999.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Mulberry Charmeuse Silk (22-Momme)",
        "fit_type": "Draped Shawl Collar Wrap",
        "care_instructions": "Dry clean or delicate silk wash in mesh bag.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 24,
        "sales_count": 96,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "silk-sleepwear-robes",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Royal Midnight Navy",
                "color_hex": "#0E1A2B",
                "sku": "AUR-22MOMMES-RO-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Royal Midnight Navy",
                "color_hex": "#0E1A2B",
                "sku": "AUR-22MOMMES-RO-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Royal Midnight Navy",
                "color_hex": "#0E1A2B",
                "sku": "AUR-22MOMMES-RO-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Royal Midnight Navy",
                "color_hex": "#0E1A2B",
                "sku": "AUR-22MOMMES-RO-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Bordeaux Crimson",
                "color_hex": "#4B1521",
                "sku": "AUR-22MOMMES-BO-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Bordeaux Crimson",
                "color_hex": "#4B1521",
                "sku": "AUR-22MOMMES-BO-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Bordeaux Crimson",
                "color_hex": "#4B1521",
                "sku": "AUR-22MOMMES-BO-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Bordeaux Crimson",
                "color_hex": "#4B1521",
                "sku": "AUR-22MOMMES-BO-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 82,
        "name": "Silk Satin Button-Down Sleep Shirt",
        "slug": "silk-satin-button-down-sleep-shirt",
        "description": "Classic tailored nightshirt with notch collar, mother-of-pearl buttons, and curved shirttail hem.",
        "category_id": 14,
        "base_price": 9999.0,
        "discount_price": 7999.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Mulberry Silk (19-Momme)",
        "fit_type": "Relaxed Boyfriend Cut",
        "care_instructions": "Hand wash cold, line dry in shade.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 36,
        "sales_count": 144,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "silk-sleepwear-robes",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "XS",
                "color": "Pearl White",
                "color_hex": "#FAF8F5",
                "sku": "AUR-SILKSATIN-PE-XS",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Pearl White",
                "color_hex": "#FAF8F5",
                "sku": "AUR-SILKSATIN-PE-S",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Pearl White",
                "color_hex": "#FAF8F5",
                "sku": "AUR-SILKSATIN-PE-M",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Pearl White",
                "color_hex": "#FAF8F5",
                "sku": "AUR-SILKSATIN-PE-L",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "XS",
                "color": "Rose Quartz",
                "color_hex": "#E8C5C8",
                "sku": "AUR-SILKSATIN-RO-XS",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Rose Quartz",
                "color_hex": "#E8C5C8",
                "sku": "AUR-SILKSATIN-RO-S",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Rose Quartz",
                "color_hex": "#E8C5C8",
                "sku": "AUR-SILKSATIN-RO-M",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Rose Quartz",
                "color_hex": "#E8C5C8",
                "sku": "AUR-SILKSATIN-RO-L",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 83,
        "name": "Draped Pure Silk Lounge Kimono",
        "slug": "draped-pure-silk-lounge-kimono",
        "description": "Handcrafted kimono-style lounge robe featuring wide batwing sleeves and fluid drape.",
        "category_id": 14,
        "base_price": 15999.0,
        "discount_price": 13499.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Heavy Mulberry Silk Habotai",
        "fit_type": "Fluid Open Silhouette",
        "care_instructions": "Delicate silk wash cold, cool iron.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 18,
        "sales_count": 72,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "silk-sleepwear-robes",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "One Size",
                "color": "Onyx Black",
                "color_hex": "#121212",
                "sku": "AUR-DRAPEDPUR-ON-One Size",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "Petite",
                "color": "Onyx Black",
                "color_hex": "#121212",
                "sku": "AUR-DRAPEDPUR-ON-Petite",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "One Size",
                "color": "Golden Bronze",
                "color_hex": "#A37C4E",
                "sku": "AUR-DRAPEDPUR-GO-One Size",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "Petite",
                "color": "Golden Bronze",
                "color_hex": "#A37C4E",
                "sku": "AUR-DRAPEDPUR-GO-Petite",
                "stock_quantity": 23,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 84,
        "name": "Micro-Perforated Ultra-Breathable Training Tee",
        "slug": "micro-perforated-ultra-breathable-training-tee",
        "description": "Laser-cut zoned ventilation with bonded flatlock seams to eradicate friction during elite training.",
        "category_id": 15,
        "base_price": 4299.0,
        "discount_price": 3499.0,
        "brand": "Aura Haute Atelier",
        "material": "82% Recycled Poly, 18% Elastane with Anti-Odor Silver",
        "fit_type": "Athletic Tailored",
        "care_instructions": "Machine wash cold inside out, no fabric softener.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 72,
        "sales_count": 288,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "haute-activewear",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1506152983158-b4a74a01c721?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Gunmetal",
                "color_hex": "#2E3138",
                "sku": "AUR-MICROPERF-GU-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Gunmetal",
                "color_hex": "#2E3138",
                "sku": "AUR-MICROPERF-GU-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Gunmetal",
                "color_hex": "#2E3138",
                "sku": "AUR-MICROPERF-GU-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Gunmetal",
                "color_hex": "#2E3138",
                "sku": "AUR-MICROPERF-GU-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Deep Forest",
                "color_hex": "#1E3326",
                "sku": "AUR-MICROPERF-DE-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Deep Forest",
                "color_hex": "#1E3326",
                "sku": "AUR-MICROPERF-DE-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Deep Forest",
                "color_hex": "#1E3326",
                "sku": "AUR-MICROPERF-DE-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Deep Forest",
                "color_hex": "#1E3326",
                "sku": "AUR-MICROPERF-DE-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 85,
        "name": "Four-Way Stretch Athletic Running Shorts",
        "slug": "four-way-stretch-athletic-running-shorts",
        "description": "Ergonomic running shorts with integrated compression liner, concealed zipper pocket, and bonded hems.",
        "category_id": 15,
        "base_price": 4999.0,
        "discount_price": 3999.0,
        "brand": "Aura Haute Atelier",
        "material": "88% Featherweight Nylon, 12% Spandex",
        "fit_type": "7-Inch Inseam Tailored",
        "care_instructions": "Machine wash cold, air dry quickly.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 55,
        "sales_count": 220,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "haute-activewear",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Matte Black",
                "color_hex": "#141414",
                "sku": "AUR-FOURWAYS-MA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Matte Black",
                "color_hex": "#141414",
                "sku": "AUR-FOURWAYS-MA-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Matte Black",
                "color_hex": "#141414",
                "sku": "AUR-FOURWAYS-MA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Matte Black",
                "color_hex": "#141414",
                "sku": "AUR-FOURWAYS-MA-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Stone Grey",
                "color_hex": "#707378",
                "sku": "AUR-FOURWAYS-ST-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Stone Grey",
                "color_hex": "#707378",
                "sku": "AUR-FOURWAYS-ST-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Stone Grey",
                "color_hex": "#707378",
                "sku": "AUR-FOURWAYS-ST-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Stone Grey",
                "color_hex": "#707378",
                "sku": "AUR-FOURWAYS-ST-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 86,
        "name": "3-Layer GORE-TEX Mountain Rain Shell",
        "slug": "3-layer-gore-tex-mountain-rain-shell",
        "description": "Fully taped stormproof technical shell with AquaGuard water-repellent zippers and storm hood.",
        "category_id": 16,
        "base_price": 19999.0,
        "discount_price": 16999.0,
        "brand": "Aura Haute Atelier",
        "material": "3-Layer Technical Shell (28,000mm Waterproof)",
        "fit_type": "Engineered Articulated Fit",
        "care_instructions": "Machine wash gentle warm with technical detergent, tumble low.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 33,
        "sales_count": 132,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "technical-performance",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1548883354-7622d03aca27?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Alpine Black",
                "color_hex": "#18181A",
                "sku": "AUR-3LAYERGO-AL-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Alpine Black",
                "color_hex": "#18181A",
                "sku": "AUR-3LAYERGO-AL-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Alpine Black",
                "color_hex": "#18181A",
                "sku": "AUR-3LAYERGO-AL-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Alpine Black",
                "color_hex": "#18181A",
                "sku": "AUR-3LAYERGO-AL-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Glacier Blue",
                "color_hex": "#4F687D",
                "sku": "AUR-3LAYERGO-GL-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Glacier Blue",
                "color_hex": "#4F687D",
                "sku": "AUR-3LAYERGO-GL-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Glacier Blue",
                "color_hex": "#4F687D",
                "sku": "AUR-3LAYERGO-GL-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Glacier Blue",
                "color_hex": "#4F687D",
                "sku": "AUR-3LAYERGO-GL-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 87,
        "name": "Thermal Insulated Technical Hybrid Vest",
        "slug": "thermal-insulated-technical-hybrid-vest",
        "description": "Core body heat retention vest featuring water-resistant front baffles and breathable stretch side inserts.",
        "category_id": 16,
        "base_price": 11999.0,
        "discount_price": 9999.0,
        "brand": "Aura Haute Atelier",
        "material": "PrimaLoft Gold Eco Insulation & Stretch Knit Panels",
        "fit_type": "Fitted Technical Layer",
        "care_instructions": "Machine wash cold gentle, tumble dry low.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 29,
        "sales_count": 116,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "technical-performance",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1516257984-b1b4d707412e?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Carbon Black",
                "color_hex": "#1A1A1D",
                "sku": "AUR-THERMALIN-CA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Carbon Black",
                "color_hex": "#1A1A1D",
                "sku": "AUR-THERMALIN-CA-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Carbon Black",
                "color_hex": "#1A1A1D",
                "sku": "AUR-THERMALIN-CA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Carbon Black",
                "color_hex": "#1A1A1D",
                "sku": "AUR-THERMALIN-CA-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Bronze Olive",
                "color_hex": "#474537",
                "sku": "AUR-THERMALIN-BR-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Bronze Olive",
                "color_hex": "#474537",
                "sku": "AUR-THERMALIN-BR-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Bronze Olive",
                "color_hex": "#474537",
                "sku": "AUR-THERMALIN-BR-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Bronze Olive",
                "color_hex": "#474537",
                "sku": "AUR-THERMALIN-BR-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 88,
        "name": "Hand-Waxed Calfskin Biker Jacket",
        "slug": "hand-waxed-calfskin-biker-jacket",
        "description": "Asymmetrical front zip moto jacket with antiqued hardware, diamond quilted shoulder accents, and cupro lining.",
        "category_id": 17,
        "base_price": 27999.0,
        "discount_price": 24999.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Full-Grain Italian Calfskin Leather",
        "fit_type": "Tailored Moto Fit",
        "care_instructions": "Specialist leather care only.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 41,
        "sales_count": 164,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "leather-suede-jackets",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1487222477894-8943e31ef7b2?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Waxed Antique Black",
                "color_hex": "#111111",
                "sku": "AUR-HANDWAXED-WA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Waxed Antique Black",
                "color_hex": "#111111",
                "sku": "AUR-HANDWAXED-WA-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Waxed Antique Black",
                "color_hex": "#111111",
                "sku": "AUR-HANDWAXED-WA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Waxed Antique Black",
                "color_hex": "#111111",
                "sku": "AUR-HANDWAXED-WA-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Vintage Cognac",
                "color_hex": "#733816",
                "sku": "AUR-HANDWAXED-VI-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Vintage Cognac",
                "color_hex": "#733816",
                "sku": "AUR-HANDWAXED-VI-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Vintage Cognac",
                "color_hex": "#733816",
                "sku": "AUR-HANDWAXED-VI-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Vintage Cognac",
                "color_hex": "#733816",
                "sku": "AUR-HANDWAXED-VI-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 89,
        "name": "Diamond-Quilted Ultralight Down Bomber",
        "slug": "diamond-quilted-ultralight-down-bomber",
        "description": "Featherweight Japanese micro-ripstop shell packed with RDS-certified 800-fill down in classic diamond quilting.",
        "category_id": 18,
        "base_price": 14499.0,
        "discount_price": 12499.0,
        "brand": "Aura Haute Atelier",
        "material": "90/10 White Goose Down (800 Fill Power)",
        "fit_type": "Streamlined Bomber Fit",
        "care_instructions": "Dry clean or tumble dry low with wool dryer balls.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 35,
        "sales_count": 140,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "parkas-puffers",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Matte Espresso",
                "color_hex": "#2B2118",
                "sku": "AUR-DIAMONDQU-MA-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Matte Espresso",
                "color_hex": "#2B2118",
                "sku": "AUR-DIAMONDQU-MA-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Matte Espresso",
                "color_hex": "#2B2118",
                "sku": "AUR-DIAMONDQU-MA-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Matte Espresso",
                "color_hex": "#2B2118",
                "sku": "AUR-DIAMONDQU-MA-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Steel Navy",
                "color_hex": "#1E2B3C",
                "sku": "AUR-DIAMONDQU-ST-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Steel Navy",
                "color_hex": "#1E2B3C",
                "sku": "AUR-DIAMONDQU-ST-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Steel Navy",
                "color_hex": "#1E2B3C",
                "sku": "AUR-DIAMONDQU-ST-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Steel Navy",
                "color_hex": "#1E2B3C",
                "sku": "AUR-DIAMONDQU-ST-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 90,
        "name": "Pure French Flax Band-Collar Linen Shirt",
        "slug": "pure-french-flax-band-collar-linen-shirt",
        "description": "Airy mandarin collar shirt with genuine river shell buttons and soft pre-washed drape.",
        "category_id": 19,
        "base_price": 5999.0,
        "discount_price": 4999.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Certified French Flax Linen",
        "fit_type": "Relaxed Resort Fit",
        "care_instructions": "Machine wash cold delicate, air dry.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 57,
        "sales_count": 228,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "linen-shirts",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1603252109303-2751441dd157?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Chalk White",
                "color_hex": "#FBFBF9",
                "sku": "AUR-PUREFRENC-CH-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Chalk White",
                "color_hex": "#FBFBF9",
                "sku": "AUR-PUREFRENC-CH-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Chalk White",
                "color_hex": "#FBFBF9",
                "sku": "AUR-PUREFRENC-CH-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Chalk White",
                "color_hex": "#FBFBF9",
                "sku": "AUR-PUREFRENC-CH-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "XXL",
                "color": "Chalk White",
                "color_hex": "#FBFBF9",
                "sku": "AUR-PUREFRENC-CH-XXL",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Sagebrush",
                "color_hex": "#9CAF88",
                "sku": "AUR-PUREFRENC-SA-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Sagebrush",
                "color_hex": "#9CAF88",
                "sku": "AUR-PUREFRENC-SA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Sagebrush",
                "color_hex": "#9CAF88",
                "sku": "AUR-PUREFRENC-SA-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Sagebrush",
                "color_hex": "#9CAF88",
                "sku": "AUR-PUREFRENC-SA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "XXL",
                "color": "Sagebrush",
                "color_hex": "#9CAF88",
                "sku": "AUR-PUREFRENC-SA-XXL",
                "stock_quantity": 32,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 91,
        "name": "Relaxed Italian Linen Camp Shirt",
        "slug": "relaxed-italian-linen-camp-shirt",
        "description": "Square-hem resort shirt designed for effortless tropical evening wear with open revere collar.",
        "category_id": 19,
        "base_price": 6499.0,
        "discount_price": 5299.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Normandy Linen",
        "fit_type": "Cuban Camp-Collar Boxy",
        "care_instructions": "Machine wash gentle cold, hang dry.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 43,
        "sales_count": 172,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "linen-shirts",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Terracotta",
                "color_hex": "#C86D51",
                "sku": "AUR-RELAXEDIT-TE-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Terracotta",
                "color_hex": "#C86D51",
                "sku": "AUR-RELAXEDIT-TE-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Terracotta",
                "color_hex": "#C86D51",
                "sku": "AUR-RELAXEDIT-TE-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Terracotta",
                "color_hex": "#C86D51",
                "sku": "AUR-RELAXEDIT-TE-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Natural Flax",
                "color_hex": "#D5C7B0",
                "sku": "AUR-RELAXEDIT-NA-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Natural Flax",
                "color_hex": "#D5C7B0",
                "sku": "AUR-RELAXEDIT-NA-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Natural Flax",
                "color_hex": "#D5C7B0",
                "sku": "AUR-RELAXEDIT-NA-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Natural Flax",
                "color_hex": "#D5C7B0",
                "sku": "AUR-RELAXEDIT-NA-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 92,
        "name": "Washed Indigo Pure Linen Button-Up",
        "slug": "washed-indigo-pure-linen-button-up",
        "description": "Artisanal yarn-dyed indigo linen that patinas beautifully with every wear and wash.",
        "category_id": 19,
        "base_price": 6999.0,
        "discount_price": 5799.0,
        "brand": "Aura Haute Atelier",
        "material": "100% Linen with Indigo Garment Dye",
        "fit_type": "Tailored Relaxed",
        "care_instructions": "Wash cold separately with mild detergent.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 27,
        "sales_count": 108,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "linen-shirts",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1578932750294-f5075e85f44a?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "S",
                "color": "Medium Indigo",
                "color_hex": "#2C4D75",
                "sku": "AUR-WASHEDIND-ME-S",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Medium Indigo",
                "color_hex": "#2C4D75",
                "sku": "AUR-WASHEDIND-ME-M",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Medium Indigo",
                "color_hex": "#2C4D75",
                "sku": "AUR-WASHEDIND-ME-L",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Medium Indigo",
                "color_hex": "#2C4D75",
                "sku": "AUR-WASHEDIND-ME-XL",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "S",
                "color": "Bleached Chambray",
                "color_hex": "#8BA4C4",
                "sku": "AUR-WASHEDIND-BL-S",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "M",
                "color": "Bleached Chambray",
                "color_hex": "#8BA4C4",
                "sku": "AUR-WASHEDIND-BL-M",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "L",
                "color": "Bleached Chambray",
                "color_hex": "#8BA4C4",
                "sku": "AUR-WASHEDIND-BL-L",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "XL",
                "color": "Bleached Chambray",
                "color_hex": "#8BA4C4",
                "sku": "AUR-WASHEDIND-BL-XL",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 93,
        "name": "Tailored Linen-Cotton Gurkha Bermuda Shorts",
        "slug": "tailored-linen-cotton-gurkha-bermuda-shorts",
        "description": "Double-buckle Gurkha waistband tailored with forward pleats and cuffed hems for refined warm-weather elegance.",
        "category_id": 20,
        "base_price": 5499.0,
        "discount_price": 4499.0,
        "brand": "Aura Haute Atelier",
        "material": "55% Linen, 45% Organic Cotton",
        "fit_type": "High-Rise Gurkha Inseam",
        "care_instructions": "Machine wash cold gentle, warm iron.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 32,
        "sales_count": 128,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "linen-resortwear",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "30",
                "color": "Ivory Linen",
                "color_hex": "#F6F3EB",
                "sku": "AUR-TAILOREDL-IV-30",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "Ivory Linen",
                "color_hex": "#F6F3EB",
                "sku": "AUR-TAILOREDL-IV-32",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Ivory Linen",
                "color_hex": "#F6F3EB",
                "sku": "AUR-TAILOREDL-IV-34",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Ivory Linen",
                "color_hex": "#F6F3EB",
                "sku": "AUR-TAILOREDL-IV-36",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "30",
                "color": "Desert Sand",
                "color_hex": "#C4B296",
                "sku": "AUR-TAILOREDL-DE-30",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "32",
                "color": "Desert Sand",
                "color_hex": "#C4B296",
                "sku": "AUR-TAILOREDL-DE-32",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Desert Sand",
                "color_hex": "#C4B296",
                "sku": "AUR-TAILOREDL-DE-34",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Desert Sand",
                "color_hex": "#C4B296",
                "sku": "AUR-TAILOREDL-DE-36",
                "stock_quantity": 29,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 94,
        "name": "Horween Chromexcel Leather Service Boots",
        "slug": "horween-chromexcel-leather-service-boots",
        "description": "360-degree Goodyear welt construction with Dainite rubber outsoles and brass eyelets.",
        "category_id": 21,
        "base_price": 18999.0,
        "discount_price": 15999.0,
        "brand": "Aura Haute Atelier",
        "material": "Horween USA Chromexcel Pull-Up Leather",
        "fit_type": "Barrie Last Structured Fit",
        "care_instructions": "Condition with Venetian shoe cream.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 48,
        "sales_count": 192,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "leather-boots",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "7",
                "color": "Color 8 Burgundy",
                "color_hex": "#3B141E",
                "sku": "AUR-HORWEENCH-CO-7",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "8",
                "color": "Color 8 Burgundy",
                "color_hex": "#3B141E",
                "sku": "AUR-HORWEENCH-CO-8",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "9",
                "color": "Color 8 Burgundy",
                "color_hex": "#3B141E",
                "sku": "AUR-HORWEENCH-CO-9",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "10",
                "color": "Color 8 Burgundy",
                "color_hex": "#3B141E",
                "sku": "AUR-HORWEENCH-CO-10",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "11",
                "color": "Color 8 Burgundy",
                "color_hex": "#3B141E",
                "sku": "AUR-HORWEENCH-CO-11",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "7",
                "color": "Natural Chromexcel",
                "color_hex": "#8A593E",
                "sku": "AUR-HORWEENCH-NA-7",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "8",
                "color": "Natural Chromexcel",
                "color_hex": "#8A593E",
                "sku": "AUR-HORWEENCH-NA-8",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "9",
                "color": "Natural Chromexcel",
                "color_hex": "#8A593E",
                "sku": "AUR-HORWEENCH-NA-9",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "10",
                "color": "Natural Chromexcel",
                "color_hex": "#8A593E",
                "sku": "AUR-HORWEENCH-NA-10",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "11",
                "color": "Natural Chromexcel",
                "color_hex": "#8A593E",
                "sku": "AUR-HORWEENCH-NA-11",
                "stock_quantity": 32,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 95,
        "name": "Suede Jodhpur Hand-Burnished Boots",
        "slug": "suede-jodhpur-hand-burnished-boots",
        "description": "Wrap-around ankle strap with solid brass buckle over beveled leather waist soles.",
        "category_id": 21,
        "base_price": 16999.0,
        "discount_price": 13999.0,
        "brand": "Aura Haute Atelier",
        "material": "Italian Reverse Calf Suede",
        "fit_type": "Chiseled Almond Toe",
        "care_instructions": "Protect with nano suede water-stop spray.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 26,
        "sales_count": 104,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "leather-boots",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "7",
                "color": "Snuff Suede",
                "color_hex": "#7A5438",
                "sku": "AUR-SUEDEJODH-SN-7",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "8",
                "color": "Snuff Suede",
                "color_hex": "#7A5438",
                "sku": "AUR-SUEDEJODH-SN-8",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "9",
                "color": "Snuff Suede",
                "color_hex": "#7A5438",
                "sku": "AUR-SUEDEJODH-SN-9",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "10",
                "color": "Snuff Suede",
                "color_hex": "#7A5438",
                "sku": "AUR-SUEDEJODH-SN-10",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "11",
                "color": "Snuff Suede",
                "color_hex": "#7A5438",
                "sku": "AUR-SUEDEJODH-SN-11",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "7",
                "color": "Dark Brown Suede",
                "color_hex": "#382315",
                "sku": "AUR-SUEDEJODH-DA-7",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "8",
                "color": "Dark Brown Suede",
                "color_hex": "#382315",
                "sku": "AUR-SUEDEJODH-DA-8",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "9",
                "color": "Dark Brown Suede",
                "color_hex": "#382315",
                "sku": "AUR-SUEDEJODH-DA-9",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "10",
                "color": "Dark Brown Suede",
                "color_hex": "#382315",
                "sku": "AUR-SUEDEJODH-DA-10",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "11",
                "color": "Dark Brown Suede",
                "color_hex": "#382315",
                "sku": "AUR-SUEDEJODH-DA-11",
                "stock_quantity": 32,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 96,
        "name": "Wholecut Calfskin Oxford Formal Shoes",
        "slug": "wholecut-calfskin-oxford-formal-shoes",
        "description": "Cut from a single flawless piece of leather with closed five-eyelet lacing and channeled leather soles.",
        "category_id": 22,
        "base_price": 17999.0,
        "discount_price": 14999.0,
        "brand": "Aura Haute Atelier",
        "material": "Full-Grain French Boxcalf Leather",
        "fit_type": "Sleek European Dress Last",
        "care_instructions": "Mirror shine with beeswax polish.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 37,
        "sales_count": 148,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "dress-shoes-loafers",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "7",
                "color": "Piano Black",
                "color_hex": "#050505",
                "sku": "AUR-WHOLECUTC-PI-7",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "8",
                "color": "Piano Black",
                "color_hex": "#050505",
                "sku": "AUR-WHOLECUTC-PI-8",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "9",
                "color": "Piano Black",
                "color_hex": "#050505",
                "sku": "AUR-WHOLECUTC-PI-9",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "10",
                "color": "Piano Black",
                "color_hex": "#050505",
                "sku": "AUR-WHOLECUTC-PI-10",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "11",
                "color": "Piano Black",
                "color_hex": "#050505",
                "sku": "AUR-WHOLECUTC-PI-11",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "7",
                "color": "Dark Museum Plum",
                "color_hex": "#2E1A24",
                "sku": "AUR-WHOLECUTC-DA-7",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "8",
                "color": "Dark Museum Plum",
                "color_hex": "#2E1A24",
                "sku": "AUR-WHOLECUTC-DA-8",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "9",
                "color": "Dark Museum Plum",
                "color_hex": "#2E1A24",
                "sku": "AUR-WHOLECUTC-DA-9",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "10",
                "color": "Dark Museum Plum",
                "color_hex": "#2E1A24",
                "sku": "AUR-WHOLECUTC-DA-10",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "11",
                "color": "Dark Museum Plum",
                "color_hex": "#2E1A24",
                "sku": "AUR-WHOLECUTC-DA-11",
                "stock_quantity": 32,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 97,
        "name": "Belgian Horsebit Suede Loafers",
        "slug": "belgian-horsebit-suede-loafers",
        "description": "Padded leather insole with polished antique gold equestrian bit accent and soft unlined forefoot.",
        "category_id": 22,
        "base_price": 14999.0,
        "discount_price": 12499.0,
        "brand": "Aura Haute Atelier",
        "material": "Water-Resistant Italian Cashmere Suede",
        "fit_type": "Slip-On Loafer Last",
        "care_instructions": "Brush with natural crepe brush.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 44,
        "sales_count": 176,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "dress-shoes-loafers",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "7",
                "color": "Chocolate Suede",
                "color_hex": "#332219",
                "sku": "AUR-BELGIANHO-CH-7",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "8",
                "color": "Chocolate Suede",
                "color_hex": "#332219",
                "sku": "AUR-BELGIANHO-CH-8",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "9",
                "color": "Chocolate Suede",
                "color_hex": "#332219",
                "sku": "AUR-BELGIANHO-CH-9",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "10",
                "color": "Chocolate Suede",
                "color_hex": "#332219",
                "sku": "AUR-BELGIANHO-CH-10",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "11",
                "color": "Chocolate Suede",
                "color_hex": "#332219",
                "sku": "AUR-BELGIANHO-CH-11",
                "stock_quantity": 27,
                "additional_price": 0.0
            },
            {
                "size": "7",
                "color": "Sand Beige",
                "color_hex": "#C6B49D",
                "sku": "AUR-BELGIANHO-SA-7",
                "stock_quantity": 20,
                "additional_price": 0.0
            },
            {
                "size": "8",
                "color": "Sand Beige",
                "color_hex": "#C6B49D",
                "sku": "AUR-BELGIANHO-SA-8",
                "stock_quantity": 23,
                "additional_price": 0.0
            },
            {
                "size": "9",
                "color": "Sand Beige",
                "color_hex": "#C6B49D",
                "sku": "AUR-BELGIANHO-SA-9",
                "stock_quantity": 26,
                "additional_price": 0.0
            },
            {
                "size": "10",
                "color": "Sand Beige",
                "color_hex": "#C6B49D",
                "sku": "AUR-BELGIANHO-SA-10",
                "stock_quantity": 29,
                "additional_price": 0.0
            },
            {
                "size": "11",
                "color": "Sand Beige",
                "color_hex": "#C6B49D",
                "sku": "AUR-BELGIANHO-SA-11",
                "stock_quantity": 32,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 98,
        "name": "Minimalist Full-Grain Leather Backpack",
        "slug": "minimalist-full-grain-leather-backpack",
        "description": "Dedicated padded 16-inch laptop compartment with water-resistant micro-suede lining and gunmetal hardware.",
        "category_id": 23,
        "base_price": 16999.0,
        "discount_price": 13999.0,
        "brand": "Aura Haute Atelier",
        "material": "Vegetable-Tanned Italian Vacchetta Leather",
        "fit_type": "16-Liter Architectural Pack",
        "care_instructions": "Condition annually with leather balm.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 53,
        "sales_count": 212,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "leather-bags-luggage",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "One Size",
                "color": "Onyx Black",
                "color_hex": "#141414",
                "sku": "AUR-MINIMALIST-ON-One Size",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "One Size",
                "color": "Vintage Chestnut",
                "color_hex": "#663B1E",
                "sku": "AUR-MINIMALIST-VI-One Size",
                "stock_quantity": 20,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 99,
        "name": "Italian Bridle Leather Reversible Dress Belt",
        "slug": "italian-bridle-leather-reversible-dress-belt",
        "description": "Dual-finish strap (Black & Dark Cognac) with solid palladium-plated brass buckle mechanism.",
        "category_id": 24,
        "base_price": 4499.0,
        "discount_price": 3699.0,
        "brand": "Aura Haute Atelier",
        "material": "Full-Grain English Bridle Leather (32mm)",
        "fit_type": "Reversible Rotating Buckle",
        "care_instructions": "Wipe with damp cloth.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 4.9,
        "review_count": 68,
        "sales_count": 272,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "accessories-fine-goods",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "32",
                "color": "Black & Cognac Reversible",
                "color_hex": "#181818",
                "sku": "AUR-ITALIANBR-BL-32",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "34",
                "color": "Black & Cognac Reversible",
                "color_hex": "#181818",
                "sku": "AUR-ITALIANBR-BL-34",
                "stock_quantity": 18,
                "additional_price": 0.0
            },
            {
                "size": "36",
                "color": "Black & Cognac Reversible",
                "color_hex": "#181818",
                "sku": "AUR-ITALIANBR-BL-36",
                "stock_quantity": 21,
                "additional_price": 0.0
            },
            {
                "size": "38",
                "color": "Black & Cognac Reversible",
                "color_hex": "#181818",
                "sku": "AUR-ITALIANBR-BL-38",
                "stock_quantity": 24,
                "additional_price": 0.0
            },
            {
                "size": "40",
                "color": "Black & Cognac Reversible",
                "color_hex": "#181818",
                "sku": "AUR-ITALIANBR-BL-40",
                "stock_quantity": 27,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 100,
        "name": "Cashmere-Silk Ombre Jacquard Scarf",
        "slug": "cashmere-silk-ombre-jacquard-scarf",
        "description": "Feather-light double-shaded ombre weave with delicate hand-frayed eyelashes at edges.",
        "category_id": 24,
        "base_price": 6999.0,
        "discount_price": 5499.0,
        "brand": "Aura Haute Atelier",
        "material": "70% Mongolian Cashmere, 30% Mulberry Silk",
        "fit_type": "70cm x 200cm Eyelash Fringe",
        "care_instructions": "Dry clean only.",
        "is_featured": 1,
        "is_active": 1,
        "average_rating": 5.0,
        "review_count": 41,
        "sales_count": 164,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "accessories-fine-goods",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "One Size",
                "color": "Charcoal to Silver Ombre",
                "color_hex": "#484D54",
                "sku": "AUR-CASHMERES-CH-One Size",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "One Size",
                "color": "Navy to Ice Blue Ombre",
                "color_hex": "#23395B",
                "sku": "AUR-CASHMERES-NA-One Size",
                "stock_quantity": 20,
                "additional_price": 0.0
            }
        ]
    },
    {
        "id": 101,
        "name": "Full-Grain Bifold Leather Card Wallet",
        "slug": "full-grain-bifold-leather-card-wallet",
        "description": "RFID-blocking ultra-thin minimalist wallet hand-stitched with waxed linen thread and burnished edges.",
        "category_id": 24,
        "base_price": 3999.0,
        "discount_price": 3299.0,
        "brand": "Aura Haute Atelier",
        "material": "Tuscan Vegetable-Tanned Buttero Leather",
        "fit_type": "Slim 6-Pocket Bifold",
        "care_instructions": "Develops unique patina with handling.",
        "is_featured": 0,
        "is_active": 1,
        "average_rating": 4.8,
        "review_count": 84,
        "sales_count": 336,
        "created_at": "2026-11-11 11:06:12",
        "updated_at": "2026-11-11 11:06:12",
        "category_slug": "accessories-fine-goods",
        "images": [
            {
                "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=1200&q=85",
                "is_primary": 1,
                "display_order": 1
            }
        ],
        "variants": [
            {
                "size": "One Size",
                "color": "London Tan",
                "color_hex": "#9C6237",
                "sku": "AUR-FULLGRAIN-LO-One Size",
                "stock_quantity": 15,
                "additional_price": 0.0
            },
            {
                "size": "One Size",
                "color": "Classic Black",
                "color_hex": "#121212",
                "sku": "AUR-FULLGRAIN-CL-One Size",
                "stock_quantity": 20,
                "additional_price": 0.0
            }
        ]
    }
]

def seed_database(target_app=None):
    app = target_app if target_app is not None else create_app('development')
    with app.app_context():
        print("Recreating database tables...")
        db.drop_all()
        db.create_all()

        # 1. Categories
        print("Seeding 24 Refined Categories...")
        cat_map = {}
        for cat in CATEGORIES_DATA:
            c = Category(
                name=cat['name'],
                slug=cat['slug'],
                description=cat['description'],
                image_url=cat['image_url'],
                is_featured=cat['is_featured']
            )
            db.session.add(c)
            db.session.flush()
            cat_map[cat['slug']] = c.id

        # 2. Users (Admin + Customers)
        print("Seeding Users...")
        admin = User(
            email='tanwaransh46@gmail.com',
            full_name='Ansh Tanwar',
            phone='+91 98765 43210',
            role='admin',
            is_active=True
        )
        admin.set_password('Tanwar@12')
        db.session.add(admin)

        # Seed sample customers
        for i in range(1, 15):
            u = User(
                email=f'client{i}@aura-atelier.com',
                full_name=fake.name(),
                phone=fake.phone_number()[:20],
                role='customer',
                is_active=True
            )
            u.set_password('Aura@2026')
            db.session.add(u)
        db.session.flush()

        # 3. Products
        print("Seeding 101 Handcrafted Luxury Products...")
        for p in PRODUCTS_DATA:
            cat_id = cat_map.get(p['category_slug'])
            if not cat_id:
                continue
            prod = Product(
                name=p['name'],
                slug=p['slug'],
                description=p['description'],
                category_id=cat_id,
                base_price=p['base_price'],
                discount_price=p.get('discount_price'),
                brand=p.get('brand', 'Aura Haute Atelier'),
                material=p.get('material', 'Luxury Natural Fibers'),
                fit_type=p.get('fit_type', 'Tailored Fit'),
                care_instructions=p.get('care_instructions', 'Specialist luxury dry clean only.'),
                is_featured=p.get('is_featured', False),
                is_active=True,
                average_rating=p.get('average_rating', 4.9),
                review_count=p.get('review_count', 25),
                sales_count=p.get('sales_count', 50)
            )
            db.session.add(prod)
            db.session.flush()

            # Images
            for img in p.get('images', []):
                p_img = ProductImage(
                    product_id=prod.id,
                    image_url=img['image_url'],
                    is_primary=img['is_primary'],
                    display_order=img['display_order']
                )
                db.session.add(p_img)

            # Variants
            for v in p.get('variants', []):
                p_var = ProductVariant(
                    product_id=prod.id,
                    size=v['size'],
                    color=v['color'],
                    color_hex=v['color_hex'],
                    sku=v['sku'],
                    stock_quantity=v['stock_quantity'],
                    additional_price=v.get('additional_price', 0.0)
                )
                db.session.add(p_var)

        # 4. Coupons
        print("Seeding Promotional Privileges & Coupons...")
        coupons = [
            Coupon(code='WELCOME15', discount_type='percent', discount_value=15.0, min_purchase_amount=5000.0, max_discount_amount=3000.0, is_active=True),
            Coupon(code='AURA20', discount_type='percent', discount_value=20.0, min_purchase_amount=10000.0, max_discount_amount=5000.0, is_active=True),
            Coupon(code='VIPHAUTE', discount_type='fixed', discount_value=2500.0, min_purchase_amount=15000.0, is_active=True),
        ]
        for cp in coupons:
            db.session.add(cp)

        db.session.commit()
        print("Database successfully seeded with 24 refined categories and 101 luxury pieces!")

if __name__ == '__main__':
    seed_database()
