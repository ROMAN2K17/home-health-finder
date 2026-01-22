import streamlit as st
import csv
import os

# -----------------------------
# Load data from CSV
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "home_healths.csv")

def load_companies(csv_file=CSV_PATH):
    companies = []
    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            insurances = [i.strip() for i in row["insurance"].split("|")] if row["insurance"].strip().lower() != "unknown" else []
            service_areas = [a.strip() for a in row["service_area"].split("|")] if row["service_area"].strip().lower() != "unknown" else []
            email = row["email"].strip() if "email" in row else ""

            companies.append({
                "name": row["name"].strip(),
                "first_dose": row["first_dose"].strip().lower() == "yes",
                "insurance": insurances,
                "service_area": service_areas,
                "email": email
            })
    return companies

companies = load_companies()
st.write("Companies loaded:", len(companies))  # Debug to check CSV is found

# -----------------------------
# Helper function
# -----------------------------
def filter_companies(companies, insurance, first_dose, service_areas):
    results = []
    for company in companies:
        if insurance and not any(
            insurance.lower() in ins.lower()
            for ins in company["insurance"]
        ):
            continue
        if first_dose and not company["first_dose"]:
            continue
        if service_areas and not any(
            area in company["service_area"] for area in service_areas
        ):
            continue
        results.append(company)
    return results

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Home Health Finder", layout="wide")
st.title("🏥 Home Health Company Finder")

st.sidebar.header("Filters")

insurance_options = sorted(
    {ins for company in companies for ins in company["insurance"]}
)
selected_insurance = st.sidebar.selectbox(
    "Insurance Accepted",
    ["Any"] + insurance_options
)

first_dose_only = st.sidebar.checkbox("First Dose Required")

service_area_options = sorted(
    {area for company in companies for area in company["service_area"]}
)
selected_service_areas = st.sidebar.multiselect(
    "Service Area",
    service_area_options
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered = filter_companies(
    companies,
    insurance=None if selected_insurance == "Any" else selected_insurance,
    first_dose=first_dose_only,
    service_areas=selected_service_areas
)

# -----------------------------
# Results
# -----------------------------
st.subheader("Results")

if not filtered:
    st.warning("No companies match your filters.")
else:
    for company in filtered:
        st.markdown(f"### {company['name']}")
        st.write("**First Dose:**", "Yes" if company["first_dose"] else "No")
        st.write("**Service Areas:**", ", ".join(company["service_area"]))
        st.write("**Insurance Accepted:**", ", ".join(company["insurance"]))
        if company["email"]:
            st.write("**Email:**", company["email"])
        st.divider()
