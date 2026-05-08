import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Outfit Theme Analysis Dashboard",
    page_icon="👗",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv("data/sample_outfits.csv")


df = load_data()


st.title("Outfit Theme Analysis Dashboard")
st.write(
    "A simple dashboard for exploring outfit themes, categories, and basic dataset statistics."
)

st.sidebar.header("Filters")

theme_options = ["All"] + sorted(df["theme"].unique().tolist())
selected_theme = st.sidebar.selectbox("Select theme", theme_options)

if selected_theme != "All":
    filtered_df = df[df["theme"] == selected_theme]
else:
    filtered_df = df.copy()


st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Outfits", len(filtered_df))

with col2:
    st.metric("Number of Themes", filtered_df["theme"].nunique())

with col3:
    st.metric("Average Items per Outfit", round(filtered_df["num_items"].mean(), 2))


st.subheader("Theme Distribution")

theme_counts = filtered_df["theme"].value_counts()

fig, ax = plt.subplots()
ax.bar(theme_counts.index, theme_counts.values)
ax.set_xlabel("Theme")
ax.set_ylabel("Number of Outfits")
ax.set_title("Number of Outfits by Theme")
plt.xticks(rotation=30)

st.pyplot(fig)


st.subheader("Category Summary")

category_columns = [
    "top_category",
    "bottom_category",
    "shoe_category",
    "accessory_category"
]

selected_category_column = st.selectbox(
    "Choose category type",
    category_columns
)

category_counts = (
    filtered_df[selected_category_column]
    .replace("None", pd.NA)
    .dropna()
    .value_counts()
    .reset_index()
)

category_counts.columns = ["Category", "Count"]

st.dataframe(category_counts, use_container_width=True)


st.subheader("Outfit Data")

st.dataframe(filtered_df, use_container_width=True)


st.subheader("Project Purpose")

st.write(
    """
    This dashboard is designed as a portfolio project based on outfit recommendation research.
    Version 1 focuses on basic exploratory data analysis using sample outfit data.
    
    Future versions can include CSV upload, theme prediction results, FITB evaluation summaries,
    category grouping analysis, and model comparison charts.
    """
)