import streamlit as st
import pandas as pd
import os
from io import BytesIO 
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data Sweeper", layout="wide")

st.title("🧹 Datasweeper ⚡ Sterling Integrator 🌟 By Sahil")
st.write("A powerful tool for cleaning, transforming, and visualizing data.")

# File Upload Section
uploaded_files = st.file_uploader("Upload Your Files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type")
            continue  # Skip this file

        # Data Cleaning Options
        st.subheader(f"Data Cleaning Options for {file.name}")
        if st.checkbox(f"Clean Data for {file.name}"):
            if st.button(f"Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates Removed!")

            if st.button(f"Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing Values Filled!")

        # Column Selection
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # **Data Visualization Section**
        st.subheader(f"📊 Data Visualization for {file.name}")
        if st.checkbox(f"Show Visualization for {file.name}"):
            # Select Columns for Visualization
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            selected_column = st.selectbox(f"Select Column for Visualization ({file.name})", numeric_columns)

            if selected_column:
                fig, ax = plt.subplots()
                sns.histplot(df[selected_column], kde=True, bins=30, ax=ax)
                st.pyplot(fig)

        # **Data Conversion Options**
        st.subheader(f"🛠️ Conversion Options for {file.name}")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
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
                label="📥 Download Processed File",
                data=buffer,
                file_name=f"processed_{file_name}",
                mime=mime_type
            )

st.success("All Files Processed Successfully!")
