#!/usr/bin/env python3
# Sample Content Images Creator
import os
import json
from PIL import Image, ImageDraw, ImageFont

def create_sample_images_for_content():
    """Create sample images for our generated content"""
    
    # Create images directory
    images_dir = "content_images"
    os.makedirs(images_dir, exist_ok=True)
    
    print("🎨 Creating sample images for content...")
    
    # Product-specific visuals
    product_visuals = {
        "organic_anti-aging_night_cream": {
            "color": (75, 50, 100),  # Deep purple
            "description": "Anti-Aging Night Cream\nLuxury Skincare\nRetinol + Hyaluronic Acid"
        },
        "vitamin_c_brightening_serum": {
            "color": (255, 165, 0),  # Orange
            "description": "Vitamin C Serum\nBrightening Formula\nNatural Antioxidants"
        },
        "hydrating_day_moisturizer": {
            "color": (100, 149, 237),  # Cornflower blue
            "description": "Day Moisturizer\nSPF 30 Protection\nBotanical Extracts"
        },
        "gentle_cleansing_face_wash": {
            "color": (144, 238, 144),  # Light green
            "description": "Gentle Face Wash\nOrganic Honey & Oats\nSensitive Skin Formula"
        },
        "rejuvenating_eye_cream": {
            "color": (221, 160, 221),  # Plum
            "description": "Eye Cream\nPeptides + Caffeine\nAnti-Aging Formula"
        },
        "weekly_exfoliating_mask": {
            "color": (205, 133, 63),  # Peru
            "description": "Exfoliating Mask\nNatural AHA + Clay\nDeep Treatment"
        }
    }
    
    # Create images for each product
    for product_key, visual_info in product_visuals.items():
        # Create main product image
        img = Image.new('RGB', (1080, 1080), color=visual_info['color'])
        draw = ImageDraw.Draw(img)
        
        # Try to load a decent font
        try:
            font_large = ImageFont.truetype("arial.ttf", 60)
            font_medium = ImageFont.truetype("arial.ttf", 40)
            font_small = ImageFont.truetype("arial.ttf", 30)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add Ethereal Glow branding
        brand_text = "ETHEREAL GLOW"
        bbox = draw.textbbox((0, 0), brand_text, font=font_large)
        brand_width = bbox[2] - bbox[0]
        draw.text(((1080 - brand_width) // 2, 100), brand_text, 
                 fill=(255, 255, 255), font=font_large)
        
        # Add product description
        lines = visual_info['description'].split('\n')
        y_position = 300
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_medium)
            line_width = bbox[2] - bbox[0]
            draw.text(((1080 - line_width) // 2, y_position), line, 
                     fill=(255, 255, 255), font=font_medium)
            y_position += 80
        
        # Add website
        website_text = "TheRealGlow.in"
        bbox = draw.textbbox((0, 0), website_text, font=font_small)
        website_width = bbox[2] - bbox[0]
        draw.text(((1080 - website_width) // 2, 900), website_text, 
                 fill=(255, 255, 255), font=font_small)
        
        # Save main product image
        main_filename = f"{product_key}_main.png"
        img.save(os.path.join(images_dir, main_filename))
        
        # Create Instagram square version
        square_img = img.copy()
        square_filename = f"{product_key}_instagram.png"
        square_img.save(os.path.join(images_dir, square_filename))
        
        # Create TikTok vertical version (1080x1920)
        vertical_img = Image.new('RGB', (1080, 1920), color=visual_info['color'])
        v_draw = ImageDraw.Draw(vertical_img)
        
        # Add brand at top
        bbox = v_draw.textbbox((0, 0), brand_text, font=font_large)
        brand_width = bbox[2] - bbox[0]
        v_draw.text(((1080 - brand_width) // 2, 200), brand_text, 
                   fill=(255, 255, 255), font=font_large)
        
        # Add product info in center
        y_pos = 600
        for line in lines:
            bbox = v_draw.textbbox((0, 0), line, font=font_medium)
            line_width = bbox[2] - bbox[0]
            v_draw.text(((1080 - line_width) // 2, y_pos), line, 
                       fill=(255, 255, 255), font=font_medium)
            y_pos += 80
        
        # Add website at bottom
        bbox = v_draw.textbbox((0, 0), website_text, font=font_small)
        website_width = bbox[2] - bbox[0]
        v_draw.text(((1080 - website_width) // 2, 1600), website_text, 
                   fill=(255, 255, 255), font=font_small)
        
        vertical_filename = f"{product_key}_tiktok.png"
        vertical_img.save(os.path.join(images_dir, vertical_filename))
        
        print(f"✅ Created images for {product_key}")
    
    # Create a master brand image
    brand_img = Image.new('RGB', (1920, 1080), color=(30, 20, 40))
    b_draw = ImageDraw.Draw(brand_img)
    
    try:
        brand_font = ImageFont.truetype("arial.ttf", 120)
        tagline_font = ImageFont.truetype("arial.ttf", 60)
    except:
        brand_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
    
    # Brand name
    brand_text = "ETHEREAL GLOW"
    bbox = b_draw.textbbox((0, 0), brand_text, font=brand_font)
    brand_width = bbox[2] - bbox[0]
    b_draw.text(((1920 - brand_width) // 2, 400), brand_text, 
               fill=(255, 215, 0), font=brand_font)
    
    # Tagline
    tagline = "Where Science Meets Nature"
    bbox = b_draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = bbox[2] - bbox[0]
    b_draw.text(((1920 - tagline_width) // 2, 600), tagline, 
               fill=(255, 255, 255), font=tagline_font)
    
    brand_img.save(os.path.join(images_dir, "ethereal_glow_brand.png"))
    
    print(f"\n✅ Sample images created in: {os.path.abspath(images_dir)}")
    print(f"📊 Total images: {len(os.listdir(images_dir))}")
    
    return images_dir

if __name__ == "__main__":
    create_sample_images_for_content()
