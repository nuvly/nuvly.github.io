import requests
import datetime
import os
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

affiliate_link = "https://sephora.com?affid=yourid"  # Replace with real link later
post_content += f"<p>DOWNLOAD THIS LOOK: <a href='{affiliate_link}'>SHOP {topic} NOW</a></p><p>RELATED: <a href='best-skincare-products.html'>BEST SKINCARE TIPS—NUVLY STYLE</a></p>"

# Generate HTML post
date = datetime.datetime.now().strftime("%Y-%m-%d")
filename = f"{date}-{topic.replace(' ', '-')}.html"
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>{topic} REVIEW</title>
    <style>
        body {{ background-color: black; color: #FF69B4; font-family: monospace; }}
        h1 {{ color: #FFFFFF; }}
        a {{ color: #FFFFFF; text-decoration: none; }}
        img {{ border: 5px solid #FF69B4; }}
    </style>
</head>
<body>
    {post_content}
    <hr>
    <a href="index.html">BACK TO HOME</a>
</body>
</html>
""")

# Update index.html by appending to existing previews
try:
    with open("index.html", "r", encoding="utf-8") as f:
        current_index = f.read()
        soup = BeautifulSoup(current_index, "html.parser")
        previews_section = soup.find("h2", string="LATEST BEAUTY SCANS")
        if previews_section:
            # Insert new preview right after the h2
            new_preview = soup.new_tag("p")
            new_preview.string = f"<a href='{filename}'>{topic} REVIEW</a> - {post_content[50:100]}..."
            previews_section.insert_after(new_preview)
            previews_section.insert_after(soup.new_tag("hr", style="border: 1px dashed #FF69B4"))
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
    # Fallback if index.html doesn’t exist (unlikely)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>NUVLY</title>
    <style>
        body {{ background-color: black; color: #FF69B4; font-family: monospace; }}
        h1 {{ color: #FFFFFF; }}
        a {{ color: #FFFFFF; text-decoration: none; }}
        img {{ border: 5px solid #FF69B4; }}
        hr {{ border: 1px dashed #FF69B4; }}
    </style>
</head>
<body>
    <h1>NUVLY’S INTRO: BEAUTY REALNESS</h1>
    <p>Welcome to Nuvly, your digital beauty haven with a retro twist!</p>
    <h2>LATEST BEAUTY SCANS</h2>
    <p><a href='{filename}'>{topic} REVIEW</a> - {post_content[50:100]}...</p>
    <hr>
    <img src="images/nuvly-robot.jpg" alt="Nuvly Robot">
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