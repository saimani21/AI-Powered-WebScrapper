# Developed this for a client.
# 🏗️ Houzz Smart Scraper Dashboard

A powerful AI-assisted scraping tool that collects verified contact information of interior designers, architects, and other professionals listed on [Houzz](https://www.houzz.com/). Built with Python, Streamlit, GPT-4o, and BeautifulSoup, this tool allows you to scrape data city-wise or category-wise with intelligent enrichment.

---
![image](https://github.com/user-attachments/assets/b4761f83-ad21-4c9e-96fa-86f1a62d6c33)

## 🚀 Features

- **Web UI with Streamlit**: Intuitive dashboard for filter selection and scraping control
- **AI + Regex Extraction**: Extracts emails and Instagram handles from designer websites using GPT and fallbacks
- **Multi-page Navigation**: Scrape any number of listing pages dynamically
- **Smart Subpage Crawling**: Visits subpages like `/contact`, `/about`, `/team`, etc.
- **Data Deduplication**: Prevents duplicate entries across runs
- **Real-time Logs**: Visual feedback on each profile being processed
- **Export Options**: Save each scrape batch and full merged file to Excel

---

## 📁 Project Structure

```bash
houzz_ai_scraper/
├── dashboard_v2.py                # Streamlit dashboard (main interface)
├── filter_config.py               # Category & city code mappings + URL builder
├── agent_modules/
│   ├── agent_directory_scraper.py   # Extract listings from Houzz page
│   └── website_contact_extractor.py # Visit and parse external websites
├── houzz_final_results.xlsx       # Combined deduplicated result file
├── .env                           # Contains your OpenAI API Key
├── requirements.txt               # Python dependencies
└── README.md
```

---

## 🔧 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/houzz-ai-scraper.git
cd houzz-ai-scraper
```

### 2. Create & activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API Key
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_key_here
```

### 5. Run the app
```bash
streamlit run dashboard_v2.py
```

Open the provided local URL (usually `http://localhost:8501`) in your browser.

---



---

## 🧠 How It Works
1. **Select filters**: Choose a category (e.g., Interior Designers) and a city (e.g., Bengaluru), or leave city as "No Filter"
2. **Click Start Scraping**: It navigates Houzz listings, fetches data per listing
3. **Smart Enrichment**: For each website found, visits relevant subpages and extracts contact details using GPT-4o and regex
4. **Saves**: Saves batch output and appends to master Excel

---

## 💡 Use Cases
- Lead generation for interior designers and service professionals
- Marketing and outreach campaigns
- Building a verified contact database

---

## 📌 To-Do / Future Improvements
- Add multi-threaded scraping for speed
- Include support for more platforms (e.g., JustDial, UrbanClap)
- Auto-resume scraping if interrupted

---

## 🛡️ Disclaimer
This tool is intended for educational and ethical use only. Always follow [Houzz’s Terms of Use](https://www.houzz.com/termsOfUse).

---

## 📬 Contact
For questions, suggestions, or collaboration:
- 📧 your.email@example.com
- 💼 [LinkedIn](https://linkedin.com/in/yourprofile)

---

Made  using Python, Streamlit, and OpenAI.
