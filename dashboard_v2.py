import streamlit as st
import pandas as pd
from filter_config import category_lookup, city_lookup, build_houzz_url
from agent_modules.agent_directory_scraper import scrape_directory_page
from agent_modules.website_contact_extractor import extract_contacts_from_website
import os
import io
import datetime

RESULT_FILE = "houzz_final_results.xlsx"

st.set_page_config(page_title="Houzz Smart Scraper", layout="wide")
st.title("\U0001f3d7️ Houzz Smart Scraper Dashboard")

st.sidebar.header("\U0001f4c2 Scraper Filters")

category = st.sidebar.selectbox("Select Category", list(category_lookup.keys()))
city_options = ["-- No City Filter --"] + list(city_lookup.keys())
city = st.sidebar.selectbox("Select City", city_options)

start_page = st.sidebar.number_input("Start Page", min_value=1, step=1, value=1)
max_pages = st.sidebar.slider("Pages to Scrape", min_value=1, max_value=10, value=1)

if st.sidebar.button("\U0001f680 Start Scraping"):
    st.info(f"Starting scrape for {category} in {city if city != '-- No City Filter --' else 'All Locations'}...")
    all_results = []

    try:
        start_page = int(start_page)
        max_pages = int(max_pages)
    except Exception as e:
        st.error(f"Invalid page inputs: {e}")
        st.stop()

    for offset in range(max_pages):
        page_num = start_page + offset
        try:
            if city == "-- No City Filter --":
                houzz_url = f"https://www.houzz.in/professionals/{category_lookup[category]}/probr0-bo~t_{category_lookup[category].split('-')[-1]}?fi={(page_num - 1) * 15}"
            else:
                houzz_url = build_houzz_url(category, city, page_num)

            st.code(houzz_url)
            directory_data = scrape_directory_page(houzz_url)
            st.write("\U0001f9ea Listings Found:", len(directory_data))

            for idx, entry in enumerate(directory_data, start=1):
                name = entry.get("company")
                website = entry.get("website")

                st.markdown(f"🔍 **[{idx}] Processing:** `{name}`")

                emails, instagrams = [], []
                if website and website.startswith("http"):
                    st.write(f"🌐 Visiting website: {website}")
                    result = extract_contacts_from_website(website)
                    emails = result.get("emails", [])
                    instagrams = result.get("instagram", [])
                    st.write(f"📨 Emails found: {emails}")
                    st.write(f"📸 Instagram: {instagrams}")

                all_results.append({
                    "Company": name,
                    "Mobile": entry.get("mobile"),
                    "Email": "; ".join(emails),
                    "Website": website,
                    "Instagram": "; ".join(instagrams),
                    "Category": category,
                    "City": city if city != "-- No City Filter --" else "--"
                })
                st.markdown("---")
        except Exception as e:
            st.warning(f"❌ Failed on page {page_num}: {e}")

    if all_results:
        df_new = pd.DataFrame(all_results)

        # Save per-page file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        city_tag = city.lower().replace(" ", "_") if city != "-- No City Filter --" else "all"
        per_page_file = f"houzz_{city_tag}_{category.lower().replace(' ', '_')}_p{start_page}_to_p{start_page + max_pages - 1}.xlsx"
        df_new.to_excel(per_page_file, index=False)
        st.success(f"🗂️ Saved this batch to: {per_page_file}")

        # Save to cumulative final file
        if os.path.exists(RESULT_FILE):
            df_existing = pd.read_excel(RESULT_FILE)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new

        df_combined.drop_duplicates(subset=["Company", "Website"], inplace=True)
        df_combined.to_excel(RESULT_FILE, index=False)

        # Download button for final Excel
        excel_buffer = io.BytesIO()
        df_combined.to_excel(excel_buffer, index=False, engine="xlsxwriter")
        excel_buffer.seek(0)

        st.download_button(
            label="⬇️ Download Full Combined Excel",
            data=excel_buffer,
            file_name=RESULT_FILE,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("No data found. Please check filters or try a different page range.")

if os.path.exists(RESULT_FILE):
    with st.expander("\U0001f4ca View Current Dataset"):
        df_current = pd.read_excel(RESULT_FILE)
        st.dataframe(df_current, use_container_width=True)
