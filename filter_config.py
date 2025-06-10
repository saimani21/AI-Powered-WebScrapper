category_lookup = {
    "Interior Designers & Decorators": "t_11785",
    "Architects & Building Designers": "t_11784",
    "Design-Build Firms": "t_11783",
    "General Contractors": "t_11786",
    "Home Builders": "t_11823",
    "Kitchen & Bathroom Designers": "t_11787",
    "Kitchen & Bathroom Remodelers": "t_11825",
    "Landscape Architects & Landscape Designers": "t_11819",
    "Landscape Contractors": "t_11812",
    "Accessory Dwelling Units (ADU)": "t_27199",
    "Home Remodeling": "t_27180",
    "Home Additions": "t_27181"
}

city_lookup = {
    "Bengaluru": "r_1277333",
    "Mumbai": "r_1258650",
    "Delhi": "r_1261481",
    "Chennai": "r_1264527",
    "Hyderabad": "r_1269843",
    "Pune": "r_1259229"
}

def build_houzz_url(category_name, city_name, page_num=1):
    page_num = int(str(page_num).strip())
    cat_code = category_lookup.get(category_name)
    city_code = city_lookup.get(city_name)

    if not cat_code or not city_code:
        raise ValueError("Invalid category or city selection")

    cat_slug = category_name.lower().replace(" & ", "-").replace(" ", "-")
    city_slug = city_name.lower().replace(" ", "-") + "-19-in"
    start_index = (page_num - 1) * 15

    return f"https://www.houzz.com/professionals/{cat_slug}/{city_slug}-probr0-bo~{cat_code}~{city_code}?fi={start_index}"