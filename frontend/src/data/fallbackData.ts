import { Product, Category } from '../types';

export const FALLBACK_CATEGORIES: Category[] = [
  {
    "id": 1,
    "name": "Women's Dresses",
    "slug": "womens-dresses",
    "description": "Effortless silhouettes from relaxed daywear to evening glamour.",
    "image_url": "/images/categories/womens-dresses.jpg",
    "is_featured": true,
    "product_count": 4
  },
  {
    "id": 2,
    "name": "Men's Shirts & Polos",
    "slug": "mens-shirts",
    "description": "Tailored poplins, breathable linen button-downs, and refined knit polos.",
    "image_url": "/images/categories/mens-shirts.jpg",
    "is_featured": true,
    "product_count": 4
  },
  {
    "id": 3,
    "name": "Tailored Blazers & Coats",
    "slug": "blazers-coats",
    "description": "Architectural tailoring and premium wool-blend outerwear for year-round sophistication.",
    "image_url": "/images/categories/blazers-coats.jpg",
    "is_featured": true,
    "product_count": 4
  },
  {
    "id": 4,
    "name": "Fine Knitwear & Sweaters",
    "slug": "knitwear-sweaters",
    "description": "Ultra-soft Mongolian cashmere, merino wool crews, and relaxed cardigans.",
    "image_url": "/images/categories/knitwear-sweaters.jpg",
    "is_featured": true,
    "product_count": 4
  },
  {
    "id": 5,
    "name": "Trousers & Chinos",
    "slug": "trousers-chinos",
    "description": "Pleated wide-leg trousers, tapered chinos, and smart casual bottoms.",
    "image_url": "/images/categories/trousers-chinos.jpg",
    "is_featured": false,
    "product_count": 3
  },
  {
    "id": 6,
    "name": "Denim & Jeans",
    "slug": "denim-jeans",
    "description": "Japanese selvedge denim, modern straight cuts, and vintage washes.",
    "image_url": "/images/categories/denim-jeans.jpg",
    "is_featured": true,
    "product_count": 3
  },
  {
    "id": 7,
    "name": "Premium Loungewear",
    "slug": "loungewear",
    "description": "Organic cotton hoodies, French terry joggers, and elevated relaxed staples.",
    "image_url": "/images/categories/loungewear.jpg",
    "is_featured": false,
    "product_count": 2
  },
  {
    "id": 8,
    "name": "Activewear & Performance",
    "slug": "activewear",
    "description": "Seamless moisture-wicking sets and technical performance apparel.",
    "image_url": "/images/categories/activewear.jpg",
    "is_featured": false,
    "product_count": 2
  },
  {
    "id": 9,
    "name": "Jackets & Outerwear",
    "slug": "jackets-outerwear",
    "description": "Water-resistant parkas, suede jackets, and insulated trench coats.",
    "image_url": "/images/categories/jackets-outerwear.jpg",
    "is_featured": true,
    "product_count": 4
  },
  {
    "id": 10,
    "name": "Summer Linen Collection",
    "slug": "summer-linen",
    "description": "Airy European flax linen garments crafted for warm coastal days.",
    "image_url": "/images/categories/summer-linen.jpg",
    "is_featured": true,
    "product_count": 2
  },
  {
    "id": 11,
    "name": "Footwear & Boots",
    "slug": "footwear",
    "description": "Handcrafted leather Chelsea boots, minimalist sneakers, and loafers.",
    "image_url": "/images/categories/footwear.jpg",
    "is_featured": false,
    "product_count": 2
  },
  {
    "id": 12,
    "name": "Leather & Accessories",
    "slug": "accessories",
    "description": "Full-grain leather belts, silk scarves, wool beanies, and tote bags.",
    "image_url": "/images/categories/accessories.jpg",
    "is_featured": false,
    "product_count": 2
  }
];

export const FALLBACK_PRODUCTS: Product[] = [
  {
    "id": 1,
    "name": "Spanish Goat Suede Harrington Bomber Jacket",
    "slug": "jackets-outerwear-01-b6dcd",
    "description": "Crafted from velvety Spanish goat suede with a butter-soft hand feel. Finished with ribbed wool cuffs and hem, an antique brass two-way front zipper, and lustrous breathable cupro lining.",
    "category_id": 9,
    "category_name": "Jackets & Outerwear",
    "category_slug": "jackets-outerwear",
    "base_price": 13999.0,
    "discount_price": 11999.0,
    "effective_price": 11999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Spanish Goat Suede Leather",
    "fit_type": "Classic Bomber Fit",
    "care_instructions": "Specialist leather clean only",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.4,
    "review_count": 22,
    "sales_count": 129,
    "total_stock": 279,
    "in_stock": true,
    "primary_image": "/images/products/spanish-goat-suede-harrington-bomber-jacket-caramel-suede.jpg",
    "created_at": "2026-11-06T17:42:14.473145",
    "images": [
      {
        "id": 1,
        "product_id": 1,
        "image_url": "/images/products/spanish-goat-suede-harrington-bomber-jacket-caramel-suede.jpg",
        "color": "Caramel Suede",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Caramel Suede",
        "color_hex": "#C19A6B",
        "image_url": "/images/products/spanish-goat-suede-harrington-bomber-jacket-caramel-suede.jpg"
      },
      {
        "color": "Noir Black Leather",
        "color_hex": "#1A1A1A",
        "image_url": "/images/products/spanish-goat-suede-harrington-bomber-jacket-noir-black-leather.jpg"
      }
    ]
  },
  {
    "id": 2,
    "name": "Spanish Merino Shearling Aviator Flight Jacket",
    "slug": "jackets-outerwear-02-b6892",
    "description": "Handcrafted from dense Spanish merino shearling with a thick fleece collar, adjustable buckled throat latch, and heavy-duty antiqued brass hardware.",
    "category_id": 9,
    "category_name": "Jackets & Outerwear",
    "category_slug": "jackets-outerwear",
    "base_price": 18999.0,
    "discount_price": 15999.0,
    "effective_price": 15999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Genuine Merino Shearling & Leather",
    "fit_type": "Heritage Aviator Regular Fit",
    "care_instructions": "Specialist leather clean only",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.4,
    "review_count": 13,
    "sales_count": 85,
    "total_stock": 286,
    "in_stock": true,
    "primary_image": "/images/products/spanish-merino-shearling-aviator-flight-jacket-cognac-tan-shearling.jpg",
    "created_at": "2026-11-06T17:42:14.475148",
    "images": [
      {
        "id": 3,
        "product_id": 2,
        "image_url": "/images/products/spanish-merino-shearling-aviator-flight-jacket-cognac-tan-shearling.jpg",
        "color": "Cognac Tan Shearling",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Cognac Tan Shearling",
        "color_hex": "#9E5B32",
        "image_url": "/images/products/spanish-merino-shearling-aviator-flight-jacket-cognac-tan-shearling.jpg"
      },
      {
        "color": "Noir Black Moto",
        "color_hex": "#1A1A1A",
        "image_url": "/images/products/spanish-merino-shearling-aviator-flight-jacket-noir-black-moto.jpg"
      }
    ]
  },
  {
    "id": 3,
    "name": "StormShield 750-Fill Down Expedition Parka",
    "slug": "jackets-outerwear-03-76af6",
    "description": "Waterproof technical shell packed with 750 fill power RDS down. Designed with an insulated storm hood, fleece-lined hand pockets, and internal storm cuffs.",
    "category_id": 9,
    "category_name": "Jackets & Outerwear",
    "category_slug": "jackets-outerwear",
    "base_price": 14499.0,
    "discount_price": 12299.0,
    "effective_price": 12299.0,
    "brand": "Aura Haute Collection",
    "material": "Waterproof Shell & 90/10 RDS Goose Down",
    "fit_type": "Expedition Fit",
    "care_instructions": "Machine wash cold gentle with down wash",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.8,
    "review_count": 17,
    "sales_count": 126,
    "total_stock": 257,
    "in_stock": true,
    "primary_image": "/images/products/stormshield-750-fill-down-expedition-parka-forest-olive-green.jpg",
    "created_at": "2026-11-06T17:42:14.481166",
    "images": [
      {
        "id": 5,
        "product_id": 3,
        "image_url": "/images/products/stormshield-750-fill-down-expedition-parka-forest-olive-green.jpg",
        "color": "Forest Olive Green",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Forest Olive Green",
        "color_hex": "#3B4A3F",
        "image_url": "/images/products/stormshield-750-fill-down-expedition-parka-forest-olive-green.jpg"
      },
      {
        "color": "Matte Black Parka",
        "color_hex": "#1A1A1A",
        "image_url": "/images/products/stormshield-750-fill-down-expedition-parka-matte-black-parka.jpg"
      }
    ]
  },
  {
    "id": 4,
    "name": "Cafe Racer Full-Grain Leather Moto Jacket",
    "slug": "jackets-outerwear-04-b9bdf",
    "description": "Iconic racer silhouette in full-grain cowhide leather with a mandarin snap collar, zippered cuffs, quilted shoulder detailing, and satin lining.",
    "category_id": 9,
    "category_name": "Jackets & Outerwear",
    "category_slug": "jackets-outerwear",
    "base_price": 15999.0,
    "discount_price": 13499.0,
    "effective_price": 13499.0,
    "brand": "Aura Haute Collection",
    "material": "100% Full-Grain Cowhide Leather",
    "fit_type": "Tailored Moto Fit",
    "care_instructions": "Condition with leather balm; specialist clean",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.7,
    "review_count": 23,
    "sales_count": 128,
    "total_stock": 280,
    "in_stock": true,
    "primary_image": "/images/products/cafe-racer-full-grain-leather-moto-jacket-noir-black.jpg",
    "created_at": "2026-11-06T17:42:14.484366",
    "images": [
      {
        "id": 7,
        "product_id": 4,
        "image_url": "/images/products/cafe-racer-full-grain-leather-moto-jacket-noir-black.jpg",
        "color": "Noir Black",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Noir Black",
        "color_hex": "#1A1A1A",
        "image_url": "/images/products/cafe-racer-full-grain-leather-moto-jacket-noir-black.jpg"
      },
      {
        "color": "Caramel Suede",
        "color_hex": "#C19A6B",
        "image_url": "/images/products/cafe-racer-full-grain-leather-moto-jacket-caramel-suede.jpg"
      }
    ]
  },
  {
    "id": 5,
    "name": "Mulberry Silk Bias-Cut Slip Dress",
    "slug": "womens-dresses-05-006c3",
    "description": "Tailored from heavyweight 22-momme Mulberry silk that drapes gracefully along natural contours with a cowl neckline and adjustable straps.",
    "category_id": 1,
    "category_name": "Women's Dresses",
    "category_slug": "womens-dresses",
    "base_price": 7499.0,
    "discount_price": 6299.0,
    "effective_price": 6299.0,
    "brand": "Aura Haute Collection",
    "material": "100% Grade 6A Mulberry Silk",
    "fit_type": "Bias Cut / Fluid",
    "care_instructions": "Specialist dry clean",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.5,
    "review_count": 6,
    "sales_count": 70,
    "total_stock": 276,
    "in_stock": true,
    "primary_image": "/images/products/mulberry-silk-bias-cut-slip-dress-champagne-ivory.jpg",
    "created_at": "2026-11-06T17:42:14.486885",
    "images": [
      {
        "id": 9,
        "product_id": 5,
        "image_url": "/images/products/mulberry-silk-bias-cut-slip-dress-champagne-ivory.jpg",
        "color": "Champagne Ivory",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Champagne Ivory",
        "color_hex": "#F3EDE2",
        "image_url": "/images/products/mulberry-silk-bias-cut-slip-dress-champagne-ivory.jpg"
      },
      {
        "color": "Emerald Green",
        "color_hex": "#0E4D3E",
        "image_url": "/images/products/mulberry-silk-bias-cut-slip-dress-emerald-green.jpg"
      }
    ]
  },
  {
    "id": 6,
    "name": "Duchess Cotton Velvet Gala Evening Gown",
    "slug": "womens-dresses-06-65c56",
    "description": "Dramatic floor-length gown crafted from plush Italian cotton velvet featuring a sculpted off-shoulder neckline and subtle side split.",
    "category_id": 1,
    "category_name": "Women's Dresses",
    "category_slug": "womens-dresses",
    "base_price": 9999.0,
    "discount_price": 8499.0,
    "effective_price": 8499.0,
    "brand": "Aura Haute Collection",
    "material": "98% Cotton Velvet, 2% Elastane",
    "fit_type": "Fitted Bodice / A-Line Skirt",
    "care_instructions": "Dry clean only",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.5,
    "review_count": 23,
    "sales_count": 118,
    "total_stock": 258,
    "in_stock": true,
    "primary_image": "/images/products/duchess-cotton-velvet-gala-evening-gown-burgundy-wine.jpg",
    "created_at": "2026-11-06T17:42:14.489886",
    "images": [
      {
        "id": 11,
        "product_id": 6,
        "image_url": "/images/products/duchess-cotton-velvet-gala-evening-gown-burgundy-wine.jpg",
        "color": "Burgundy Wine",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Burgundy Wine",
        "color_hex": "#6B1D2F",
        "image_url": "/images/products/duchess-cotton-velvet-gala-evening-gown-burgundy-wine.jpg"
      },
      {
        "color": "Midnight Noir",
        "color_hex": "#141416",
        "image_url": "/images/products/duchess-cotton-velvet-gala-evening-gown-midnight-noir.jpg"
      }
    ]
  },
  {
    "id": 7,
    "name": "French Flax Belted Linen Shirtdress",
    "slug": "womens-dresses-07-2fc53",
    "description": "Spun from pre-washed Normandy flax linen that softens beautifully with wear. Features natural mother-of-pearl buttons and a self-tie sash.",
    "category_id": 1,
    "category_name": "Women's Dresses",
    "category_slug": "womens-dresses",
    "base_price": 5499.0,
    "discount_price": 4699.0,
    "effective_price": 4699.0,
    "brand": "Aura Haute Collection",
    "material": "100% European Flax Linen",
    "fit_type": "Relaxed Fit",
    "care_instructions": "Machine wash cold delicate",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.8,
    "review_count": 24,
    "sales_count": 64,
    "total_stock": 267,
    "in_stock": true,
    "primary_image": "/images/products/french-flax-belted-linen-shirtdress-sage-olive.jpg",
    "created_at": "2026-11-06T17:42:14.491927",
    "images": [
      {
        "id": 13,
        "product_id": 7,
        "image_url": "/images/products/french-flax-belted-linen-shirtdress-sage-olive.jpg",
        "color": "Sage Olive",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Sage Olive",
        "color_hex": "#6B7C59",
        "image_url": "/images/products/french-flax-belted-linen-shirtdress-sage-olive.jpg"
      },
      {
        "color": "Oatmeal Natural",
        "color_hex": "#DCCBB5",
        "image_url": "/images/products/french-flax-belted-linen-shirtdress-oatmeal-natural.jpg"
      }
    ]
  },
  {
    "id": 8,
    "name": "Botanical Silk Chiffon Tiered Maxi Dress",
    "slug": "womens-dresses-08-cf93f",
    "description": "Ethereal floral silk chiffon dress with cascading micro-pleats, smocked elasticated waist, and delicate bishop sleeves.",
    "category_id": 1,
    "category_name": "Women's Dresses",
    "category_slug": "womens-dresses",
    "base_price": 8299.0,
    "discount_price": 6999.0,
    "effective_price": 6999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Silk Chiffon with Rayon Lining",
    "fit_type": "Flowing Tiered Fit",
    "care_instructions": "Hand wash cold or dry clean",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.9,
    "review_count": 9,
    "sales_count": 35,
    "total_stock": 245,
    "in_stock": true,
    "primary_image": "/images/products/botanical-silk-chiffon-tiered-maxi-dress-blush-rose-floral.jpg",
    "created_at": "2026-11-06T17:42:14.494935",
    "images": [
      {
        "id": 15,
        "product_id": 8,
        "image_url": "/images/products/botanical-silk-chiffon-tiered-maxi-dress-blush-rose-floral.jpg",
        "color": "Blush Rose Floral",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Blush Rose Floral",
        "color_hex": "#E29D9D",
        "image_url": "/images/products/botanical-silk-chiffon-tiered-maxi-dress-blush-rose-floral.jpg"
      },
      {
        "color": "Scarlet Blossom",
        "color_hex": "#A52A2A",
        "image_url": "/images/products/botanical-silk-chiffon-tiered-maxi-dress-scarlet-blossom.jpg"
      }
    ]
  },
  {
    "id": 9,
    "name": "Albini Two-Ply Royal Oxford Shirt",
    "slug": "mens-shirts-09-46401",
    "description": "Woven from superfine two-ply Egyptian cotton from renowned Italian mill Albini. Features a structured semi-spread collar and mother-of-pearl buttons.",
    "category_id": 2,
    "category_name": "Men's Shirts & Polos",
    "category_slug": "mens-shirts",
    "base_price": 4499.0,
    "discount_price": 3799.0,
    "effective_price": 3799.0,
    "brand": "Aura Haute Collection",
    "material": "100% Egyptian Giza Cotton",
    "fit_type": "Tailored Slim Fit",
    "care_instructions": "Machine wash warm, iron medium",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.7,
    "review_count": 12,
    "sales_count": 45,
    "total_stock": 248,
    "in_stock": true,
    "primary_image": "/images/products/albini-two-ply-royal-oxford-shirt-sky-blue-oxford.jpg",
    "created_at": "2026-11-06T17:42:14.498454",
    "images": [
      {
        "id": 17,
        "product_id": 9,
        "image_url": "/images/products/albini-two-ply-royal-oxford-shirt-sky-blue-oxford.jpg",
        "color": "Sky Blue Oxford",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Sky Blue Oxford",
        "color_hex": "#87CEEB",
        "image_url": "/images/products/albini-two-ply-royal-oxford-shirt-sky-blue-oxford.jpg"
      },
      {
        "color": "Crisp White Poplin",
        "color_hex": "#F8F9FA",
        "image_url": "/images/products/albini-two-ply-royal-oxford-shirt-crisp-white-poplin.jpg"
      }
    ]
  },
  {
    "id": 10,
    "name": "Riviera Camp-Collar Normandy Linen Shirt",
    "slug": "mens-shirts-10-50461",
    "description": "Casual relaxed camp-collar shirt cut from pre-washed French flax linen with an airy basket weave and straight split hem.",
    "category_id": 2,
    "category_name": "Men's Shirts & Polos",
    "category_slug": "mens-shirts",
    "base_price": 3999.0,
    "discount_price": 3299.0,
    "effective_price": 3299.0,
    "brand": "Aura Haute Collection",
    "material": "100% French Flax Linen",
    "fit_type": "Relaxed Fit",
    "care_instructions": "Machine wash cold gentle, line dry",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.7,
    "review_count": 25,
    "sales_count": 107,
    "total_stock": 310,
    "in_stock": true,
    "primary_image": "/images/products/riviera-camp-collar-normandy-linen-shirt-terracotta-rust.jpg",
    "created_at": "2026-11-06T17:42:14.500453",
    "images": [
      {
        "id": 19,
        "product_id": 10,
        "image_url": "/images/products/riviera-camp-collar-normandy-linen-shirt-terracotta-rust.jpg",
        "color": "Terracotta Rust",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Terracotta Rust",
        "color_hex": "#C85A32",
        "image_url": "/images/products/riviera-camp-collar-normandy-linen-shirt-terracotta-rust.jpg"
      },
      {
        "color": "Sage Olive Linen",
        "color_hex": "#667C59",
        "image_url": "/images/products/riviera-camp-collar-normandy-linen-shirt-sage-olive-linen.jpg"
      }
    ]
  },
  {
    "id": 11,
    "name": "Silk-Cotton Fine Gauge Knit Polo",
    "slug": "mens-shirts-11-5eb43",
    "description": "Elevated polo shirt spun with 70% long-staple cotton and 30% silk for a luxurious hand feel, seamless collar, and ribbed hems.",
    "category_id": 2,
    "category_name": "Men's Shirts & Polos",
    "category_slug": "mens-shirts",
    "base_price": 4299.0,
    "discount_price": null,
    "effective_price": 4299.0,
    "brand": "Aura Haute Collection",
    "material": "70% Long-Staple Cotton, 30% Silk",
    "fit_type": "Modern Tailored",
    "care_instructions": "Hand wash cold, dry flat",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.8,
    "review_count": 6,
    "sales_count": 47,
    "total_stock": 252,
    "in_stock": true,
    "primary_image": "/images/products/silk-cotton-fine-gauge-knit-polo-navy-melange.jpg",
    "created_at": "2026-11-06T17:42:14.503426",
    "images": [
      {
        "id": 21,
        "product_id": 11,
        "image_url": "/images/products/silk-cotton-fine-gauge-knit-polo-navy-melange.jpg",
        "color": "Navy Melange",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Navy Melange",
        "color_hex": "#1B2A4A",
        "image_url": "/images/products/silk-cotton-fine-gauge-knit-polo-navy-melange.jpg"
      },
      {
        "color": "Crisp White",
        "color_hex": "#F8F9FA",
        "image_url": "/images/products/silk-cotton-fine-gauge-knit-polo-crisp-white.jpg"
      }
    ]
  },
  {
    "id": 12,
    "name": "Heavyweight Japanese Cotton Twill Overshirt",
    "slug": "mens-shirts-12-af4aa",
    "description": "Substantial 340 GSM Japanese twill overshirt engineered with dual chest flap pockets and reinforced felled seams for versatile over-layering.",
    "category_id": 2,
    "category_name": "Men's Shirts & Polos",
    "category_slug": "mens-shirts",
    "base_price": 5299.0,
    "discount_price": 4499.0,
    "effective_price": 4499.0,
    "brand": "Aura Haute Collection",
    "material": "100% Japanese Cotton Twill",
    "fit_type": "Relaxed Overshirt Fit",
    "care_instructions": "Machine wash cold, inside out",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.8,
    "review_count": 6,
    "sales_count": 132,
    "total_stock": 225,
    "in_stock": true,
    "primary_image": "/images/products/heavyweight-japanese-cotton-twill-overshirt-midnight-navy.jpg",
    "created_at": "2026-11-06T17:42:14.505472",
    "images": [
      {
        "id": 23,
        "product_id": 12,
        "image_url": "/images/products/heavyweight-japanese-cotton-twill-overshirt-midnight-navy.jpg",
        "color": "Midnight Navy",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Midnight Navy",
        "color_hex": "#1A2332",
        "image_url": "/images/products/heavyweight-japanese-cotton-twill-overshirt-midnight-navy.jpg"
      },
      {
        "color": "Terracotta Clay",
        "color_hex": "#C85A32",
        "image_url": "/images/products/heavyweight-japanese-cotton-twill-overshirt-terracotta-clay.jpg"
      }
    ]
  },
  {
    "id": 13,
    "name": "Biella Virgin Wool Double-Breasted Blazer",
    "slug": "blazers-coats-13-de66f",
    "description": "Tailored from luxurious virgin wool twill from Biella, Italy. Features peak lapels, half-canvas construction, horn buttons, and double back vents.",
    "category_id": 3,
    "category_name": "Tailored Blazers & Coats",
    "category_slug": "blazers-coats",
    "base_price": 12999.0,
    "discount_price": 10999.0,
    "effective_price": 10999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Italian Virgin Wool",
    "fit_type": "Structured Tailored",
    "care_instructions": "Specialist dry clean",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.5,
    "review_count": 16,
    "sales_count": 87,
    "total_stock": 269,
    "in_stock": true,
    "primary_image": "/images/products/biella-virgin-wool-double-breasted-blazer-camel-tan-flannel.jpg",
    "created_at": "2026-11-06T17:42:14.508481",
    "images": [
      {
        "id": 25,
        "product_id": 13,
        "image_url": "/images/products/biella-virgin-wool-double-breasted-blazer-camel-tan-flannel.jpg",
        "color": "Camel Tan Flannel",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Camel Tan Flannel",
        "color_hex": "#C19A6B",
        "image_url": "/images/products/biella-virgin-wool-double-breasted-blazer-camel-tan-flannel.jpg"
      },
      {
        "color": "Midnight Navy Twill",
        "color_hex": "#1A2639",
        "image_url": "/images/products/biella-virgin-wool-double-breasted-blazer-midnight-navy-twill.jpg"
      }
    ]
  },
  {
    "id": 14,
    "name": "Double-Faced Cashmere & Wool Trench Overcoat",
    "slug": "blazers-coats-14-a8630",
    "description": "Exceptional thermal warmth woven with 85% Australian merino wool and 15% Mongolian cashmere. Hand-finished double-face craftsmanship with unlined interior.",
    "category_id": 3,
    "category_name": "Tailored Blazers & Coats",
    "category_slug": "blazers-coats",
    "base_price": 16999.0,
    "discount_price": 14499.0,
    "effective_price": 14499.0,
    "brand": "Aura Haute Collection",
    "material": "85% Merino Wool, 15% Cashmere",
    "fit_type": "Relaxed Overcoat Fit",
    "care_instructions": "Specialist dry clean",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.5,
    "review_count": 21,
    "sales_count": 88,
    "total_stock": 279,
    "in_stock": true,
    "primary_image": "/images/products/double-faced-cashmere-wool-trench-overcoat-charcoal-black-melange.jpg",
    "created_at": "2026-11-06T17:42:14.511060",
    "images": [
      {
        "id": 27,
        "product_id": 14,
        "image_url": "/images/products/double-faced-cashmere-wool-trench-overcoat-charcoal-black-melange.jpg",
        "color": "Charcoal Black Melange",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Charcoal Black Melange",
        "color_hex": "#212121",
        "image_url": "/images/products/double-faced-cashmere-wool-trench-overcoat-charcoal-black-melange.jpg"
      },
      {
        "color": "Camel Gabardine",
        "color_hex": "#C49E73",
        "image_url": "/images/products/double-faced-cashmere-wool-trench-overcoat-camel-gabardine.jpg"
      }
    ]
  },
  {
    "id": 15,
    "name": "Unstructured Belgian Linen Sport Coat",
    "slug": "blazers-coats-15-65706",
    "description": "Breezy tailored sport coat crafted with unlined shoulders and patch pockets from breathable Belgian flax linen.",
    "category_id": 3,
    "category_name": "Tailored Blazers & Coats",
    "category_slug": "blazers-coats",
    "base_price": 9499.0,
    "discount_price": 7999.0,
    "effective_price": 7999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Belgian Linen",
    "fit_type": "Soft Tailoring",
    "care_instructions": "Dry clean only",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.6,
    "review_count": 8,
    "sales_count": 124,
    "total_stock": 260,
    "in_stock": true,
    "primary_image": "/images/products/unstructured-belgian-linen-sport-coat-midnight-navy.jpg",
    "created_at": "2026-11-06T17:42:14.514423",
    "images": [
      {
        "id": 29,
        "product_id": 15,
        "image_url": "/images/products/unstructured-belgian-linen-sport-coat-midnight-navy.jpg",
        "color": "Midnight Navy",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Midnight Navy",
        "color_hex": "#1A2639",
        "image_url": "/images/products/unstructured-belgian-linen-sport-coat-midnight-navy.jpg"
      },
      {
        "color": "Camel Tan",
        "color_hex": "#C19A6B",
        "image_url": "/images/products/unstructured-belgian-linen-sport-coat-camel-tan.jpg"
      }
    ]
  },
  {
    "id": 16,
    "name": "Weatherproof Cotton Gabardine Belted Trench",
    "slug": "blazers-coats-16-babfc",
    "description": "Timeless military trench coat cut from tightly woven water-repellent cotton gabardine. Features storm flap, buckled waist belt, and horn buttons.",
    "category_id": 3,
    "category_name": "Tailored Blazers & Coats",
    "category_slug": "blazers-coats",
    "base_price": 14999.0,
    "discount_price": null,
    "effective_price": 14999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Weatherproof Cotton Gabardine",
    "fit_type": "Classic Trench Cut",
    "care_instructions": "Dry clean only",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.6,
    "review_count": 22,
    "sales_count": 96,
    "total_stock": 281,
    "in_stock": true,
    "primary_image": "/images/products/weatherproof-cotton-gabardine-belted-trench-honey-camel-trench.jpg",
    "created_at": "2026-11-06T17:42:14.518363",
    "images": [
      {
        "id": 31,
        "product_id": 16,
        "image_url": "/images/products/weatherproof-cotton-gabardine-belted-trench-honey-camel-trench.jpg",
        "color": "Honey Camel Trench",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Honey Camel Trench",
        "color_hex": "#C49E73",
        "image_url": "/images/products/weatherproof-cotton-gabardine-belted-trench-honey-camel-trench.jpg"
      },
      {
        "color": "Charcoal Slate",
        "color_hex": "#212121",
        "image_url": "/images/products/weatherproof-cotton-gabardine-belted-trench-charcoal-slate.jpg"
      }
    ]
  },
  {
    "id": 17,
    "name": "Grade-A Mongolian Cashmere Crewneck",
    "slug": "knitwear-sweaters-17-178d7",
    "description": "Supreme softness spun from 2-ply 100% Grade-A inner Mongolian cashmere. Features ribbed collar, cuffs, and hem for timeless warmth.",
    "category_id": 4,
    "category_name": "Fine Knitwear & Sweaters",
    "category_slug": "knitwear-sweaters",
    "base_price": 8999.0,
    "discount_price": 7499.0,
    "effective_price": 7499.0,
    "brand": "Aura Haute Collection",
    "material": "100% Grade-A Mongolian Cashmere",
    "fit_type": "Classic Fit",
    "care_instructions": "Hand wash cold, dry flat",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.5,
    "review_count": 20,
    "sales_count": 53,
    "total_stock": 322,
    "in_stock": true,
    "primary_image": "/images/products/grade-a-mongolian-cashmere-crewneck-cream-oatmeal.jpg",
    "created_at": "2026-11-06T17:42:14.522101",
    "images": [
      {
        "id": 33,
        "product_id": 17,
        "image_url": "/images/products/grade-a-mongolian-cashmere-crewneck-cream-oatmeal.jpg",
        "color": "Cream Oatmeal",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Cream Oatmeal",
        "color_hex": "#E8DFD1",
        "image_url": "/images/products/grade-a-mongolian-cashmere-crewneck-cream-oatmeal.jpg"
      },
      {
        "color": "Charcoal Heather",
        "color_hex": "#343A40",
        "image_url": "/images/products/grade-a-mongolian-cashmere-crewneck-charcoal-heather.jpg"
      }
    ]
  },
  {
    "id": 18,
    "name": "Heavyweight Cable-Knit Merino Cardigan",
    "slug": "knitwear-sweaters-18-829d1",
    "description": "Chunky Aran cable knit woven from 100% Australian extra-fine merino wool with hand-stitched leather buttons and front patch pockets.",
    "category_id": 4,
    "category_name": "Fine Knitwear & Sweaters",
    "category_slug": "knitwear-sweaters",
    "base_price": 7299.0,
    "discount_price": 5999.0,
    "effective_price": 5999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Extra-Fine Merino Wool",
    "fit_type": "Relaxed Fit",
    "care_instructions": "Dry clean or gentle hand wash",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.6,
    "review_count": 10,
    "sales_count": 81,
    "total_stock": 269,
    "in_stock": true,
    "primary_image": "/images/products/heavyweight-cable-knit-merino-cardigan-winter-ecru-white.jpg",
    "created_at": "2026-11-06T17:42:14.524838",
    "images": [
      {
        "id": 35,
        "product_id": 18,
        "image_url": "/images/products/heavyweight-cable-knit-merino-cardigan-winter-ecru-white.jpg",
        "color": "Winter Ecru White",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Winter Ecru White",
        "color_hex": "#F4F0E8",
        "image_url": "/images/products/heavyweight-cable-knit-merino-cardigan-winter-ecru-white.jpg"
      },
      {
        "color": "Cognac Ribbed",
        "color_hex": "#8B4513",
        "image_url": "/images/products/heavyweight-cable-knit-merino-cardigan-cognac-ribbed.jpg"
      }
    ]
  },
  {
    "id": 19,
    "name": "Fine Gauge Merino Wool Turtleneck",
    "slug": "knitwear-sweaters-19-3bb08",
    "description": "Spun from 19.5-micron fine Australian merino wool in a silky rib knit. Designed to layer smoothly beneath tailored blazers and trench coats.",
    "category_id": 4,
    "category_name": "Fine Knitwear & Sweaters",
    "category_slug": "knitwear-sweaters",
    "base_price": 6299.0,
    "discount_price": null,
    "effective_price": 6299.0,
    "brand": "Aura Haute Collection",
    "material": "100% Fine Merino Wool",
    "fit_type": "Slim Tailored",
    "care_instructions": "Machine wash cold on wool cycle",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.6,
    "review_count": 20,
    "sales_count": 58,
    "total_stock": 234,
    "in_stock": true,
    "primary_image": "/images/products/fine-gauge-merino-wool-turtleneck-camel-heather.jpg",
    "created_at": "2026-11-06T17:42:14.528458",
    "images": [
      {
        "id": 37,
        "product_id": 19,
        "image_url": "/images/products/fine-gauge-merino-wool-turtleneck-camel-heather.jpg",
        "color": "Camel Heather",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Camel Heather",
        "color_hex": "#C19A6B",
        "image_url": "/images/products/fine-gauge-merino-wool-turtleneck-camel-heather.jpg"
      },
      {
        "color": "Noir Black",
        "color_hex": "#1A1A1A",
        "image_url": "/images/products/fine-gauge-merino-wool-turtleneck-noir-black.jpg"
      }
    ]
  },
  {
    "id": 20,
    "name": "Brushed Alpaca Wool Relaxed Crew",
    "slug": "knitwear-sweaters-20-b3ed4",
    "description": "Fluffy, cloud-like texture knitted from a blend of Peruvian baby alpaca and wool. Warm, breathable, and finished with a comfortable ribbed collar.",
    "category_id": 4,
    "category_name": "Fine Knitwear & Sweaters",
    "category_slug": "knitwear-sweaters",
    "base_price": 7899.0,
    "discount_price": 6499.0,
    "effective_price": 6499.0,
    "brand": "Aura Haute Collection",
    "material": "60% Baby Alpaca, 28% Wool, 12% Polyamide",
    "fit_type": "Boxy Relaxed Fit",
    "care_instructions": "Hand wash cold, reshape and dry flat",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.5,
    "review_count": 24,
    "sales_count": 83,
    "total_stock": 257,
    "in_stock": true,
    "primary_image": "/images/products/brushed-alpaca-wool-relaxed-crew-charcoal-heather-melange.jpg",
    "created_at": "2026-11-06T17:42:14.532264",
    "images": [
      {
        "id": 39,
        "product_id": 20,
        "image_url": "/images/products/brushed-alpaca-wool-relaxed-crew-charcoal-heather-melange.jpg",
        "color": "Charcoal Heather Melange",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Charcoal Heather Melange",
        "color_hex": "#343A40",
        "image_url": "/images/products/brushed-alpaca-wool-relaxed-crew-charcoal-heather-melange.jpg"
      },
      {
        "color": "Winter Ecru White",
        "color_hex": "#F4F0E8",
        "image_url": "/images/products/brushed-alpaca-wool-relaxed-crew-winter-ecru-white.jpg"
      }
    ]
  },
  {
    "id": 21,
    "name": "Biella Tropical Wool Pleated Trousers",
    "slug": "trousers-chinos-21-555ca",
    "description": "Tailored with single front pleats, side adjusters, and a clean taper. Woven from breathable tropical wool for a sharp fluid drape in all seasons.",
    "category_id": 5,
    "category_name": "Trousers & Chinos",
    "category_slug": "trousers-chinos",
    "base_price": 6499.0,
    "discount_price": 5299.0,
    "effective_price": 5299.0,
    "brand": "Aura Haute Collection",
    "material": "100% Tropical Wool",
    "fit_type": "Tapered Pleated",
    "care_instructions": "Specialist dry clean",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.4,
    "review_count": 21,
    "sales_count": 111,
    "total_stock": 301,
    "in_stock": true,
    "primary_image": "/images/products/biella-tropical-wool-pleated-trousers-charcoal-slate-melange.jpg",
    "created_at": "2026-11-06T17:42:14.536561",
    "images": [
      {
        "id": 41,
        "product_id": 21,
        "image_url": "/images/products/biella-tropical-wool-pleated-trousers-charcoal-slate-melange.jpg",
        "color": "Charcoal Slate Melange",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Charcoal Slate Melange",
        "color_hex": "#343A40",
        "image_url": "/images/products/biella-tropical-wool-pleated-trousers-charcoal-slate-melange.jpg"
      },
      {
        "color": "Natural Oatmeal Linen",
        "color_hex": "#D8D2C2",
        "image_url": "/images/products/biella-tropical-wool-pleated-trousers-natural-oatmeal-linen.jpg"
      }
    ]
  },
  {
    "id": 22,
    "name": "Pima Stretch Cotton Tailored Chinos",
    "slug": "trousers-chinos-22-c09af",
    "description": "Cut from premium 98% long-staple pima cotton twill and 2% elastane for slight give. Features horn buttons and taped interior seams.",
    "category_id": 5,
    "category_name": "Trousers & Chinos",
    "category_slug": "trousers-chinos",
    "base_price": 4299.0,
    "discount_price": 3599.0,
    "effective_price": 3599.0,
    "brand": "Aura Haute Collection",
    "material": "98% Pima Cotton, 2% Elastane",
    "fit_type": "Slim Tapered",
    "care_instructions": "Machine wash cold",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.7,
    "review_count": 7,
    "sales_count": 76,
    "total_stock": 235,
    "in_stock": true,
    "primary_image": "/images/products/pima-stretch-cotton-tailored-chinos-classic-khaki-tan.jpg",
    "created_at": "2026-11-06T17:42:14.540269",
    "images": [
      {
        "id": 43,
        "product_id": 22,
        "image_url": "/images/products/pima-stretch-cotton-tailored-chinos-classic-khaki-tan.jpg",
        "color": "Classic Khaki Tan",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Classic Khaki Tan",
        "color_hex": "#C19A6B",
        "image_url": "/images/products/pima-stretch-cotton-tailored-chinos-classic-khaki-tan.jpg"
      },
      {
        "color": "Charcoal Grey",
        "color_hex": "#343A40",
        "image_url": "/images/products/pima-stretch-cotton-tailored-chinos-charcoal-grey.jpg"
      }
    ]
  },
  {
    "id": 23,
    "name": "Belgian Flax Linen Wide-Leg Trousers",
    "slug": "trousers-chinos-23-3c05a",
    "description": "High-waisted, fluid silhouette tailored with deep front pleats from heavyweight 280 GSM Belgian flax linen. Effortlessly relaxed and cool.",
    "category_id": 5,
    "category_name": "Trousers & Chinos",
    "category_slug": "trousers-chinos",
    "base_price": 5499.0,
    "discount_price": null,
    "effective_price": 5499.0,
    "brand": "Aura Haute Collection",
    "material": "100% Belgian Flax Linen",
    "fit_type": "Wide Leg Relaxed",
    "care_instructions": "Machine wash delicate, hang dry",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.7,
    "review_count": 19,
    "sales_count": 131,
    "total_stock": 289,
    "in_stock": true,
    "primary_image": "/images/products/belgian-flax-linen-wide-leg-trousers-ecru-natural-linen.jpg",
    "created_at": "2026-11-06T17:42:14.541949",
    "images": [
      {
        "id": 45,
        "product_id": 23,
        "image_url": "/images/products/belgian-flax-linen-wide-leg-trousers-ecru-natural-linen.jpg",
        "color": "Ecru Natural Linen",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Ecru Natural Linen",
        "color_hex": "#E8E2D5",
        "image_url": "/images/products/belgian-flax-linen-wide-leg-trousers-ecru-natural-linen.jpg"
      },
      {
        "color": "Charcoal Slate",
        "color_hex": "#343A40",
        "image_url": "/images/products/belgian-flax-linen-wide-leg-trousers-charcoal-slate.jpg"
      }
    ]
  },
  {
    "id": 24,
    "name": "Okayama 14oz Vintage Straight Jeans",
    "slug": "denim-jeans-24-cf33e",
    "description": "Crafted in Kojima, Japan from 14oz shuttle-loomed selvedge denim. Detailed with red-line selvedge ID, custom copper hardware, and genuine button fly.",
    "category_id": 6,
    "category_name": "Denim & Jeans",
    "category_slug": "denim-jeans",
    "base_price": 6999.0,
    "discount_price": 5899.0,
    "effective_price": 5899.0,
    "brand": "Aura Haute Collection",
    "material": "100% Long-Staple Japanese Cotton",
    "fit_type": "Classic Straight Leg",
    "care_instructions": "Wash sparingly inside out in cold water",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.5,
    "review_count": 9,
    "sales_count": 109,
    "total_stock": 258,
    "in_stock": true,
    "primary_image": "/images/products/okayama-14oz-vintage-straight-jeans-vintage-light-indigo.jpg",
    "created_at": "2026-11-06T17:42:14.543959",
    "images": [
      {
        "id": 47,
        "product_id": 24,
        "image_url": "/images/products/okayama-14oz-vintage-straight-jeans-vintage-light-indigo.jpg",
        "color": "Vintage Light Indigo",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Vintage Light Indigo",
        "color_hex": "#5B84B1",
        "image_url": "/images/products/okayama-14oz-vintage-straight-jeans-vintage-light-indigo.jpg"
      },
      {
        "color": "Dark Selvedge Indigo",
        "color_hex": "#1B2A4A",
        "image_url": "/images/products/okayama-14oz-vintage-straight-jeans-dark-selvedge-indigo.jpg"
      }
    ]
  },
  {
    "id": 25,
    "name": "Kuroki Raw Indigo Slim-Taper Jeans",
    "slug": "denim-jeans-25-99869",
    "description": "Tailored from 13.5oz rope-dyed Kuroki Mills raw denim. Starts crisp and molds to your body, developing personalized honeycombs and whiskers.",
    "category_id": 6,
    "category_name": "Denim & Jeans",
    "category_slug": "denim-jeans",
    "base_price": 6499.0,
    "discount_price": 5499.0,
    "effective_price": 5499.0,
    "brand": "Aura Haute Collection",
    "material": "99% Japanese Selvedge Cotton, 1% Comfort Stretch",
    "fit_type": "Slim Tapered",
    "care_instructions": "Cold soak, line dry",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.7,
    "review_count": 17,
    "sales_count": 35,
    "total_stock": 230,
    "in_stock": true,
    "primary_image": "/images/products/kuroki-raw-indigo-slim-taper-jeans-raw-dark-indigo.jpg",
    "created_at": "2026-11-06T17:42:14.547479",
    "images": [
      {
        "id": 49,
        "product_id": 25,
        "image_url": "/images/products/kuroki-raw-indigo-slim-taper-jeans-raw-dark-indigo.jpg",
        "color": "Raw Dark Indigo",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Raw Dark Indigo",
        "color_hex": "#1B2A4A",
        "image_url": "/images/products/kuroki-raw-indigo-slim-taper-jeans-raw-dark-indigo.jpg"
      },
      {
        "color": "Washed Charcoal Black",
        "color_hex": "#2F3136",
        "image_url": "/images/products/kuroki-raw-indigo-slim-taper-jeans-washed-charcoal-black.jpg"
      }
    ]
  },
  {
    "id": 26,
    "name": "Relaxed 90s Heritage Stonewash Jeans",
    "slug": "denim-jeans-26-a4ee4",
    "description": "Authentic loose silhouette inspired by iconic 90s casualwear. Cut from 100% regenerative ring-spun cotton denim with vintage stonewashing.",
    "category_id": 6,
    "category_name": "Denim & Jeans",
    "category_slug": "denim-jeans",
    "base_price": 5299.0,
    "discount_price": null,
    "effective_price": 5299.0,
    "brand": "Aura Haute Collection",
    "material": "100% Regenerative Cotton Denim",
    "fit_type": "Relaxed 90s Straight",
    "care_instructions": "Machine wash cold",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.9,
    "review_count": 12,
    "sales_count": 102,
    "total_stock": 269,
    "in_stock": true,
    "primary_image": "/images/products/relaxed-90s-heritage-stonewash-jeans-stonewash-sky-blue.jpg",
    "created_at": "2026-11-06T17:42:14.550479",
    "images": [
      {
        "id": 51,
        "product_id": 26,
        "image_url": "/images/products/relaxed-90s-heritage-stonewash-jeans-stonewash-sky-blue.jpg",
        "color": "Stonewash Sky Blue",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Stonewash Sky Blue",
        "color_hex": "#7DA0CA",
        "image_url": "/images/products/relaxed-90s-heritage-stonewash-jeans-stonewash-sky-blue.jpg"
      },
      {
        "color": "Vintage Light Indigo",
        "color_hex": "#5B84B1",
        "image_url": "/images/products/relaxed-90s-heritage-stonewash-jeans-vintage-light-indigo.jpg"
      }
    ]
  },
  {
    "id": 27,
    "name": "Heavyweight 450 GSM Organic Cotton Hoodie",
    "slug": "loungewear-27-10ca6",
    "description": "Crafted from ultra-dense 450 GSM organic French terry cotton. Features double-layered hood, flatlock stitching, and ribbed side mobility gussets.",
    "category_id": 7,
    "category_name": "Premium Loungewear",
    "category_slug": "loungewear",
    "base_price": 4299.0,
    "discount_price": 3499.0,
    "effective_price": 3499.0,
    "brand": "Aura Haute Collection",
    "material": "100% Combed Organic Cotton",
    "fit_type": "Relaxed Boxy Fit",
    "care_instructions": "Machine wash warm, tumble dry low",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.7,
    "review_count": 10,
    "sales_count": 38,
    "total_stock": 225,
    "in_stock": true,
    "primary_image": "/images/products/heavyweight-450-gsm-organic-cotton-hoodie-heather-grey-melange.jpg",
    "created_at": "2026-11-06T17:42:14.551994",
    "images": [
      {
        "id": 53,
        "product_id": 27,
        "image_url": "/images/products/heavyweight-450-gsm-organic-cotton-hoodie-heather-grey-melange.jpg",
        "color": "Heather Grey Melange",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Heather Grey Melange",
        "color_hex": "#9E9E9E",
        "image_url": "/images/products/heavyweight-450-gsm-organic-cotton-hoodie-heather-grey-melange.jpg"
      },
      {
        "color": "Oatmeal Natural",
        "color_hex": "#E5DEC9",
        "image_url": "/images/products/heavyweight-450-gsm-organic-cotton-hoodie-oatmeal-natural.jpg"
      }
    ]
  },
  {
    "id": 28,
    "name": "Organic Loopback French Terry Sweatpants",
    "slug": "loungewear-28-46530",
    "description": "Plush loopback organic cotton joggers with a drawstring elastic waist, tailored slanted welt pockets, and comfortable ribbed cuffs.",
    "category_id": 7,
    "category_name": "Premium Loungewear",
    "category_slug": "loungewear",
    "base_price": 3699.0,
    "discount_price": 2999.0,
    "effective_price": 2999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Organic French Terry Cotton",
    "fit_type": "Relaxed Tapered Fit",
    "care_instructions": "Machine wash cold with like colors",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.7,
    "review_count": 16,
    "sales_count": 68,
    "total_stock": 270,
    "in_stock": true,
    "primary_image": "/images/products/organic-loopback-french-terry-sweatpants-oatmeal-natural.jpg",
    "created_at": "2026-11-06T17:42:14.556042",
    "images": [
      {
        "id": 55,
        "product_id": 28,
        "image_url": "/images/products/organic-loopback-french-terry-sweatpants-oatmeal-natural.jpg",
        "color": "Oatmeal Natural",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Oatmeal Natural",
        "color_hex": "#E5DEC9",
        "image_url": "/images/products/organic-loopback-french-terry-sweatpants-oatmeal-natural.jpg"
      },
      {
        "color": "Heather Grey Melange",
        "color_hex": "#9E9E9E",
        "image_url": "/images/products/organic-loopback-french-terry-sweatpants-heather-grey-melange.jpg"
      }
    ]
  },
  {
    "id": 29,
    "name": "Seamless Ribbed Compression Workout Set",
    "slug": "activewear-29-f47f7",
    "description": "High-performance moisture-wicking four-way stretch fabric with targeted muscle support, zero-chafe flat seams, and breathable ventilation zones.",
    "category_id": 8,
    "category_name": "Activewear & Performance",
    "category_slug": "activewear",
    "base_price": 4499.0,
    "discount_price": 3699.0,
    "effective_price": 3699.0,
    "brand": "Aura Haute Collection",
    "material": "78% Recycled Polyamide, 22% Elastane",
    "fit_type": "Athletic Compression Fit",
    "care_instructions": "Machine wash cold, line dry",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.4,
    "review_count": 21,
    "sales_count": 42,
    "total_stock": 260,
    "in_stock": true,
    "primary_image": "/images/products/seamless-ribbed-compression-workout-set-dusty-rose-pink.jpg",
    "created_at": "2026-11-06T17:42:14.558561",
    "images": [
      {
        "id": 57,
        "product_id": 29,
        "image_url": "/images/products/seamless-ribbed-compression-workout-set-dusty-rose-pink.jpg",
        "color": "Dusty Rose Pink",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Dusty Rose Pink",
        "color_hex": "#D8A47F",
        "image_url": "/images/products/seamless-ribbed-compression-workout-set-dusty-rose-pink.jpg"
      },
      {
        "color": "Olive Green",
        "color_hex": "#556B2F",
        "image_url": "/images/products/seamless-ribbed-compression-workout-set-olive-green.jpg"
      }
    ]
  },
  {
    "id": 30,
    "name": "AeroShield Ultralight Performance Windbreaker",
    "slug": "activewear-30-bed78",
    "description": "Featherweight technical ripstop running jacket with DWR water-repellent coating, underarm ventilation eyelets, and packable pocket.",
    "category_id": 8,
    "category_name": "Activewear & Performance",
    "category_slug": "activewear",
    "base_price": 4999.0,
    "discount_price": 3999.0,
    "effective_price": 3999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Recycled Ripstop Nylon",
    "fit_type": "Athletic Slim Fit",
    "care_instructions": "Machine wash cold gentle",
    "is_featured": false,
    "is_active": true,
    "average_rating": 4.5,
    "review_count": 18,
    "sales_count": 63,
    "total_stock": 279,
    "in_stock": true,
    "primary_image": "/images/products/aeroshield-ultralight-performance-windbreaker-olive-sage.jpg",
    "created_at": "2026-11-06T17:42:14.563832",
    "images": [
      {
        "id": 59,
        "product_id": 30,
        "image_url": "/images/products/aeroshield-ultralight-performance-windbreaker-olive-sage.jpg",
        "color": "Olive Sage",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Olive Sage",
        "color_hex": "#556B2F",
        "image_url": "/images/products/aeroshield-ultralight-performance-windbreaker-olive-sage.jpg"
      },
      {
        "color": "Midnight Stealth Black",
        "color_hex": "#1A1A1A",
        "image_url": "/images/products/aeroshield-ultralight-performance-windbreaker-midnight-stealth-black.jpg"
      }
    ]
  },
  {
    "id": 31,
    "name": "Pre-Washed Normandy Linen Drawstring Trousers",
    "slug": "summer-linen-31-f66bc",
    "description": "Airy, relaxed-leg trousers with an elasticated drawstring waist and breathable open weave. Garment-washed for a soft touch and effortless drape.",
    "category_id": 10,
    "category_name": "Summer Linen Collection",
    "category_slug": "summer-linen",
    "base_price": 4499.0,
    "discount_price": 3799.0,
    "effective_price": 3799.0,
    "brand": "Aura Haute Collection",
    "material": "100% European Flax Linen",
    "fit_type": "Relaxed Straight Fit",
    "care_instructions": "Machine wash cold gentle, line dry",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.7,
    "review_count": 27,
    "sales_count": 93,
    "total_stock": 294,
    "in_stock": true,
    "primary_image": "/images/products/pre-washed-normandy-linen-drawstring-trousers-natural-oatmeal-linen.jpg",
    "created_at": "2026-11-06T17:42:14.566489",
    "images": [
      {
        "id": 61,
        "product_id": 31,
        "image_url": "/images/products/pre-washed-normandy-linen-drawstring-trousers-natural-oatmeal-linen.jpg",
        "color": "Natural Oatmeal Linen",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Natural Oatmeal Linen",
        "color_hex": "#E5DEC9",
        "image_url": "/images/products/pre-washed-normandy-linen-drawstring-trousers-natural-oatmeal-linen.jpg"
      },
      {
        "color": "Belgian Ecru Linen",
        "color_hex": "#D8D2C2",
        "image_url": "/images/products/pre-washed-normandy-linen-drawstring-trousers-belgian-ecru-linen.jpg"
      }
    ]
  },
  {
    "id": 32,
    "name": "European Flax Sleeveless Linen Jumpsuit",
    "slug": "summer-linen-32-3728f",
    "description": "Wide-leg minimalist jumpsuit cut from 100% French flax linen. Features a flattering square neckline, removable belt, and concealed back zip.",
    "category_id": 10,
    "category_name": "Summer Linen Collection",
    "category_slug": "summer-linen",
    "base_price": 5999.0,
    "discount_price": 4999.0,
    "effective_price": 4999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Certified European Flax Linen",
    "fit_type": "Wide-Leg Jumpsuit",
    "care_instructions": "Machine wash cold delicate",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.6,
    "review_count": 16,
    "sales_count": 109,
    "total_stock": 254,
    "in_stock": true,
    "primary_image": "/images/products/european-flax-sleeveless-linen-jumpsuit-oatmeal-natural.jpg",
    "created_at": "2026-11-06T17:42:14.569212",
    "images": [
      {
        "id": 63,
        "product_id": 32,
        "image_url": "/images/products/european-flax-sleeveless-linen-jumpsuit-oatmeal-natural.jpg",
        "color": "Oatmeal Natural",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Oatmeal Natural",
        "color_hex": "#D8CBB5",
        "image_url": "/images/products/european-flax-sleeveless-linen-jumpsuit-oatmeal-natural.jpg"
      },
      {
        "color": "Sage Olive",
        "color_hex": "#6B7C59",
        "image_url": "/images/products/european-flax-sleeveless-linen-jumpsuit-sage-olive.jpg"
      }
    ]
  },
  {
    "id": 33,
    "name": "Tuscan Calfskin Blake-Stitched Chelsea Boots",
    "slug": "footwear-33-43550",
    "description": "Artisan-crafted in Tuscany from vegetable-tanned Italian calfskin. Features flexible elastic side gussets, woven pull loops, and a resoleable Vibram rubber sole.",
    "category_id": 11,
    "category_name": "Footwear & Boots",
    "category_slug": "footwear",
    "base_price": 11499.0,
    "discount_price": 9499.0,
    "effective_price": 9499.0,
    "brand": "Aura Haute Collection",
    "material": "100% Full-Grain Tuscan Calfskin",
    "fit_type": "Standard D Width / True to Size",
    "care_instructions": "Condition with leather balm regularly",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.9,
    "review_count": 22,
    "sales_count": 91,
    "total_stock": 234,
    "in_stock": true,
    "primary_image": "/images/products/tuscan-calfskin-blake-stitched-chelsea-boots-cognac-tan-leather.jpg",
    "created_at": "2026-11-06T17:42:14.573032",
    "images": [
      {
        "id": 65,
        "product_id": 33,
        "image_url": "/images/products/tuscan-calfskin-blake-stitched-chelsea-boots-cognac-tan-leather.jpg",
        "color": "Cognac Tan Leather",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Cognac Tan Leather",
        "color_hex": "#9E5B32",
        "image_url": "/images/products/tuscan-calfskin-blake-stitched-chelsea-boots-cognac-tan-leather.jpg"
      },
      {
        "color": "Noir Black Leather",
        "color_hex": "#1A1A1A",
        "image_url": "/images/products/tuscan-calfskin-blake-stitched-chelsea-boots-noir-black-leather.jpg"
      }
    ]
  },
  {
    "id": 34,
    "name": "Minimalist Full-Grain Italian Nappa Sneakers",
    "slug": "footwear-34-3023a",
    "description": "Clean, understated court sneaker handmade from buttery Italian nappa leather with soft calfskin lining, waxed laces, and durable Margom cupsole.",
    "category_id": 11,
    "category_name": "Footwear & Boots",
    "category_slug": "footwear",
    "base_price": 7999.0,
    "discount_price": 6499.0,
    "effective_price": 6499.0,
    "brand": "Aura Haute Collection",
    "material": "100% Italian Nappa Leather",
    "fit_type": "True to Size",
    "care_instructions": "Wipe clean with a damp cloth",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.6,
    "review_count": 22,
    "sales_count": 41,
    "total_stock": 294,
    "in_stock": true,
    "primary_image": "/images/products/minimalist-full-grain-italian-nappa-sneakers-optic-white-nappa.jpg",
    "created_at": "2026-11-06T17:42:14.579195",
    "images": [
      {
        "id": 67,
        "product_id": 34,
        "image_url": "/images/products/minimalist-full-grain-italian-nappa-sneakers-optic-white-nappa.jpg",
        "color": "Optic White Nappa",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Optic White Nappa",
        "color_hex": "#F8F9FA",
        "image_url": "/images/products/minimalist-full-grain-italian-nappa-sneakers-optic-white-nappa.jpg"
      },
      {
        "color": "Noir Black Leather",
        "color_hex": "#1A1A1A",
        "image_url": "/images/products/minimalist-full-grain-italian-nappa-sneakers-noir-black-leather.jpg"
      }
    ]
  },
  {
    "id": 35,
    "name": "Tuscan Vacchetta Leather Heritage Weekend Tote",
    "slug": "accessories-35-fade0",
    "description": "Spacious travel tote crafted from full-grain vegetable-tanned vacchetta leather that develops rich patina. Rolled handles and heavy solid brass hardware.",
    "category_id": 12,
    "category_name": "Leather & Accessories",
    "category_slug": "accessories",
    "base_price": 9999.0,
    "discount_price": 8299.0,
    "effective_price": 8299.0,
    "brand": "Aura Haute Collection",
    "material": "100% Full-Grain Tuscan Vacchetta Leather",
    "fit_type": "42cm x 36cm x 16cm",
    "care_instructions": "Protect from standing water; condition periodically",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.7,
    "review_count": 16,
    "sales_count": 71,
    "total_stock": 274,
    "in_stock": true,
    "primary_image": "/images/products/tuscan-vacchetta-leather-heritage-weekend-tote-cognac-saddle-leather.jpg",
    "created_at": "2026-11-06T17:42:14.582230",
    "images": [
      {
        "id": 69,
        "product_id": 35,
        "image_url": "/images/products/tuscan-vacchetta-leather-heritage-weekend-tote-cognac-saddle-leather.jpg",
        "color": "Cognac Saddle Leather",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Cognac Saddle Leather",
        "color_hex": "#8B4513",
        "image_url": "/images/products/tuscan-vacchetta-leather-heritage-weekend-tote-cognac-saddle-leather.jpg"
      },
      {
        "color": "Noir Black Leather",
        "color_hex": "#1A1A1A",
        "image_url": "/images/products/tuscan-vacchetta-leather-heritage-weekend-tote-noir-black-leather.jpg"
      }
    ]
  },
  {
    "id": 36,
    "name": "Full-Grain Pebble Leather Executive Briefcase",
    "slug": "accessories-36-8eb7e",
    "description": "Refined slim briefcase constructed from scratch-resistant full-grain pebble leather. Features padded 15-inch laptop compartment and detachable shoulder strap.",
    "category_id": 12,
    "category_name": "Leather & Accessories",
    "category_slug": "accessories",
    "base_price": 10999.0,
    "discount_price": 8999.0,
    "effective_price": 8999.0,
    "brand": "Aura Haute Collection",
    "material": "100% Full-Grain Pebble Cowhide",
    "fit_type": "40cm x 30cm x 8cm",
    "care_instructions": "Wipe clean with microfiber cloth",
    "is_featured": true,
    "is_active": true,
    "average_rating": 4.8,
    "review_count": 10,
    "sales_count": 118,
    "total_stock": 290,
    "in_stock": true,
    "primary_image": "/images/products/full-grain-pebble-leather-executive-briefcase-noir-black-leather.jpg",
    "created_at": "2026-11-06T17:42:14.585748",
    "images": [
      {
        "id": 71,
        "product_id": 36,
        "image_url": "/images/products/full-grain-pebble-leather-executive-briefcase-noir-black-leather.jpg",
        "color": "Noir Black Leather",
        "is_primary": true,
        "display_order": 1
      }
    ],
    "available_sizes": [
      "M",
      "L",
      "XS",
      "XL",
      "S"
    ],
    "available_colors": [
      {
        "color": "Noir Black Leather",
        "color_hex": "#1A1A1A",
        "image_url": "/images/products/full-grain-pebble-leather-executive-briefcase-noir-black-leather.jpg"
      },
      {
        "color": "Cognac Saddle Leather",
        "color_hex": "#8B4513",
        "image_url": "/images/products/full-grain-pebble-leather-executive-briefcase-cognac-saddle-leather.jpg"
      }
    ]
  }
];

export const FALLBACK_FEATURED: Product[] = FALLBACK_PRODUCTS.filter(p => p.is_featured);

export const FALLBACK_TRENDING: Product[] = FALLBACK_PRODUCTS.slice(0, 8);
