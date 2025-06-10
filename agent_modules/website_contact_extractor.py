import requests
import re
import os
import json
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def extract_emails_and_instagram_basic(html: str):
    soup = BeautifulSoup(html, "html.parser")
    visible_text = soup.get_text(separator=" ", strip=True)

    # 📨 Find raw emails
    raw_emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html)
    emails = list(set(
        e for e in raw_emails
        if not e.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".webp"))
        and len(e.split('@')[0]) > 2
    ))

    # 📸 Find Instagram links
    insta_links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if "instagram.com" in href:
            clean = href.split("?")[0].rstrip("/")
            if "login" not in clean and "share" not in clean:
                insta_links.add(clean)

    # Find @handles in visible text
    text_handles = re.findall(r"@([A-Za-z0-9_.]{3,})", visible_text)
    for handle in text_handles:
        if not handle.endswith(("com", "in", "net")):
            insta_links.add(f"@{handle}")

    return sorted(emails), sorted(insta_links)

def extract_with_gpt(html: str, model: str = "gpt-4o-mini") -> dict:
    prompt = (
        "You're an AI agent that extracts contact info from website HTML.\n"
        "Return only valid email addresses and Instagram handles or links.\n"
        "Avoid tracking or image-based emails.\n"
        "Output JSON: {\"emails\": [...], \"instagram\": [...]}.\n\n"
        f"HTML:\n{html[:6000]}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You extract contact info from HTML."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500,
        )
        content = response.choices[0].message.content.strip()

        # Clean markdown if any
        if content.startswith("```"):
            content = content.strip("`").strip()
            if content.lower().startswith("json"):
                content = content[4:].strip()

        return json.loads(content)

    except Exception as e:
        print(f"[WARN] GPT extraction failed: {e}")
        return {}

def extract_contacts_from_website(base_url: str):
    pages_to_try = [
        base_url.rstrip("/"),
        f"{base_url.rstrip('/')}/contact",
        f"{base_url.rstrip('/')}/contact-us",
        f"{base_url.rstrip('/')}/about",
        f"{base_url.rstrip('/')}/team"
    ]

    combined_html = ""

    for url in pages_to_try:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            combined_html += "\n\n" + response.text
        except Exception as e:
            print(f"[WARN] Could not fetch {url}: {e}")

    if not combined_html.strip():
        return {"emails": [], "instagram": []}

    # Try GPT first
    gpt_result = extract_with_gpt(combined_html)

    # Fallback to regex-based
    if not gpt_result.get("emails") and not gpt_result.get("instagram"):
        emails, instas = extract_emails_and_instagram_basic(combined_html)
        gpt_result["emails"] = emails
        gpt_result["instagram"] = instas

    # Filter & clean
    gpt_result["emails"] = [
        e for e in gpt_result.get("emails", [])
        if not e.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".svg"))
    ]
    gpt_result["instagram"] = [
        i for i in gpt_result.get("instagram", [])
        if i.startswith("http") or (i.startswith("@") and not i.endswith(("com", "in", "net")))
    ]

    return gpt_result

