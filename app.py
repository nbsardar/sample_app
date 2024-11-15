# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the app
st.title("Simple Data Insights App")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load the data
    data = pd.read_csv(uploaded_file)

    # Display the raw data
    st.subheader("Raw Data Preview")
    st.write(data.head())

    # Show basic stats
    st.subheader("Data Statistics")
    st.write(data.describe())

    # Column selection for analysis
    numeric_columns = data.select_dtypes(include=["float64", "int64"]).columns
    selected_column = st.selectbox("Select a column for analysis", numeric_columns)

    # Plotting
    if selected_column:
        st.subheader(f"Distribution of {selected_column}")
        fig, ax = plt.subplots()
        sns.histplot(data[selected_column], kde=True, ax=ax)
        st.pyplot(fig)

        # Scatter plot for bivariate analysis
        other_column = st.selectbox("Select another column for scatter plot", numeric_columns)
        if other_column and other_column != selected_column:
            st.subheader(f"Scatter plot between {selected_column} and {other_column}")
            fig, ax = plt.subplots()
            sns.scatterplot(data=data, x=selected_column, y=other_column, ax=ax)
            st.pyplot(fig)

    # Identifying outliers
    st.subheader("Outliers Detection")
    threshold = st.slider("Select threshold for outliers", min_value=1.5, max_value=3.5, value=3.0)
    outliers = data[(data[selected_column] > data[selected_column].mean() + threshold * data[selected_column].std()) |
                    (data[selected_column] < data[selected_column].mean() - threshold * data[selected_column].std())]
    st.write(outliers if not outliers.empty else "No outliers found")
