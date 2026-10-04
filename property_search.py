import os
import re
from functools import lru_cache
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROPERTY_DATABASE = os.path.join(BASE_DIR, "rental_properties.csv")


def extract_price(value):
    value = str(value).replace("\\n", " ").strip()
    value = value.replace("PKR", "").strip()
    match = re.search(r"[\d.]+", value)
    if not match:
        return None

    amount = float(match.group())
    text = value.lower()
    if "crore" in text:
        amount *= 10_000_000
    elif "lakh" in text:
        amount *= 100_000
    elif "thousand" in text:
        amount *= 1_000
    return amount


@lru_cache(maxsize=1)
def load_properties():
    properties = pd.read_csv(PROPERTY_DATABASE)
    properties["price_numeric"] = properties["price"].apply(extract_price)
    properties["bedroom_numeric"] = pd.to_numeric(properties["bedroom"], errors="coerce")
    properties["bath_numeric"] = pd.to_numeric(properties["bath"], errors="coerce")
    return properties


def search_properties(city="Islamabad", max_budget=100000, min_bedrooms=2,
                      min_bathrooms=2, property_type="Flat"):
    properties = load_properties()
    results = properties[
        (properties["location_city"].astype(str).str.strip().str.lower() == city.lower())
        & (properties["price_numeric"] <= max_budget)
        & (properties["bedroom_numeric"] >= min_bedrooms)
        & (properties["bath_numeric"] >= min_bathrooms)
        & (properties["type"].astype(str).str.strip().str.lower() == property_type.lower())
    ].copy()
    return results