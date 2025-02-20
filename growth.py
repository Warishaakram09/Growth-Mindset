from pydoc import pager
import streamlit as st # type: ignore
import pandas as pd # type: ignore
import os
from io import BytestIO

st.set_page_config(page_title="Data Growth", layout="wide")

#custom css

st.markdown(
    """
    <style>
    .stApp
        background-color: #f0f6ff;
        color:white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description

st.title("Data Growth")
st.write("This app is used to calculate the growth of a dataset over time.")

# file uploader
uploaded_file = st.file_uploader("Choose a file(accetps CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1],lower() # type: ignore
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("File type not supported: {file_ext}")
            continue

        #file details
        st.write("Preview of the dataset")
        st.write(df.head())

        #data cleaning options
        st.write("Data Cleaning Options")
        if st.checkbox("clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Remove Duplicates from the files: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed")

                    with col2:
                        if st.button("Remove Missing Values from the file: {file.name}"):
                            numeric_cols = df.select_dtypes(include=["number"]).columns
                            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                            st.write("Missing Values Removed")

                st.subheader("Select Columns to Keep")
                columns = st.multiselect("Select Columns For {file.name}", df.columns)
                df = df[columns]

                #data visualization
                st.subheader("Data Visualization")
                if st.checkbox(f"Show Data Summary {file.name}"):
                    st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])

                #conversion options
                st.subheader("Data Conversion Options")
                conversion_type = st.radio(f"convert {file.name} to", ["csv", "Excel"], key=file.name)
                if st.button(f"Convert {file.name}"):
                    buffer = BytestIO()
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
                        label=f"Click to download {file_name}",
                        data=buffer,
                        file_name=file_name,
                        mime=mime_type
                    )
                    
                    st.success("All Files proceed successfully")
                    st.balloons()


