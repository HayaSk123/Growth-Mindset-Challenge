import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Growth Mindset Challenge", layout="wide")
st.title("Data Sweeper")
st.write("Easily convert CSV and Excel files and enhance your data with built-in cleaning and visualization.")
st.write("Upload your file and let the magic happen!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload CSV or Excel file.")
            continue

        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")

        st.write("Preview the head of the dataframe")
        st.dataframe(df.head())

        st.subheader("Data Cleaning Options")

        if st.checkbox(f"Clean data for {uploaded_file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed")
                    st.dataframe(df.head())

            with col2:
                if st.button(f"Fill missing values for {uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled")
                    st.dataframe(df.head())

        st.subheader("Choose colums to convert")
        columns = st.multiselect(f"Choose columns for {uploaded_file.name}" , df.columns, default=df.columns)
        df = df[columns]

        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization for {uploaded_file.name}"):
            st.bar_chart(df.select_dtypes(include ="number").iloc[:,2])

        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {uploaded_file.name} to: ", ["CSV", "Excel"], key=uploaded_file.name)
        if st.button(f"Convert {uploaded_file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer , index=False)
                file_name = uploaded_file.name.replace(file_ext,".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer , index=False)
                file_name = uploaded_file.name.replace(file_ext,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label =(f"Download {uploaded_file.name} as {conversion_type}"),
                data = buffer,
                file_name = file_name,
                mime=mime_type
            )

st.success("All files have successfully been processesd")