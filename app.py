import streamlit as st
import google.generativeai as genai
import json
from PIL import Image

# 1. API Key Configuration
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]  
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Aestheticly", layout="wide", initial_sidebar_state="expanded")
st.title("✨ Aesthetic.ly — Get Products That Match Your Aesthetic")

# 2. The Comprehensive Mock Inventory Catalog
MOCK_CATALOG = [

{
    "item_id": "M01",
    "category": "Mugs",
    "title": "Coffee Cat Ceramic Mug 350ml",
    "style_tags": ["cat", "cute", "aesthetic", "animal"],
    "image_url": "https://m.media-amazon.com/images/I/71tI-R1fFHL._SX425_.jpg",
    "buy_link": "https://amzn.in/d/08Af1OPk"
},

{
    "item_id": "M02",
    "category": "Mugs",
    "title": "Cute Cat Ceramic Coffee Mug with Lid & Spoon",
    "style_tags": ["cat", "kawaii", "cute", "japanese"],
    "image_url": "https://m.media-amazon.com/images/I/51zanHhW9pL._SX425_.jpg",
    "buy_link": "https://amzn.in/d/04sSX2KY"
},

{
    "item_id": "M03",
    "category": "Mugs",
    "title": "Spring Dog Coffee Mug with Lid & Spoon",
    "style_tags": ["dog", "cute", "animal", "cartoon"],
    "image_url": "https://m.media-amazon.com/images/I/51bq4xg9EZL._SX425_.jpg",
    "buy_link": "https://amzn.in/d/08gX57QL"
},

{
    "item_id": "M04",
    "category": "Mugs",
    "title": "Dog and Girls Cartoon Printed Coffee Mug",
    "style_tags": ["dog", "cartoon", "cute", "fun"],
    "image_url": "https://m.media-amazon.com/images/I/51AKQcPUi1L._SX425_.jpg",
    "buy_link": "https://amzn.in/d/0ewuI4al"
},

{
    "item_id": "M05",
    "category": "Mugs",
    "title": "Pink Bow Premium Ceramic Mug",
    "style_tags": ["pink", "girly", "cute", "aesthetic"],
    "image_url": "https://m.media-amazon.com/images/I/6102XC3+XsL._SY679_.jpg",
    "buy_link": "https://amzn.in/d/00DxuEc3"
},

{
    "item_id": "M06",
    "category": "Mugs",
    "title": "Peach Pink Heart Design Ceramic Mug",
    "style_tags": ["pink", "girly", "heart", "aesthetic"],
    "image_url": "https://m.media-amazon.com/images/I/61yXNgz12rL._SX425_.jpg",
    "buy_link": "https://amzn.in/d/06NemN3E"
},

{
    "item_id": "M07",
    "category": "Mugs",
    "title": "Vintage Skull Ceramic Mug",
    "style_tags": ["punk", "rock", "skull", "gothic"],
    "image_url": "https://m.media-amazon.com/images/I/71uMAd+yI5L._SX425_.jpg",
    "buy_link": "https://amzn.in/d/0bO5Bhkc"
},

{
    "item_id": "M08",
    "category": "Mugs",
    "title": "Gothic Skull Coffee Mug",
    "style_tags": ["punk", "gothic", "skull", "dark"],
    "image_url": "https://m.media-amazon.com/images/I/61zs0g1KKPL._SY679_.jpg",
    "buy_link": "https://amzn.in/d/07Sp89IH"
},

{
    "item_id": "M09",
    "category": "Mugs",
    "title": "Minimalist Black Ceramic Coffee Mug",
    "style_tags": ["plain", "minimalist", "office", "modern"],
    "image_url": "https://m.media-amazon.com/images/I/61d9MyA87zL._SX425_.jpg",
    "buy_link": "https://amzn.in/d/0gy0NnJC"
},

{
    "item_id": "M10",
    "category": "Mugs",
    "title": "Ecohome Matte Finish Coffee Mug Set",
    "style_tags": ["plain", "minimalist", "eco-friendly", "modern"],
    "image_url": "https://m.media-amazon.com/images/I/81nK-D8bdDL._SX425_.jpg",
    "buy_link": "https://amzn.in/d/0g3oCGCq"
},

{
    "item_id": "T01",
    "category": "T-Shirts",
    "title": "Black Crew Neck Plain T-Shirt",
    "style_tags": ["plain", "minimalist", "casual", "basic"],
    "image_url": "https://m.media-amazon.com/images/I/41AdjFqSCkL._SX522_.jpg",
    "buy_link": "https://amzn.in/d/0d3LrfUM"
},

{
    "item_id": "T02",
    "category": "T-Shirts",
    "title": "Solid Cotton Crew Neck Lounge T-Shirt",
    "style_tags": ["plain", "minimalist", "casual", "everyday"],
    "image_url": "https://m.media-amazon.com/images/I/7128Ix8OkaL._SY550_.jpg",
    "buy_link": "https://amzn.in/d/0fExkd9n"
},

{
    "item_id": "T03",
    "category": "T-Shirts",
    "title": "Los Angeles Racing Y2K Oversized T-Shirt",
    "style_tags": ["y2k", "streetwear", "graphic", "oversized","rock","pink"],
    "image_url": "https://m.media-amazon.com/images/I/71268+ZbJiL._SY550_.jpg",
    "buy_link": "https://amzn.in/d/06RM3pxV"
},

{
    "item_id": "T04",
    "category": "T-Shirts",
    "title": "Smile Graphic Cotton T-Shirt",
    "style_tags": ["cartoon", "cute", "graphic", "fun"],
    "image_url": "https://m.media-amazon.com/images/I/61Gs99zLCvL._SY550_.jpg",
    "buy_link": "https://amzn.in/d/00KxkdV8"
},

{
    "item_id": "T05",
    "category": "T-Shirts",
    "title": "Funny Cat and Coffee Graphic T-Shirt",
    "style_tags": ["cat", "coffee", "graphic", "cute"],
    "image_url": "https://m.media-amazon.com/images/I/61ibkEhdJyL._SX425_.jpg",
    "buy_link": "https://amzn.in/d/07GthOOa"
},

{
    "item_id": "T06",
    "category": "T-Shirts",
    "title": "Cartoon Cats Graphic T-Shirt",
    "style_tags": ["cat", "cartoon", "cute", "graphic"],
    "image_url": "https://m.media-amazon.com/images/I/710rMvsX50L._SX425_.jpg",
    "buy_link": "https://amzn.in/d/024s7zJ5"
},

{
    "item_id": "T07",
    "category": "T-Shirts",
    "title": "Satanic Pentagram Oversized Streetwear T-Shirt",
    "style_tags": ["punk", "rock", "gothic", "streetwear"],
    "image_url": "https://m.media-amazon.com/images/I/71O1I7Zv9wL._SX522_.jpg",
    "buy_link": "https://amzn.in/d/03kAaYIY"
},

{
    "item_id": "T08",
    "category": "T-Shirts",
    "title": "Blondie Rock Band Oversized T-Shirt",
    "style_tags": ["punk", "rock", "band", "music"],
    "image_url": "https://m.media-amazon.com/images/I/61YLC76rbWL._SX425_.jpg",
    "buy_link": "https://amzn.in/d/0eaW7zm2"
},

{
    "item_id": "T09",
    "category": "T-Shirts",
    "title": "Avengers Inspired Captain America Graphic T-Shirt",
    "style_tags": ["marvel", "avengers", "captain-america", "superhero"],
    "image_url": "https://m.media-amazon.com/images/I/61g+3qAko4L._SX425_.jpg",
    "buy_link": "https://amzn.in/d/02ZBRtaq"
},

{
    "item_id": "T10",
    "category": "T-Shirts",
    "title": "Marvel Graphic Oversized T-Shirt",
    "style_tags": ["marvel", "superhero", "graphic", "oversized"],
    "image_url": "https://m.media-amazon.com/images/I/61B1t3rABRL._SX425_.jpg",
    "buy_link": "https://amzn.in/d/01eCGD3I"
},

{
    "item_id": "T11",
    "category": "T-Shirts",
    "title": "One Piece Anime Oversized T-Shirt",
    "style_tags": ["anime", "one-piece", "manga", "graphic"],
    "image_url": "https://m.media-amazon.com/images/I/61W2tcIp0xL._SY550_.jpg",
    "buy_link": "https://amzn.in/d/0g8VHp4S"
}]

# 3. Sidebar Configuration Layout
with st.sidebar:
    st.header("1. Upload Your Aesthetic")
    uploaded_files = st.file_uploader(
        "Upload 1-5 inspiration images", type=["jpg", "jpeg", "png"], accept_multiple_files=True
    )
    
    st.header("2. Search Parameter")
    # Implemented clean dropdown switching
    selected_category = st.selectbox(
        "Select Product Category", 
        ["Mugs", "T-Shirts"]
    )
    
    submit_button = st.button("Get Product Recommendations", type="primary")

# 4. Filter and Dispatch Payload
if submit_button and uploaded_files:
    st.info(f"Finding {selected_category} that match your aesthetic...")
    
    filtered_catalog = [item for item in MOCK_CATALOG if item["category"] == selected_category]
    
    images = [Image.open(file) for file in uploaded_files]
    
    prompt = f"""
    You are an elite AI personal shopper and visual stylist. 
    1. Analyze the uploaded images to determine the overarching aesthetic vibe, color palette, design styles, and literal motifs. If it's pink make sure to match with pink things.
    2. Review this targeted collection of available {selected_category}:
    {json.dumps(filtered_catalog)}
    3. Select up to 3 items from this list that best match or incorporate the visual aesthetic/motifs found in the uploaded photos.
    
    You must respond ONLY with a valid JSON object matching this structure:
    {{
      "aesthetic_name": "Name of the style profile matching the images in simple, casual terms",
      "bg_tint_hex": "A very light, muted hex color matching this vibe",
      "selected_items": [
        {{
          "item_id": "The exact item_id string from the catalog list",
          "vibe_justification": "Explain concisely how this item's visual elements match the style rules of the uploaded images. Use exactly 100-120 characters.Use casual language."
        }}
      ]
    }}
    """
    
    try:
        model = genai.GenerativeModel('gemini-3.1-flash-lite')
        response = model.generate_content([prompt, *images])
        
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_text)
        
        st.success(f"Targeted Aesthetic Profile: **{data['aesthetic_name']}**")
        
        cols = st.columns(len(data['selected_items']))
        
        for idx, selection in enumerate(data['selected_items']):
            item_details = next((item for item in MOCK_CATALOG if item["item_id"] == selection["item_id"]), None)c