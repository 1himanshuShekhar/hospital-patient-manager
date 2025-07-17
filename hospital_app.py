import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize patient list in session
if 'patients' not in st.session_state:
    st.session_state.patients = []

st.set_page_config(page_title="Hospital Patient Manager", layout="centered")
st.title("🏥 Hospital Patient Manager")

# ------------------ Add Patient ------------------
st.header("➕ Add New Patient")
with st.form("add_form"):
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
    disease = st.text_input("Disease")

    submitted = st.form_submit_button("Add Patient")
    if submitted:
        st.session_state.patients.append({
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Disease": disease
        })
        st.success(f"✅ Patient '{name}' added!")

# ------------------ Search Patient ------------------
st.header("🔍 Search Patients")
search_term = st.text_input("Search by name").lower()

filtered_patients = [
    p for p in st.session_state.patients
    if search_term in p["Name"].lower()
]

# ------------------ Display Table ------------------
st.header("📋 Patient Records")

if filtered_patients:
    df = pd.DataFrame(filtered_patients)
    st.dataframe(df, use_container_width=True)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "patients.csv", "text/csv")

    # ------------------ Stats ------------------
    st.subheader("📊 Gender Distribution")
    fig = px.pie(df, names='Gender', title='Patient Gender Ratio')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Summary")
    st.write(f"👨 Male Patients: {df[df['Gender'] == 'Male'].shape[0]}")
    st.write(f"👩 Female Patients: {df[df['Gender'] == 'Female'].shape[0]}")
    st.write(f"🧑‍🦰 Other: {df[df['Gender'] == 'Other'].shape[0]}")
    st.write(f"📌 Total Patients: {df.shape[0]}")

else:
    st.info("No matching patients found or none added yet.")

# ------------------ Footer ------------------
st.markdown("---")
st.markdown("👨‍⚕️ *Made by Himanshu | CipherSchool Project*")
