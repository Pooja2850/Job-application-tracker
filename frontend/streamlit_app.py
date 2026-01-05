import streamlit as st
import requests
from datetime import date

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Job Tracker", layout="wide")
st.title("Job Tracker")

# Helpers
def fetch_applications():
    resp = requests.get(f"{API_URL}/applications", timeout=10)
    resp.raise_for_status()
    return resp.json()

def create_application(payload: dict):
    resp = requests.post(f"{API_URL}/applications", json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()

st.sidebar.header("Filters")
status_filter = st.sidebar.selectbox(
    "Status", 
    options=["All", "Interested", "Applied", "OA", "Interview", "Offer", "Rejected", "Ghosted"],
    index=0
)

def update_application(app_id: int, payload: dict):
    resp = requests.patch(f"{API_URL}/applications/{app_id}", json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()

# Add form
st.subheader("Add an application")

with st.form("add_app_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input("Company", placeholder="Google", max_chars=100)
        role_title = st.text_input("Role title", placeholder="Software Engineer New Grad", max_chars=120)
        location = st.text_input("Location", placeholder="Mountain View, CA", max_chars=120)
        link = st.text_input("Job link", placeholder="https://...", max_chars=300)

    with col2:
        date_applied = st.date_input("Date applied", value=date.today())
        status = st.selectbox("Status", ["Interested", "Applied", "OA", "Interview", "Offer", "Rejected", "Ghosted"], index=1)
        tags = st.text_input("Tags", placeholder="backend, newgrad")
        notes = st.text_area("Notes", placeholder="Any notes...", height=100)

    submitted = st.form_submit_button("Save")

    if submitted:
        if not company.strip() or not role_title.strip():
            st.error("Company and Role title are required.")
        else:
            payload = {
                "company": company.strip(),
                "role_title": role_title.strip(),
                "location": location.strip() or None,
                "link": link.strip() or None,
                "date_applied": str(date_applied) if date_applied else None,
                "status": status,
                "tags": tags.strip() or None,
                "notes": notes.strip() or None,
            }

            try:
                created = create_application(payload)
                st.success(f"Saved: {created['company']} | {created['role_title']}")
                st.rerun()
            except requests.RequestException as e:
                st.error(f"Failed to save. Error: {e}")

# List applications
st.subheader("Applications")

try:
    data = fetch_applications()
except requests.RequestException as e:
    st.error(f"Could not load applications. Is the backend running? Error: {e}")
    st.stop()

# Apply filter
if status_filter != "All":
    data = [row for row in data if row.get("status") == status_filter]

# Display
if not data:
    st.info("No applications to display.")
else:
    display_rows = []
    for row in data:
        display_rows.append({
            "Company": row["company"],
            "Role": row["role_title"],
            "Location": row["location"],
            "Date Applied": row["date_applied"],
            "Status": row["status"],
            "Tags": row["tags"],
            "Notes": row["notes"], 
        })

    st.dataframe(
        display_rows,
        use_container_width=True,
        hide_index=True
    )

st.subheader("Update an application")

if data:
    label_to_id = {
        f"{row['company']} | {row['role_title']} | id {row['id']}": row["id"]
        for row in data
    }
    selected_label = st.selectbox("Select", options=list(label_to_id.keys()))
    selected_id = label_to_id[selected_label]

    new_status = st.selectbox(
        "New status", 
        ["Interested", "Applied", "OA", "Interview", "Offer", "Rejected", "Ghosted"]
    )
    new_notes = st.text_area("Update notes", placeholder="Add or replace notes")

    if st.button("Apply update"):
        try:
            update_application(selected_id, {"status": new_status, "notes": new_notes.strip() or None})
            st.success("Updated")
            st.rerun()
        except requests.RequestException as e:
            st.error(f"Update failed: {e}")