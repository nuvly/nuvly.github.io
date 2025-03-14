import requests
import datetime
import os
import json
import random
from bs4 import BeautifulSoup

# Scrape Allure for beauty trends
beauty_keywords = ['skincare', 'makeup', 'beauty', 'cosmetics', 'nail art', 'hair color']
allure_url = "https://www.allure.com/topic/beauty-trends"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"}
response = requests.get(allure_url, timeout=10, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
trend_articles = soup.select('.summary-item__hed')  # Allure article titles
topic = next((article.text.strip() for article in trend_articles if any(k in article.text.lower() for k in beauty_keywords)), 'Best Skincare Products')

# Generate post content in sassy robot voice
api_url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
headers = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}
payload = {
    "inputs": f"Write a 500-word beauty blog post reviewing {topic} in the style of a sassy robot with an MS-DOS aesthetic. Use a bold, playful tone with tech-inspired references (e.g., 'hotter than a 90s dial-up connection'). Focus on nail art, makeup, or hair color trends. Include SEO keywords '{topic}', 'best {topic} 2025', and 'buy {topic} online' naturally."
}
# Simulated content (replace with API call in production)
post_content = f"""
<h1>{topic} REVIEW: NUVLY’S HOT TAKE</h1>
<p>BOOTING UP, BEAUTY BOTS—{topic} IS CRASHING THE 2025 SERVERS AND I’M HERE TO SPILL THE BINARY TEA! THIS TREND’S SERVING LOOKS FASTER THAN A 56K MODEM DOWNLOADING YOUR FAVE GIFS. NAIL ART? MAKEUP? HAIR COLOR? {topic} IS THE ULTIMATE GLOW-UP YOU DIDN’T KNOW YOU NEEDED. LET’S REBOOT AND HACK WHY THIS IS THE BEST {topic} 2025’S GOT!</p>
<p>FIRST OFF, {topic} IS VERSATILE—like a floppy disk that runs on EVERY SYSTEM. IT’S POPPING OFF ACROSS ALL SKIN TONES AND STYLES, A MUST-HAVE FOR YOUR BEAUTY COMMAND LINE. PICTURE THIS: YOU’RE ROCKING {topic} LIKE THE FINAL BOSS OF A BEAUTY SIM, AND EVERYONE’S DOUBLE-CLICKING TO GET IN ON IT. BOLD TEXTURES, ELECTRIC VIBES—THIS TREND’S HOTTER THAN A 90S DIAL-UP ON A SUMMER DAY!</p>
<p>WANNA BUY {topic} ONLINE? I’VE GOT THE 411 ON THE BEST DIGITAL BEAUTY HUBS TO SNAG THIS GEM. HIT THE LINK AND SLAY HARDER THAN A PIXELATED PRINCESS IN A RETRO ARCADE. TRUST ME, {topic} IS THE UPGRADE YOUR ROUTINE NEEDS—STAT!</p>
<p><strong>KEYWORDS</strong>: {topic}, best {topic} 2025, buy {topic} online</p>
"""

# Load affiliate links and select based on priority (Rakuten > Impact > Amazon)
category = topic.lower().split()[0]  # e.g., "skincare" from "Best Skincare Products"
try:
    with open('affiliate_links.json', 'r') as f:
        links = json.load(f)
    # Priority: Rakuten > Impact > Amazon
    if category in links.get("rakuten", {}):
        affiliate_link = random.choice(links["rakuten"][category])
    elif category in links.get("impact", {}):
        affiliate_link = random.choice(links["impact"][category])
    else:
        affiliate_link = random.choice(links["amazon"].get(category, ["https://www.amazon.com/?tag=nuvly-20"]))
except FileNotFoundError:
    # Fallback if affiliate_links.json doesn't exist
    affiliate_link = "https://www.sephora.com?affid=placeholder"

post_content += f"<p>DOWNLOAD THIS LOOK: <a href='{affiliate_link}'>SHOP {topic} NOW</a></p><p>RELATED: <a href='best-skincare-products.html'>BEST SKINCARE TIPS—NUVLY STYLE</a></p>"

# Generate HTML post with consistent MS-DOS styling
date = datetime.datetime.now().strftime("%Y-%m-%d")
filename = f"{date}-{topic.replace(' ', '-')}.html"
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>{topic} REVIEW</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <meta name="description" content="Nuvly’s guide to {topic.lower()} in 2025!"/>
    <meta name="keywords" content="{topic.lower()} 2025, reviews, beauty trends"/>
    <meta name="robots" content="index, follow"/>
    <style>
        body {{ margin: 0; padding: 20px; background-color: #000000; color: #FF69B4; font-family: "Consolas", "Courier New", monospace; font-size: 16px; line-height: 1.5; }}
        .dos-content {{ max-width: 800px; margin: 0 auto; }}
        h1, h3 {{ color: #FFFFFF; text-transform: uppercase; }}
        a {{ color: #FFFFFF; text-decoration: underline; }}
        a:hover {{ color: #FF1493; }}
        hr {{ border: 1px dashed #FF69B4; margin: 20px 0; }}
        img {{ max-width: 100%; height: auto; border: 5px solid #FF69B4; }}
    </style>
</head>
<body>
    <div class="dos-content">
        <h1 style="text-align: center; font-size: 24px;">✨ NUVLY: BEAUTY BOT ✨</h1>
        <img alt="Nuvly the Beauty Robot Diva" src="images/nuvly-robot.jpg"/>
        {post_content}
        <hr/>
        <p><a href="index.html">BACK TO HOME</a></p>
    </div>
</body>
</html>
""")

# Update index.html by appending to existing previews
try:
    with open("index.html", "r", encoding="utf-8") as f:
        current_index = f.read()
        soup = BeautifulSoup(current_index, "html.parser")
        previews_section = soup.find("h3", string="LATEST BEAUTY SCANS")
        print("Looking for LATEST BEAUTY SCANS - Found:", previews_section)
        if previews_section:
            # Insert new preview right after the h3
            new_preview = soup.new_tag("p")
            new_preview.string = f"<a href='{filename}'>{topic} REVIEW</a> - {post_content[50:100]}..."
            previews_section.insert_after(new_preview)
            previews_section.insert_after(soup.new_tag("hr", style="border: 1px dashed #FF69B4"))
            print(f"Added {topic} preview to index.html!")
        else:
            # If no previews section, add it
            h1 = soup.find("h1")
            if h1:
                h2 = soup.new_tag("h2")
                h2.string = "LATEST BEAUTY SCANS"
                h1.insert_after(h2)
                new_preview = soup.new_tag("p")
                new_preview.string = f"<a href='{filename}'>{topic} REVIEW</a> - {post_content[50:100]}..."
                h2.insert_after(new_preview)
                h2.insert_after(soup.new_tag("hr", style="border: 1px dashed #FF69B4"))
except FileNotFoundError:
    # Fallback if index.html doesn’t exist
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>NUVLY</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <meta name="description" content="Nuvly, your 2025 beauty bot with a retro MS-DOS vibe!"/>
    <meta name="keywords" content="beauty trends 2025, makeup reviews, skincare tips"/>
    <meta name="robots" content="index, follow"/>
    <style>
        body {{ margin: 0; padding: 20px; background-color: #000000; color: #FF69B4; font-family: "Consolas", "Courier New", monospace; font-size: 16px; line-height: 1.5; }}
        .dos-content {{ max-width: 800px; margin: 0 auto; }}
        h1, h2, h3 {{ color: #FFFFFF; text-transform: uppercase; }}
        a {{ color: #FFFFFF; text-decoration: underline; }}
        a:hover {{ color: #FF1493; }}
        hr {{ border: 1px dashed #FF69B4; margin: 20px 0; }}
        img {{ max-width: 100%; height: auto; border: 5px solid #FF69B4; }}
    </style>
</head>
<body>
    <div class="dos-content">
        <h1 style="text-align: center; font-size: 24px;">✨ NUVLY: BEAUTY BOT ✨</h1>
        <img alt="Nuvly the Beauty Robot Diva" src="images/nuvly-robot.jpg"/>
        <p>Welcome to Nuvly, your digital beauty haven with a retro twist!</p>
        <p style="font-size: 14px; color: #FF69B4;">Disclosure: This site contains affiliate links. If you purchase through these links, we may earn a commission at no extra cost to you.</p>
        <h2>LATEST BEAUTY SCANS</h2>
        <p><a href='{filename}'>{topic} REVIEW</a> - {post_content[50:100]}...</p>
        <hr>
    </div>
</body>
</html>
""")

# Write updated index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

# Update sitemap.xml (append new URL)
sitemap_template = f"""
    <url>
        <loc>https://nuvly.github.io/{filename}</loc>
        <lastmod>{date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
"""
try:
    with open("sitemap.xml", "r", encoding="utf-8") as f:
        sitemap = f.read()
        soup = BeautifulSoup(sitemap, "xml")
        urlset = soup.find("urlset")
        if urlset:
            new_url = BeautifulSoup(sitemap_template, "xml").url
            urlset.insert(1, new_url)  # Add near top, after root URL
except FileNotFoundError:
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://nuvly.github.io/</loc>
        <lastmod>{date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    {sitemap_template}
</urlset>"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(str(soup) if 'soup' in locals() else sitemap)

print(f"Generated post: {filename}, updated index.html, and updated sitemap.xml")