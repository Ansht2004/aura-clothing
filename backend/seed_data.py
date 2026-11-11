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

def seed_database(target_app=None):
    app = target_app if target_app is not None else create_app('development')
    with app.app_context():
        print("Recreating database tables...")
        db.drop_all()
        db.create_all()

        record_counts = {}

        # -----------------------------------------------------------
        # 1. Categories (12 fashion categories)
        # -----------------------------------------------------------
        print("Seeding Categories...")
        categories_data = [
            {
                "name": "Women's Dresses",
                "slug": "womens-dresses",
                "description": "Effortless silhouettes from relaxed daywear to evening glamour.",
                "image_url": "/images/categories/womens-dresses.jpg",
                "is_featured": True
            },
            {
                "name": "Men's Shirts & Polos",
                "slug": "mens-shirts",
                "description": "Tailored poplins, breathable linen button-downs, and refined knit polos.",
                "image_url": "/images/categories/mens-shirts.jpg",
                "is_featured": True
            },
            {
                "name": "Tailored Blazers & Coats",
                "slug": "blazers-coats",
                "description": "Architectural tailoring and premium wool-blend outerwear for year-round sophistication.",
                "image_url": "/images/categories/blazers-coats.jpg",
                "is_featured": True
            },
            {
                "name": "Fine Knitwear & Sweaters",
                "slug": "knitwear-sweaters",
                "description": "Ultra-soft Mongolian cashmere, merino wool crews, and relaxed cardigans.",
                "image_url": "/images/categories/knitwear-sweaters.jpg",
                "is_featured": True
            },
            {
                "name": "Trousers & Chinos",
                "slug": "trousers-chinos",
                "description": "Pleated wide-leg trousers, tapered chinos, and smart casual bottoms.",
                "image_url": "/images/categories/trousers-chinos.jpg",
                "is_featured": False
            },
            {
                "name": "Denim & Jeans",
                "slug": "denim-jeans",
                "description": "Japanese selvedge denim, modern straight cuts, and vintage washes.",
                "image_url": "/images/categories/denim-jeans.jpg",
                "is_featured": True
            },
            {
                "name": "Premium Loungewear",
                "slug": "loungewear",
                "description": "Organic cotton hoodies, French terry joggers, and elevated relaxed staples.",
                "image_url": "/images/categories/loungewear.jpg",
                "is_featured": False
            },
            {
                "name": "Activewear & Performance",
                "slug": "activewear",
                "description": "Seamless moisture-wicking sets and technical performance apparel.",
                "image_url": "/images/categories/activewear.jpg",
                "is_featured": False
            },
            {
                "name": "Jackets & Outerwear",
                "slug": "jackets-outerwear",
                "description": "Water-resistant parkas, suede jackets, and insulated trench coats.",
                "image_url": "/images/categories/jackets-outerwear.jpg",
                "is_featured": True
            },
            {
                "name": "Summer Linen Collection",
                "slug": "summer-linen",
                "description": "Airy European flax linen garments crafted for warm coastal days.",
                "image_url": "/images/categories/summer-linen.jpg",
                "is_featured": True
            },
            {
                "name": "Footwear & Boots",
                "slug": "footwear",
                "description": "Handcrafted leather Chelsea boots, minimalist sneakers, and loafers.",
                "image_url": "/images/categories/footwear.jpg",
                "is_featured": False
            },
            {
                "name": "Leather & Accessories",
                "slug": "accessories",
                "description": "Full-grain leather belts, silk scarves, wool beanies, and tote bags.",
                "image_url": "/images/categories/accessories.jpg",
                "is_featured": False
            }
        ]

        categories = []
        for cat_info in categories_data:
            cat = Category(**cat_info)
            db.session.add(cat)
            categories.append(cat)
        db.session.flush()
        record_counts['categories'] = len(categories)

        # -----------------------------------------------------------
        # 2. Users (Admin, Demo Customer + 40 Fictional Customers)
        # -----------------------------------------------------------
        print("Seeding Users...")
        admin = User(
            email="tanwaransh46@gmail.com",
            full_name="Ansh Tanwar",
            phone="+91 98765 43210",
            role="admin"
        )
        admin.set_password("Tanwar@12")
        db.session.add(admin)

        demo_customer = User(
            email="alexander.vance@gmail.com",
            full_name="Alexander Vance",
            phone="+91 98450 14992",
            role="customer"
        )
        demo_customer.set_password("Customer@123456")
        db.session.add(demo_customer)

        users = [admin, demo_customer]
        used_emails = {admin.email.lower(), demo_customer.email.lower()}
        titles = {'mr', 'ms', 'mrs', 'dr', 'prof', 'miss', 'dds', 'md', 'phd', 'dvm', 'esq', 'jr', 'sr', 'ii', 'iii', 'iv'}
        domains = ['gmail.com', 'outlook.com', 'icloud.com', 'yahoo.com']

        for i in range(40):
            raw_name = fake.name()
            words = [w for w in re.sub(r'[^a-zA-Z\s]', '', raw_name).split() if w.lower() not in titles]
            clean_name = ' '.join(words) if words else raw_name
            first = words[0].lower() if len(words) >= 1 else 'patron'
            last = words[-1].lower() if len(words) >= 2 else 'aura'
            domain = domains[i % len(domains)]
            email_candidate = f"{first}.{last}@{domain}"
            suffix = 2
            while email_candidate in used_emails:
                email_candidate = f"{first}.{last}{suffix}@{domain}"
                suffix += 1
            used_emails.add(email_candidate)

            cust = User(
                email=email_candidate,
                full_name=clean_name,
                phone=f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}",
                role="customer"
            )
            cust.set_password("Password@123")
            db.session.add(cust)
            users.append(cust)

        db.session.flush()
        record_counts['users'] = len(users)

        # -----------------------------------------------------------
        # 3. Customer Delivery Addresses (80+ addresses in India)
        # -----------------------------------------------------------
        print("Seeding Customer Addresses...")
        addresses = []
        demo_addr1 = Address(
            user_id=demo_customer.id,
            full_name=demo_customer.full_name,
            phone=demo_customer.phone,
            address_line1="B-402, Lodha Bellissimo, NM Joshi Marg",
            address_line2="Lower Parel",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400013",
            country="India",
            is_default=True
        )
        demo_addr2 = Address(
            user_id=demo_customer.id,
            full_name=demo_customer.full_name,
            phone=demo_customer.phone,
            address_line1="Villa 18, Palm Meadows",
            address_line2="Whitefield",
            city="Bengaluru",
            state="Karnataka",
            postal_code="560066",
            country="India",
            is_default=False
        )
        db.session.add_all([demo_addr1, demo_addr2])
        addresses.extend([demo_addr1, demo_addr2])

        indian_cities = [
            ("Mumbai", "Maharashtra", "400001"),
            ("Bengaluru", "Karnataka", "560001"),
            ("New Delhi", "Delhi", "110001"),
            ("Jaipur", "Rajasthan", "302001"),
            ("Hyderabad", "Telangana", "500001"),
            ("Pune", "Maharashtra", "411001"),
            ("Chennai", "Tamil Nadu", "600001"),
            ("Kolkata", "West Bengal", "700001"),
            ("Ahmedabad", "Gujarat", "380001"),
            ("Chandigarh", "Punjab", "160001")
        ]

        for u in users[2:]:
            addr_count = random.choice([1, 2, 3])
            for k in range(addr_count):
                city, state, pin_base = random.choice(indian_cities)
                addr = Address(
                    user_id=u.id,
                    full_name=u.full_name,
                    phone=u.phone or f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}",
                    address_line1=fake.street_address(),
                    address_line2=f"Apartment {random.randint(101, 804)}" if random.random() < 0.4 else "",
                    city=city,
                    state=state,
                    postal_code=str(int(pin_base) + random.randint(1, 90)),
                    country="India",
                    is_default=(k == 0)
                )
                db.session.add(addr)
                addresses.append(addr)

        db.session.flush()
        record_counts['addresses'] = len(addresses)

        # -----------------------------------------------------------
        # 4. Products Catalogue (100% Real, Local, Accurate Color Photos)
        # -----------------------------------------------------------
        print("Seeding Products, Images, and Variants...")
        cat_map = {c.slug: c.id for c in categories}

        curated_catalog = [
            # 1. JACKETS & OUTERWEAR (Accurate photo-to-color mapping!)
            {
                "name": "Spanish Goat Suede Harrington Bomber Jacket",
                "category": "jackets-outerwear",
                "description": "Crafted from velvety Spanish goat suede with a butter-soft hand feel. Finished with ribbed wool cuffs and hem, an antique brass two-way front zipper, and lustrous breathable cupro lining.",
                "material": "100% Spanish Goat Suede Leather",
                "fit_type": "Classic Bomber Fit",
                "care_instructions": "Specialist leather clean only",
                "base_price": 13999.0,
                "discount_price": 11999.0,
                "is_featured": True,
                "colors": [
                    ("Caramel Suede", "#C19A6B", "/images/products/spanish-goat-suede-harrington-bomber-jacket-caramel-suede.jpg"),
                    ("Noir Black Leather", "#1A1A1A", "/images/products/spanish-goat-suede-harrington-bomber-jacket-noir-black-leather.jpg")
                ]
            },
            {
                "name": "Spanish Merino Shearling Aviator Flight Jacket",
                "category": "jackets-outerwear",
                "description": "Handcrafted from dense Spanish merino shearling with a thick fleece collar, adjustable buckled throat latch, and heavy-duty antiqued brass hardware.",
                "material": "100% Genuine Merino Shearling & Leather",
                "fit_type": "Heritage Aviator Regular Fit",
                "care_instructions": "Specialist leather clean only",
                "base_price": 18999.0,
                "discount_price": 15999.0,
                "is_featured": True,
                "colors": [
                    ("Cognac Tan Shearling", "#9E5B32", "/images/products/spanish-merino-shearling-aviator-flight-jacket-cognac-tan-shearling.jpg"),
                    ("Noir Black Moto", "#1A1A1A", "/images/products/spanish-merino-shearling-aviator-flight-jacket-noir-black-moto.jpg")
                ]
            },
            {
                "name": "StormShield 750-Fill Down Expedition Parka",
                "category": "jackets-outerwear",
                "description": "Waterproof technical shell packed with 750 fill power RDS down. Designed with an insulated storm hood, fleece-lined hand pockets, and internal storm cuffs.",
                "material": "Waterproof Shell & 90/10 RDS Goose Down",
                "fit_type": "Expedition Fit",
                "care_instructions": "Machine wash cold gentle with down wash",
                "base_price": 14499.0,
                "discount_price": 12299.0,
                "is_featured": False,
                "colors": [
                    ("Forest Olive Green", "#3B4A3F", "/images/products/stormshield-750-fill-down-expedition-parka-forest-olive-green.jpg"),
                    ("Matte Black Parka", "#1A1A1A", "/images/products/stormshield-750-fill-down-expedition-parka-matte-black-parka.jpg")
                ]
            },
            {
                "name": "Cafe Racer Full-Grain Leather Moto Jacket",
                "category": "jackets-outerwear",
                "description": "Iconic racer silhouette in full-grain cowhide leather with a mandarin snap collar, zippered cuffs, quilted shoulder detailing, and satin lining.",
                "material": "100% Full-Grain Cowhide Leather",
                "fit_type": "Tailored Moto Fit",
                "care_instructions": "Condition with leather balm; specialist clean",
                "base_price": 15999.0,
                "discount_price": 13499.0,
                "is_featured": True,
                "colors": [
                    ("Noir Black", "#1A1A1A", "/images/products/cafe-racer-full-grain-leather-moto-jacket-noir-black.jpg"),
                    ("Caramel Suede", "#C19A6B", "/images/products/cafe-racer-full-grain-leather-moto-jacket-caramel-suede.jpg")
                ]
            },

            # 2. WOMEN'S DRESSES
            {
                "name": "Mulberry Silk Bias-Cut Slip Dress",
                "category": "womens-dresses",
                "description": "Tailored from heavyweight 22-momme Mulberry silk that drapes gracefully along natural contours with a cowl neckline and adjustable straps.",
                "material": "100% Grade 6A Mulberry Silk",
                "fit_type": "Bias Cut / Fluid",
                "care_instructions": "Specialist dry clean",
                "base_price": 7499.0,
                "discount_price": 6299.0,
                "is_featured": True,
                "colors": [
                    ("Champagne Ivory", "#F3EDE2", "/images/products/mulberry-silk-bias-cut-slip-dress-champagne-ivory.jpg"),
                    ("Emerald Green", "#0E4D3E", "/images/products/mulberry-silk-bias-cut-slip-dress-emerald-green.jpg")
                ]
            },
            {
                "name": "Duchess Cotton Velvet Gala Evening Gown",
                "category": "womens-dresses",
                "description": "Dramatic floor-length gown crafted from plush Italian cotton velvet featuring a sculpted off-shoulder neckline and subtle side split.",
                "material": "98% Cotton Velvet, 2% Elastane",
                "fit_type": "Fitted Bodice / A-Line Skirt",
                "care_instructions": "Dry clean only",
                "base_price": 9999.0,
                "discount_price": 8499.0,
                "is_featured": True,
                "colors": [
                    ("Burgundy Wine", "#6B1D2F", "/images/products/duchess-cotton-velvet-gala-evening-gown-burgundy-wine.jpg"),
                    ("Midnight Noir", "#141416", "/images/products/duchess-cotton-velvet-gala-evening-gown-midnight-noir.jpg")
                ]
            },
            {
                "name": "French Flax Belted Linen Shirtdress",
                "category": "womens-dresses",
                "description": "Spun from pre-washed Normandy flax linen that softens beautifully with wear. Features natural mother-of-pearl buttons and a self-tie sash.",
                "material": "100% European Flax Linen",
                "fit_type": "Relaxed Fit",
                "care_instructions": "Machine wash cold delicate",
                "base_price": 5499.0,
                "discount_price": 4699.0,
                "is_featured": False,
                "colors": [
                    ("Sage Olive", "#6B7C59", "/images/products/french-flax-belted-linen-shirtdress-sage-olive.jpg"),
                    ("Oatmeal Natural", "#DCCBB5", "/images/products/french-flax-belted-linen-shirtdress-oatmeal-natural.jpg")
                ]
            },
            {
                "name": "Botanical Silk Chiffon Tiered Maxi Dress",
                "category": "womens-dresses",
                "description": "Ethereal floral silk chiffon dress with cascading micro-pleats, smocked elasticated waist, and delicate bishop sleeves.",
                "material": "100% Silk Chiffon with Rayon Lining",
                "fit_type": "Flowing Tiered Fit",
                "care_instructions": "Hand wash cold or dry clean",
                "base_price": 8299.0,
                "discount_price": 6999.0,
                "is_featured": True,
                "colors": [
                    ("Blush Rose Floral", "#E29D9D", "/images/products/botanical-silk-chiffon-tiered-maxi-dress-blush-rose-floral.jpg"),
                    ("Scarlet Blossom", "#A52A2A", "/images/products/botanical-silk-chiffon-tiered-maxi-dress-scarlet-blossom.jpg")
                ]
            },

            # 3. MEN'S SHIRTS & POLOS
            {
                "name": "Albini Two-Ply Royal Oxford Shirt",
                "category": "mens-shirts",
                "description": "Woven from superfine two-ply Egyptian cotton from renowned Italian mill Albini. Features a structured semi-spread collar and mother-of-pearl buttons.",
                "material": "100% Egyptian Giza Cotton",
                "fit_type": "Tailored Slim Fit",
                "care_instructions": "Machine wash warm, iron medium",
                "base_price": 4499.0,
                "discount_price": 3799.0,
                "is_featured": True,
                "colors": [
                    ("Sky Blue Oxford", "#87CEEB", "/images/products/albini-two-ply-royal-oxford-shirt-sky-blue-oxford.jpg"),
                    ("Crisp White Poplin", "#F8F9FA", "/images/products/albini-two-ply-royal-oxford-shirt-crisp-white-poplin.jpg")
                ]
            },
            {
                "name": "Riviera Camp-Collar Normandy Linen Shirt",
                "category": "mens-shirts",
                "description": "Casual relaxed camp-collar shirt cut from pre-washed French flax linen with an airy basket weave and straight split hem.",
                "material": "100% French Flax Linen",
                "fit_type": "Relaxed Fit",
                "care_instructions": "Machine wash cold gentle, line dry",
                "base_price": 3999.0,
                "discount_price": 3299.0,
                "is_featured": True,
                "colors": [
                    ("Terracotta Rust", "#C85A32", "/images/products/riviera-camp-collar-normandy-linen-shirt-terracotta-rust.jpg"),
                    ("Sage Olive Linen", "#667C59", "/images/products/riviera-camp-collar-normandy-linen-shirt-sage-olive-linen.jpg")
                ]
            },
            {
                "name": "Silk-Cotton Fine Gauge Knit Polo",
                "category": "mens-shirts",
                "description": "Elevated polo shirt spun with 70% long-staple cotton and 30% silk for a luxurious hand feel, seamless collar, and ribbed hems.",
                "material": "70% Long-Staple Cotton, 30% Silk",
                "fit_type": "Modern Tailored",
                "care_instructions": "Hand wash cold, dry flat",
                "base_price": 4299.0,
                "discount_price": None,
                "is_featured": False,
                "colors": [
                    ("Navy Melange", "#1B2A4A", "/images/products/silk-cotton-fine-gauge-knit-polo-navy-melange.jpg"),
                    ("Crisp White", "#F8F9FA", "/images/products/silk-cotton-fine-gauge-knit-polo-crisp-white.jpg")
                ]
            },
            {
                "name": "Heavyweight Japanese Cotton Twill Overshirt",
                "category": "mens-shirts",
                "description": "Substantial 340 GSM Japanese twill overshirt engineered with dual chest flap pockets and reinforced felled seams for versatile over-layering.",
                "material": "100% Japanese Cotton Twill",
                "fit_type": "Relaxed Overshirt Fit",
                "care_instructions": "Machine wash cold, inside out",
                "base_price": 5299.0,
                "discount_price": 4499.0,
                "is_featured": False,
                "colors": [
                    ("Midnight Navy", "#1A2332", "/images/products/heavyweight-japanese-cotton-twill-overshirt-midnight-navy.jpg"),
                    ("Terracotta Clay", "#C85A32", "/images/products/heavyweight-japanese-cotton-twill-overshirt-terracotta-clay.jpg")
                ]
            },

            # 4. TAILORED BLAZERS & COATS
            {
                "name": "Biella Virgin Wool Double-Breasted Blazer",
                "category": "blazers-coats",
                "description": "Tailored from luxurious virgin wool twill from Biella, Italy. Features peak lapels, half-canvas construction, horn buttons, and double back vents.",
                "material": "100% Italian Virgin Wool",
                "fit_type": "Structured Tailored",
                "care_instructions": "Specialist dry clean",
                "base_price": 12999.0,
                "discount_price": 10999.0,
                "is_featured": True,
                "colors": [
                    ("Camel Tan Flannel", "#C19A6B", "/images/products/biella-virgin-wool-double-breasted-blazer-camel-tan-flannel.jpg"),
                    ("Midnight Navy Twill", "#1A2639", "/images/products/biella-virgin-wool-double-breasted-blazer-midnight-navy-twill.jpg")
                ]
            },
            {
                "name": "Double-Faced Cashmere & Wool Trench Overcoat",
                "category": "blazers-coats",
                "description": "Exceptional thermal warmth woven with 85% Australian merino wool and 15% Mongolian cashmere. Hand-finished double-face craftsmanship with unlined interior.",
                "material": "85% Merino Wool, 15% Cashmere",
                "fit_type": "Relaxed Overcoat Fit",
                "care_instructions": "Specialist dry clean",
                "base_price": 16999.0,
                "discount_price": 14499.0,
                "is_featured": True,
                "colors": [
                    ("Charcoal Black Melange", "#212121", "/images/products/double-faced-cashmere-wool-trench-overcoat-charcoal-black-melange.jpg"),
                    ("Camel Gabardine", "#C49E73", "/images/products/double-faced-cashmere-wool-trench-overcoat-camel-gabardine.jpg")
                ]
            },
            {
                "name": "Unstructured Belgian Linen Sport Coat",
                "category": "blazers-coats",
                "description": "Breezy tailored sport coat crafted with unlined shoulders and patch pockets from breathable Belgian flax linen.",
                "material": "100% Belgian Linen",
                "fit_type": "Soft Tailoring",
                "care_instructions": "Dry clean only",
                "base_price": 9499.0,
                "discount_price": 7999.0,
                "is_featured": False,
                "colors": [
                    ("Midnight Navy", "#1A2639", "/images/products/unstructured-belgian-linen-sport-coat-midnight-navy.jpg"),
                    ("Camel Tan", "#C19A6B", "/images/products/unstructured-belgian-linen-sport-coat-camel-tan.jpg")
                ]
            },
            {
                "name": "Weatherproof Cotton Gabardine Belted Trench",
                "category": "blazers-coats",
                "description": "Timeless military trench coat cut from tightly woven water-repellent cotton gabardine. Features storm flap, buckled waist belt, and horn buttons.",
                "material": "100% Weatherproof Cotton Gabardine",
                "fit_type": "Classic Trench Cut",
                "care_instructions": "Dry clean only",
                "base_price": 14999.0,
                "discount_price": None,
                "is_featured": True,
                "colors": [
                    ("Honey Camel Trench", "#C49E73", "/images/products/weatherproof-cotton-gabardine-belted-trench-honey-camel-trench.jpg"),
                    ("Charcoal Slate", "#212121", "/images/products/weatherproof-cotton-gabardine-belted-trench-charcoal-slate.jpg")
                ]
            },

            # 5. FINE KNITWEAR & SWEATERS
            {
                "name": "Grade-A Mongolian Cashmere Crewneck",
                "category": "knitwear-sweaters",
                "description": "Supreme softness spun from 2-ply 100% Grade-A inner Mongolian cashmere. Features ribbed collar, cuffs, and hem for timeless warmth.",
                "material": "100% Grade-A Mongolian Cashmere",
                "fit_type": "Classic Fit",
                "care_instructions": "Hand wash cold, dry flat",
                "base_price": 8999.0,
                "discount_price": 7499.0,
                "is_featured": True,
                "colors": [
                    ("Cream Oatmeal", "#E8DFD1", "/images/products/grade-a-mongolian-cashmere-crewneck-cream-oatmeal.jpg"),
                    ("Charcoal Heather", "#343A40", "/images/products/grade-a-mongolian-cashmere-crewneck-charcoal-heather.jpg")
                ]
            },
            {
                "name": "Heavyweight Cable-Knit Merino Cardigan",
                "category": "knitwear-sweaters",
                "description": "Chunky Aran cable knit woven from 100% Australian extra-fine merino wool with hand-stitched leather buttons and front patch pockets.",
                "material": "100% Extra-Fine Merino Wool",
                "fit_type": "Relaxed Fit",
                "care_instructions": "Dry clean or gentle hand wash",
                "base_price": 7299.0,
                "discount_price": 5999.0,
                "is_featured": True,
                "colors": [
                    ("Winter Ecru White", "#F4F0E8", "/images/products/heavyweight-cable-knit-merino-cardigan-winter-ecru-white.jpg"),
                    ("Cognac Ribbed", "#8B4513", "/images/products/heavyweight-cable-knit-merino-cardigan-cognac-ribbed.jpg")
                ]
            },
            {
                "name": "Fine Gauge Merino Wool Turtleneck",
                "category": "knitwear-sweaters",
                "description": "Spun from 19.5-micron fine Australian merino wool in a silky rib knit. Designed to layer smoothly beneath tailored blazers and trench coats.",
                "material": "100% Fine Merino Wool",
                "fit_type": "Slim Tailored",
                "care_instructions": "Machine wash cold on wool cycle",
                "base_price": 6299.0,
                "discount_price": None,
                "is_featured": False,
                "colors": [
                    ("Camel Heather", "#C19A6B", "/images/products/fine-gauge-merino-wool-turtleneck-camel-heather.jpg"),
                    ("Noir Black", "#1A1A1A", "/images/products/fine-gauge-merino-wool-turtleneck-noir-black.jpg")
                ]
            },
            {
                "name": "Brushed Alpaca Wool Relaxed Crew",
                "category": "knitwear-sweaters",
                "description": "Fluffy, cloud-like texture knitted from a blend of Peruvian baby alpaca and wool. Warm, breathable, and finished with a comfortable ribbed collar.",
                "material": "60% Baby Alpaca, 28% Wool, 12% Polyamide",
                "fit_type": "Boxy Relaxed Fit",
                "care_instructions": "Hand wash cold, reshape and dry flat",
                "base_price": 7899.0,
                "discount_price": 6499.0,
                "is_featured": False,
                "colors": [
                    ("Charcoal Heather Melange", "#343A40", "/images/products/brushed-alpaca-wool-relaxed-crew-charcoal-heather-melange.jpg"),
                    ("Winter Ecru White", "#F4F0E8", "/images/products/brushed-alpaca-wool-relaxed-crew-winter-ecru-white.jpg")
                ]
            },

            # 6. TROUSERS & CHINOS
            {
                "name": "Biella Tropical Wool Pleated Trousers",
                "category": "trousers-chinos",
                "description": "Tailored with single front pleats, side adjusters, and a clean taper. Woven from breathable tropical wool for a sharp fluid drape in all seasons.",
                "material": "100% Tropical Wool",
                "fit_type": "Tapered Pleated",
                "care_instructions": "Specialist dry clean",
                "base_price": 6499.0,
                "discount_price": 5299.0,
                "is_featured": True,
                "colors": [
                    ("Charcoal Slate Melange", "#343A40", "/images/products/biella-tropical-wool-pleated-trousers-charcoal-slate-melange.jpg"),
                    ("Natural Oatmeal Linen", "#D8D2C2", "/images/products/biella-tropical-wool-pleated-trousers-natural-oatmeal-linen.jpg")
                ]
            },
            {
                "name": "Pima Stretch Cotton Tailored Chinos",
                "category": "trousers-chinos",
                "description": "Cut from premium 98% long-staple pima cotton twill and 2% elastane for slight give. Features horn buttons and taped interior seams.",
                "material": "98% Pima Cotton, 2% Elastane",
                "fit_type": "Slim Tapered",
                "care_instructions": "Machine wash cold",
                "base_price": 4299.0,
                "discount_price": 3599.0,
                "is_featured": False,
                "colors": [
                    ("Classic Khaki Tan", "#C19A6B", "/images/products/pima-stretch-cotton-tailored-chinos-classic-khaki-tan.jpg"),
                    ("Charcoal Grey", "#343A40", "/images/products/pima-stretch-cotton-tailored-chinos-charcoal-grey.jpg")
                ]
            },
            {
                "name": "Belgian Flax Linen Wide-Leg Trousers",
                "category": "trousers-chinos",
                "description": "High-waisted, fluid silhouette tailored with deep front pleats from heavyweight 280 GSM Belgian flax linen. Effortlessly relaxed and cool.",
                "material": "100% Belgian Flax Linen",
                "fit_type": "Wide Leg Relaxed",
                "care_instructions": "Machine wash delicate, hang dry",
                "base_price": 5499.0,
                "discount_price": None,
                "is_featured": False,
                "colors": [
                    ("Ecru Natural Linen", "#E8E2D5", "/images/products/belgian-flax-linen-wide-leg-trousers-ecru-natural-linen.jpg"),
                    ("Charcoal Slate", "#343A40", "/images/products/belgian-flax-linen-wide-leg-trousers-charcoal-slate.jpg")
                ]
            },

            # 7. DENIM & JEANS
            {
                "name": "Okayama 14oz Vintage Straight Jeans",
                "category": "denim-jeans",
                "description": "Crafted in Kojima, Japan from 14oz shuttle-loomed selvedge denim. Detailed with red-line selvedge ID, custom copper hardware, and genuine button fly.",
                "material": "100% Long-Staple Japanese Cotton",
                "fit_type": "Classic Straight Leg",
                "care_instructions": "Wash sparingly inside out in cold water",
                "base_price": 6999.0,
                "discount_price": 5899.0,
                "is_featured": True,
                "colors": [
                    ("Vintage Light Indigo", "#5B84B1", "/images/products/okayama-14oz-vintage-straight-jeans-vintage-light-indigo.jpg"),
                    ("Dark Selvedge Indigo", "#1B2A4A", "/images/products/okayama-14oz-vintage-straight-jeans-dark-selvedge-indigo.jpg")
                ]
            },
            {
                "name": "Kuroki Raw Indigo Slim-Taper Jeans",
                "category": "denim-jeans",
                "description": "Tailored from 13.5oz rope-dyed Kuroki Mills raw denim. Starts crisp and molds to your body, developing personalized honeycombs and whiskers.",
                "material": "99% Japanese Selvedge Cotton, 1% Comfort Stretch",
                "fit_type": "Slim Tapered",
                "care_instructions": "Cold soak, line dry",
                "base_price": 6499.0,
                "discount_price": 5499.0,
                "is_featured": True,
                "colors": [
                    ("Raw Dark Indigo", "#1B2A4A", "/images/products/kuroki-raw-indigo-slim-taper-jeans-raw-dark-indigo.jpg"),
                    ("Washed Charcoal Black", "#2F3136", "/images/products/kuroki-raw-indigo-slim-taper-jeans-washed-charcoal-black.jpg")
                ]
            },
            {
                "name": "Relaxed 90s Heritage Stonewash Jeans",
                "category": "denim-jeans",
                "description": "Authentic loose silhouette inspired by iconic 90s casualwear. Cut from 100% regenerative ring-spun cotton denim with vintage stonewashing.",
                "material": "100% Regenerative Cotton Denim",
                "fit_type": "Relaxed 90s Straight",
                "care_instructions": "Machine wash cold",
                "base_price": 5299.0,
                "discount_price": None,
                "is_featured": False,
                "colors": [
                    ("Stonewash Sky Blue", "#7DA0CA", "/images/products/relaxed-90s-heritage-stonewash-jeans-stonewash-sky-blue.jpg"),
                    ("Vintage Light Indigo", "#5B84B1", "/images/products/relaxed-90s-heritage-stonewash-jeans-vintage-light-indigo.jpg")
                ]
            },

            # 8. PREMIUM LOUNGEWEAR
            {
                "name": "Heavyweight 450 GSM Organic Cotton Hoodie",
                "category": "loungewear",
                "description": "Crafted from ultra-dense 450 GSM organic French terry cotton. Features double-layered hood, flatlock stitching, and ribbed side mobility gussets.",
                "material": "100% Combed Organic Cotton",
                "fit_type": "Relaxed Boxy Fit",
                "care_instructions": "Machine wash warm, tumble dry low",
                "base_price": 4299.0,
                "discount_price": 3499.0,
                "is_featured": True,
                "colors": [
                    ("Heather Grey Melange", "#9E9E9E", "/images/products/heavyweight-450-gsm-organic-cotton-hoodie-heather-grey-melange.jpg"),
                    ("Oatmeal Natural", "#E5DEC9", "/images/products/heavyweight-450-gsm-organic-cotton-hoodie-oatmeal-natural.jpg")
                ]
            },
            {
                "name": "Organic Loopback French Terry Sweatpants",
                "category": "loungewear",
                "description": "Plush loopback organic cotton joggers with a drawstring elastic waist, tailored slanted welt pockets, and comfortable ribbed cuffs.",
                "material": "100% Organic French Terry Cotton",
                "fit_type": "Relaxed Tapered Fit",
                "care_instructions": "Machine wash cold with like colors",
                "base_price": 3699.0,
                "discount_price": 2999.0,
                "is_featured": False,
                "colors": [
                    ("Oatmeal Natural", "#E5DEC9", "/images/products/organic-loopback-french-terry-sweatpants-oatmeal-natural.jpg"),
                    ("Heather Grey Melange", "#9E9E9E", "/images/products/organic-loopback-french-terry-sweatpants-heather-grey-melange.jpg")
                ]
            },

            # 9. ACTIVEWEAR & PERFORMANCE
            {
                "name": "Seamless Ribbed Compression Workout Set",
                "category": "activewear",
                "description": "High-performance moisture-wicking four-way stretch fabric with targeted muscle support, zero-chafe flat seams, and breathable ventilation zones.",
                "material": "78% Recycled Polyamide, 22% Elastane",
                "fit_type": "Athletic Compression Fit",
                "care_instructions": "Machine wash cold, line dry",
                "base_price": 4499.0,
                "discount_price": 3699.0,
                "is_featured": True,
                "colors": [
                    ("Dusty Rose Pink", "#D8A47F", "/images/products/seamless-ribbed-compression-workout-set-dusty-rose-pink.jpg"),
                    ("Olive Green", "#556B2F", "/images/products/seamless-ribbed-compression-workout-set-olive-green.jpg")
                ]
            },
            {
                "name": "AeroShield Ultralight Performance Windbreaker",
                "category": "activewear",
                "description": "Featherweight technical ripstop running jacket with DWR water-repellent coating, underarm ventilation eyelets, and packable pocket.",
                "material": "100% Recycled Ripstop Nylon",
                "fit_type": "Athletic Slim Fit",
                "care_instructions": "Machine wash cold gentle",
                "base_price": 4999.0,
                "discount_price": 3999.0,
                "is_featured": False,
                "colors": [
                    ("Olive Sage", "#556B2F", "/images/products/aeroshield-ultralight-performance-windbreaker-olive-sage.jpg"),
                    ("Midnight Stealth Black", "#1A1A1A", "/images/products/aeroshield-ultralight-performance-windbreaker-midnight-stealth-black.jpg")
                ]
            },

            # 10. SUMMER LINEN COLLECTION
            {
                "name": "Pre-Washed Normandy Linen Drawstring Trousers",
                "category": "summer-linen",
                "description": "Airy, relaxed-leg trousers with an elasticated drawstring waist and breathable open weave. Garment-washed for a soft touch and effortless drape.",
                "material": "100% European Flax Linen",
                "fit_type": "Relaxed Straight Fit",
                "care_instructions": "Machine wash cold gentle, line dry",
                "base_price": 4499.0,
                "discount_price": 3799.0,
                "is_featured": True,
                "colors": [
                    ("Natural Oatmeal Linen", "#E5DEC9", "/images/products/pre-washed-normandy-linen-drawstring-trousers-natural-oatmeal-linen.jpg"),
                    ("Belgian Ecru Linen", "#D8D2C2", "/images/products/pre-washed-normandy-linen-drawstring-trousers-belgian-ecru-linen.jpg")
                ]
            },
            {
                "name": "European Flax Sleeveless Linen Jumpsuit",
                "category": "summer-linen",
                "description": "Wide-leg minimalist jumpsuit cut from 100% French flax linen. Features a flattering square neckline, removable belt, and concealed back zip.",
                "material": "100% Certified European Flax Linen",
                "fit_type": "Wide-Leg Jumpsuit",
                "care_instructions": "Machine wash cold delicate",
                "base_price": 5999.0,
                "discount_price": 4999.0,
                "is_featured": True,
                "colors": [
                    ("Oatmeal Natural", "#D8CBB5", "/images/products/european-flax-sleeveless-linen-jumpsuit-oatmeal-natural.jpg"),
                    ("Sage Olive", "#6B7C59", "/images/products/european-flax-sleeveless-linen-jumpsuit-sage-olive.jpg")
                ]
            },

            # 11. FOOTWEAR & BOOTS
            {
                "name": "Tuscan Calfskin Blake-Stitched Chelsea Boots",
                "category": "footwear",
                "description": "Artisan-crafted in Tuscany from vegetable-tanned Italian calfskin. Features flexible elastic side gussets, woven pull loops, and a resoleable Vibram rubber sole.",
                "material": "100% Full-Grain Tuscan Calfskin",
                "fit_type": "Standard D Width / True to Size",
                "care_instructions": "Condition with leather balm regularly",
                "base_price": 11499.0,
                "discount_price": 9499.0,
                "is_featured": True,
                "colors": [
                    ("Cognac Tan Leather", "#9E5B32", "/images/products/tuscan-calfskin-blake-stitched-chelsea-boots-cognac-tan-leather.jpg"),
                    ("Noir Black Leather", "#1A1A1A", "/images/products/tuscan-calfskin-blake-stitched-chelsea-boots-noir-black-leather.jpg")
                ]
            },
            {
                "name": "Minimalist Full-Grain Italian Nappa Sneakers",
                "category": "footwear",
                "description": "Clean, understated court sneaker handmade from buttery Italian nappa leather with soft calfskin lining, waxed laces, and durable Margom cupsole.",
                "material": "100% Italian Nappa Leather",
                "fit_type": "True to Size",
                "care_instructions": "Wipe clean with a damp cloth",
                "base_price": 7999.0,
                "discount_price": 6499.0,
                "is_featured": True,
                "colors": [
                    ("Optic White Nappa", "#F8F9FA", "/images/products/minimalist-full-grain-italian-nappa-sneakers-optic-white-nappa.jpg"),
                    ("Noir Black Leather", "#1A1A1A", "/images/products/minimalist-full-grain-italian-nappa-sneakers-noir-black-leather.jpg")
                ]
            },

            # 12. LEATHER & ACCESSORIES
            {
                "name": "Tuscan Vacchetta Leather Heritage Weekend Tote",
                "category": "accessories",
                "description": "Spacious travel tote crafted from full-grain vegetable-tanned vacchetta leather that develops rich patina. Rolled handles and heavy solid brass hardware.",
                "material": "100% Full-Grain Tuscan Vacchetta Leather",
                "fit_type": "42cm x 36cm x 16cm",
                "care_instructions": "Protect from standing water; condition periodically",
                "base_price": 9999.0,
                "discount_price": 8299.0,
                "is_featured": True,
                "colors": [
                    ("Cognac Saddle Leather", "#8B4513", "/images/products/tuscan-vacchetta-leather-heritage-weekend-tote-cognac-saddle-leather.jpg"),
                    ("Noir Black Leather", "#1A1A1A", "/images/products/tuscan-vacchetta-leather-heritage-weekend-tote-noir-black-leather.jpg")
                ]
            },
            {
                "name": "Full-Grain Pebble Leather Executive Briefcase",
                "category": "accessories",
                "description": "Refined slim briefcase constructed from scratch-resistant full-grain pebble leather. Features padded 15-inch laptop compartment and detachable shoulder strap.",
                "material": "100% Full-Grain Pebble Cowhide",
                "fit_type": "40cm x 30cm x 8cm",
                "care_instructions": "Wipe clean with microfiber cloth",
                "base_price": 10999.0,
                "discount_price": 8999.0,
                "is_featured": True,
                "colors": [
                    ("Noir Black Leather", "#1A1A1A", "/images/products/full-grain-pebble-leather-executive-briefcase-noir-black-leather.jpg"),
                    ("Cognac Saddle Leather", "#8B4513", "/images/products/full-grain-pebble-leather-executive-briefcase-cognac-saddle-leather.jpg")
                ]
            }
        ]

        all_products = []
        product_images_list = []
        product_variants_list = []
        sizes = ['XS', 'S', 'M', 'L', 'XL']

        for idx, item in enumerate(curated_catalog, start=1):
            cat_slug = item["category"]
            cat_id = cat_map.get(cat_slug, 1)
            p_slug = f"{cat_slug}-{idx:02d}-{uuid.uuid4().hex[:5]}"

            prod = Product(
                name=item["name"],
                slug=p_slug,
                description=item["description"],
                category_id=cat_id,
                base_price=item["base_price"],
                discount_price=item["discount_price"],
                brand="Aura Haute Collection",
                material=item["material"],
                fit_type=item["fit_type"],
                care_instructions=item["care_instructions"],
                is_featured=item["is_featured"],
                is_active=True,
                average_rating=round(random.uniform(4.4, 4.9), 1),
                review_count=random.randint(6, 28),
                sales_count=random.randint(25, 140)
            )
            db.session.add(prod)
            db.session.flush()
            all_products.append(prod)

            # Add Color-Matched Images (Exact 1-to-1 matching)
            for img_idx, (color_name, color_hex, img_url) in enumerate(item["colors"], start=1):
                p_img = ProductImage(
                    product_id=prod.id,
                    image_url=img_url,
                    color=color_name,
                    is_primary=(img_idx == 1),
                    display_order=img_idx
                )
                db.session.add(p_img)
                product_images_list.append(p_img)

            # Add Variants for each color across standard sizes
            for color_name, color_hex, img_url in item["colors"]:
                for sz in sizes:
                    stock_qty = random.randint(12, 40)
                    sku = f"AUR-{prod.id:03d}-{sz}-{color_name[:3].upper()}"
                    variant = ProductVariant(
                        product_id=prod.id,
                        size=sz,
                        color=color_name,
                        color_hex=color_hex,
                        sku=sku,
                        stock_quantity=stock_qty,
                        additional_price=0.0
                    )
                    db.session.add(variant)
                    product_variants_list.append(variant)

        db.session.flush()
        record_counts['products'] = len(all_products)
        record_counts['product_images'] = len(product_images_list)
        record_counts['product_variants'] = len(product_variants_list)

        # -----------------------------------------------------------
        # 5. Coupons (12 Promotional Coupons in Rupees)
        # -----------------------------------------------------------
        print("Seeding Promotional Coupons...")
        coupons_data = [
            ("WELCOME15", "percentage", 15.0, 1999.0, 1500.0, 1000, True),
            ("ELEGANCE20", "percentage", 20.0, 3999.0, 2500.0, 500, True),
            ("FESTIVE500", "fixed", 500.0, 2999.0, 500.0, 300, True),
            ("SUMMER25", "percentage", 25.0, 4999.0, 3000.0, 300, True),
            ("FLAT300", "fixed", 300.0, 1999.0, 300.0, 200, True),
            ("VIP1000", "fixed", 1000.0, 5999.0, 1000.0, 100, True),
            ("SEASON10", "percentage", 10.0, 0.0, 1000.0, 2000, True),
            ("FREESHIP", "fixed", 149.0, 1499.0, 149.0, 500, True),
            ("AURA10", "percentage", 10.0, 999.0, 800.0, 1500, True),
            ("FALL20", "percentage", 20.0, 2499.0, 1500.0, 400, True),
            ("EXPIRED99", "percentage", 99.0, 0.0, 500.0, 10, False),
            ("CYBER35", "percentage", 35.0, 3999.0, 2500.0, 250, True)
        ]
        coupons = []
        for code, dtype, dval, min_amt, max_amt, ulimit, is_act in coupons_data:
            c = Coupon(
                code=code,
                discount_type=dtype,
                discount_value=dval,
                min_order_amount=min_amt,
                max_discount_amount=max_amt,
                usage_limit=ulimit,
                times_used=random.randint(5, 45) if is_act else 0,
                valid_from=datetime.now(timezone.utc) - timedelta(days=30),
                valid_to=datetime.now(timezone.utc) + timedelta(days=180),
                is_active=is_act
            )
            db.session.add(c)
            coupons.append(c)

        db.session.flush()
        record_counts['coupons'] = len(coupons)

        # -----------------------------------------------------------
        # 6. Customer Reviews (250+ Verified Reviews)
        # -----------------------------------------------------------
        print("Seeding Customer Reviews...")
        review_titles = [
            "Exceptional craftsmanship and feel", "Exceeded my expectations!", "Superb drape and fit",
            "Luxurious material, worth every rupee", "My new wardrobe staple", "Pure perfection",
            "Incredible quality fabric", "Beautiful silhouette", "Softest garment I own", "Received so many compliments"
        ]
        review_comments = [
            "The fit is true to size and the fabric feels substantial yet exceptionally breathable. The color matches the online photos perfectly.",
            "Wore this to a dinner gala and felt incredible. The subtle sheen and tailor-level finishing are remarkable.",
            "Aura Apparel really nails the minimalist luxury aesthetic. Seamless stitching and arrived impeccably packaged.",
            "Top tier quality! Washes well and retains its softness, color, and shape completely.",
            "Couldn't be happier with this purchase. The color match in person is identical to the photos.",
            "Such an elegant piece! Feels like true bespoke tailoring at a fair price point."
        ]

        reviews = []
        for prod in all_products:
            num_reviews = random.randint(4, 7)
            for _ in range(num_reviews):
                reviewer = random.choice(users[1:])
                rev = Review(
                    product_id=prod.id,
                    user_id=reviewer.id,
                    rating=random.choices([4, 5, 5], weights=[0.25, 0.45, 0.30])[0],
                    title=random.choice(review_titles),
                    comment=random.choice(review_comments),
                    is_verified_purchase=True,
                    created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 120))
                )
                db.session.add(rev)
                reviews.append(rev)

        db.session.flush()
        record_counts['reviews'] = len(reviews)

        # -----------------------------------------------------------
        # 7. Customer Orders, Order Items & Payments (100+ Orders in INR)
        # -----------------------------------------------------------
        print("Seeding Orders, Order Items, and Payments...")
        orders = []
        order_items = []
        payments = []
        return_requests = []

        statuses = ['delivered', 'shipped', 'processing', 'pending', 'cancelled']
        status_weights = [0.55, 0.20, 0.12, 0.08, 0.05]
        payment_methods = ['card', 'upi', 'netbanking', 'cod']

        for i in range(100):
            customer = demo_customer if i < 10 else random.choice(users[1:])
            cust_addresses = [a for a in addresses if a.user_id == customer.id]
            addr = cust_addresses[0] if cust_addresses else addresses[0]

            order_status = random.choices(statuses, weights=status_weights)[0]
            pay_method = random.choice(payment_methods)
            is_cancelled = (order_status == 'cancelled')
            is_delivered = (order_status == 'delivered')

            chosen_variants = random.sample(product_variants_list, random.randint(1, 3))
            subtotal = 0.0
            temp_items = []

            for v in chosen_variants:
                p = v.product
                u_price = p.discount_price if (p.discount_price and p.discount_price > 0) else p.base_price
                u_price += v.additional_price
                qty = random.randint(1, 2)
                t_price = round(u_price * qty, 2)
                subtotal += t_price
                temp_items.append((p, v, u_price, qty, t_price))

            subtotal = round(subtotal, 2)
            discount = round(subtotal * 0.15, 2) if random.random() < 0.35 else 0.0
            tax = round(max(0.0, subtotal - discount) * 0.12, 2)
            shipping = 0.0 if subtotal >= 2499.0 else 149.0
            final_total = round(max(0.0, subtotal - discount) + tax + shipping, 2)

            order_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))
            order_num = f"AUR-{order_date.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

            order = Order(
                order_number=order_num,
                user_id=customer.id,
                address_id=addr.id,
                coupon_code="WELCOME15" if discount > 0 else None,
                subtotal=subtotal,
                discount_amount=discount,
                shipping_amount=shipping,
                tax_amount=tax,
                total_amount=final_total,
                status=order_status,
                payment_status='refunded' if is_cancelled else ('paid' if pay_method != 'cod' or is_delivered else 'pending'),
                payment_method=pay_method,
                tracking_number=f"TRK-{uuid.uuid4().hex[:10].upper()}",
                carrier_name="Blue Dart Express",
                created_at=order_date
            )
            db.session.add(order)
            db.session.flush()
            orders.append(order)

            # Order items
            for p, v, u_price, qty, t_price in temp_items:
                oi = OrderItem(
                    order_id=order.id,
                    product_id=p.id,
                    variant_id=v.id,
                    product_name=p.name,
                    variant_size=v.size,
                    variant_color=v.color,
                    sku=v.sku,
                    image_url=p.primary_image,
                    unit_price=u_price,
                    quantity=qty,
                    total_price=t_price
                )
                db.session.add(oi)
                order_items.append(oi)

            # Payment record
            payment = Payment(
                order_id=order.id,
                user_id=customer.id,
                payment_method=pay_method,
                transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
                amount=final_total,
                status='refunded' if is_cancelled else ('completed' if pay_method != 'cod' or is_delivered else 'pending'),
                payment_details=f"Processed via {pay_method.upper()}",
                created_at=order_date
            )
            db.session.add(payment)
            payments.append(payment)

            # Returns or cancellations
            if is_cancelled:
                rr = ReturnRequest(
                    order_id=order.id,
                    user_id=customer.id,
                    request_type="cancellation",
                    reason="Customer changed preference before dispatch.",
                    status="approved",
                    admin_notes="Cancellation approved and full refund initiated to original payment source.",
                    created_at=order_date
                )
                db.session.add(rr)
                return_requests.append(rr)
            elif is_delivered and random.random() < 0.12:
                req_type = random.choice(["return", "exchange"])
                rr = ReturnRequest(
                    order_id=order.id,
                    user_id=customer.id,
                    request_type=req_type,
                    reason="Size exchange requested for one size larger.",
                    status=random.choice(["pending", "approved"]),
                    admin_notes="Reverse pickup scheduled with Blue Dart.",
                    created_at=order_date + timedelta(days=2)
                )
                db.session.add(rr)
                return_requests.append(rr)

        db.session.flush()
        record_counts['orders'] = len(orders)
        record_counts['order_items'] = len(order_items)
        record_counts['payments'] = len(payments)
        record_counts['return_requests'] = len(return_requests)

        # -----------------------------------------------------------
        # 8. Notifications (120+ in-app notifications)
        # -----------------------------------------------------------
        print("Seeding In-App Notifications...")
        notifications = []
        for u in users[1:]:
            n1 = Notification(
                user_id=u.id,
                title="Welcome to Aura Apparel",
                message="Discover timeless clothing pieces. Use coupon WELCOME15 for 15% off your first order.",
                type="promo",
                is_read=True,
                created_at=datetime.now(timezone.utc) - timedelta(days=15)
            )
            n2 = Notification(
                user_id=u.id,
                title="New Collection Alert: Summer Linen & Suede Outerwear",
                message="Our European Flax linen collection and Spanish goat suede jackets are now live. Explore effortless luxury today.",
                type="promo",
                is_read=random.choice([True, False]),
                created_at=datetime.now(timezone.utc) - timedelta(days=2)
            )
            db.session.add_all([n1, n2])
            notifications.extend([n1, n2])

        db.session.flush()
        record_counts['notifications'] = len(notifications)

        # Commit everything to database
        db.session.commit()

        total_records = sum(record_counts.values())
        print("\n" + "=" * 50)
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        for entity, count in record_counts.items():
            print(f"  - {entity.replace('_', ' ').capitalize()}: {count} records")
        print("-" * 50)
        print(f"TOTAL FICTIONAL TEST RECORDS: {total_records}")
        print("=" * 50)

if __name__ == '__main__':
    seed_database()
