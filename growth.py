import streamlit as st
import pandas as pd
import os
from io import BytesIO 

#Page
st.set_page_config(page_title="Data Sweeper Ch", layout="wide")

#Styling through CSS
st.markdown(
    """
    <style>
    .stApp { 
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("🧹 Datasweeper ⚡ Sterling Integrator 🌟 By Sahil")
st.write("Datasweeper Sterling Integrator is a powerful data processing and integration tool built using Python and Streamlit. It is designed to efficiently clean, transform, and integrate large datasets while ensuring smooth connectivity between different data sources.")

# File Uploader
uploaded_files = st.file_uploader("📂 Upload Your Files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read CSV File
        if file_ext == ".csv":
            df = pd.read_csv(file)
        # Read Excel File
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file format: {file_ext}")
            continue
        
        # Display Data
        st.write(f"### 📊 Preview of {file.name}")
        st.dataframe(df)

        # Data Cleaning Section
        st.subheader("🧼 Data Cleaning Options")
        
        if st.checkbox(f"🛠 Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🗑 Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")

            with col2:
                if st.button(f"🛠 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Have Been Filled!")

#data visualization
st.subheader("Data Visualization")
if st.checkbox(f"Show Visualization for {file.name}"):
    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

# Conversion Options
st.subheader("🔄 Conversion Options")

conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

if st.button(f"🔄 Convert {file.name}"):
    buffer = BytesIO()

    if conversion_type == "CSV":
        df.to_csv(buffer, index=False)
        file_name = file.name.replace(file_ext, ".csv")
        mime_type = "text/csv"

    elif conversion_type == "Excel":
        df.to_excel(buffer, index=False)
        file_name = file.name.replace(file_ext, ".xlsx")
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    buffer.seek(0)

    st.download_button(
        label="📥 Download Converted File",
        data=buffer,
        file_name=f"converted_{file_name}",
        mime=mime_type
    )

st.success("✅ All Files Processed Successfully!")
