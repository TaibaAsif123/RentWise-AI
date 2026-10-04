# 🏠 RentWise AI

**Rent smarter. Investigate before you commit.**

RentWise AI is an AI-assisted rental property screening tool. Instead of just listing properties, it checks a listing against the renter's requirements and flags missing or unclear information, so the renter knows what to verify before committing.

> Built for the **Aspire Pakistan Hackathon**: the Final (2nd) Hackathon of the HEC-NCEAC & PEC Generative & Agentic AI Training (Cohort 11), October 2026.

## The Problem

Rental listings are often incomplete. They may not mention the security deposit, maintenance charges, utility arrangements, or who actually owns the property. Renters usually discover these gaps only after investing time or money.

## The Solution

RentWise lets a renter search listings by their requirements, pick a property, and run an investigation that covers four areas:

| Analysis | What it checks |
|---|---|
| 💰 \**Price** | Is the rent within budget, and what costs are unstated? |
| 📍 **Location** | Does the listing match the preferred city and area? |
| 📋 **Requirements** | Bedrooms, bathrooms, property type, furnishing, parking |
| 🛡️ **Risk** | Missing details, unclear terms, and questions to ask the landlord |

The result includes a **RentWise score (0-100)**, a **risk level**, a **verdict**, and a list of **questions to ask the landlord**. Users can also **compare multiple investigated properties** and get an AI recommendation.

> RentWise is a **risk-screening assistant**. It does not claim to prove whether a property or landlord is legitimate or fraudulent. Missing information is treated as something to verify, not as proof of wrongdoing.

---

## Features

- 🔎 Search 4,161 Islamabad and Rawalpindi rental listings by budget, city, bedrooms, bathrooms, and property type
- 🏘️ Property cards with a one-click **Investigate** button
- 🤖 AI analysis of price, location, requirements, and risk using Google Gemini
- ⭐ Weighted RentWise score and a Proceed / Proceed with caution / Do not proceed verdict
- ❓ Auto-generated questions to ask the landlord
- ⚖️ Side-by-side comparison of investigated properties, with an optional AI recommendation
- 🛡️ **Rule-based fallback**: if Gemini is unavailable (quota, network, missing key), the app still returns a result and clearly says so

---

## How It Works

```
Renter requirements
        ↓
Search rental dataset  →  Property cards
        ↓
Select a property
        ↓
Price + Location + Requirements + Risk analysis (Gemini)
        ↓
Weighted score + risk level + verdict
        ↓
Landlord questions  →  Compare properties
```

**Scoring:** Gemini produces the yes/no findings and explanations. The final score is then calculated in Python with a fixed weighted formula: requirements 30%, price 25%, location 25%, risk 20%.

---

## Tech Stack

- **Frontend:** Streamlit (multi-page app)
- **AI:** Google Gemini via the `google-genai` SDK
- **Data:** pandas, CSV rental dataset
- **Language:** Python

## Project Structure

```
RentWise/
├── app.py                  # Navigation / router
├── rentwise_backend.py     # Gemini analysis, scoring, fallback, comparison
├── property_search.py      # Dataset loading and filtering
├── rental_properties.csv   # Rental listings (Islamabad & Rawalpindi)
├── requirements.txt
└── pages/
    ├── home.py
    ├── how_it_works.py
    ├── investigate.py      # Search, cards, results, comparison
    ├── risk_analysis.py
    └── requirements.py
```

---

## Run Locally

```bash
git clone [your-repo-url]
cd [repo-folder]
pip install -r requirements.txt
```

Set your Gemini API key (get one from [Google AI Studio](https://aistudio.google.com)).

## Data

The property data is a **snapshot** of a Pakistan real-estate dataset (originally from Kaggle), filtered to rental listings in Islamabad and Rawalpindi (4,161 listings). It is **not a live connection** to any listing website.

## Limitations

- Listings come from a static dataset, not live data.
- The dataset does not include details such as furnishing, parking, security deposit, or ownership, so RentWise reports these as "not stated" and asks the renter to verify them.
- Gemini's free-tier quota is limited; the rule-based fallback keeps the app usable when it runs out.
- Scores come from a fixed formula and are a screening aid, not a guarantee.

## Future Work

- Live listing sources or a landlord-submitted listing form
- Landlord and ownership verification workflows
- More cities and richer listing details
- Saved searches and exportable investigation reports

## Acknowledgements

- Aspire Pakistan, PAK Angels, iCode Guru, HEC-NCEAC & PEC for the Generative & Agentic AI Training and Hackathon
