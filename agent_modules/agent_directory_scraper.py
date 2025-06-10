import requests
import re
from bs4 import BeautifulSoup
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_directory_page(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.text

def extract_designer_blocks(html: str):
    soup = BeautifulSoup(html, "html.parser")
    listing_blocks = soup.find_all("li", class_=re.compile("hz-pro-search-result"))
    return [str(block) for block in listing_blocks]

def clean_json_block(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()
    return text

def gpt_extract_contact_info(block_html: str, model: str = "gpt-4o-mini") -> dict:
    prompt = (
        "You are an intelligent agent that extracts structured contact information from a Houzz HTML block.\n"
        "Return a JSON with keys: company, mobile, email, website, instagram.\n"
        "Use null for missing fields.\n\n"
        f"HTML Block:\n{block_html[:6000]}\n"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You extract contact info from Houzz blocks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500,
        )
        content = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] GPT extraction failed: {e}")
        return {}

    cleaned = clean_json_block(content)

    try:
        return json.loads(cleaned)
    except Exception:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        return json.loads(match.group(0)) if match else {}

def scrape_directory_page(url):  # ✅ this function must exist!
    html = fetch_directory_page(url)
    blocks = extract_designer_blocks(html)
    if not blocks:
        print("⚠️ No listing blocks found.")
        return []

    results = []
    for i, block in enumerate(blocks):
        print(f"[INFO] Parsing listing {i+1}/{len(blocks)}")
        data = gpt_extract_contact_info(block)
        if data:
            results.append(data)
    return results
