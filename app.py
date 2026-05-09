import json
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Outfit Theme Research Dashboard",
    page_icon="👗",
    layout="wide",
)


TRAIN_PATH = "data/cleaned_outfits_train.json"
TEST_PATH = "data/cleaned_outfits_test.json"
CATEGORY_SUMMARY_PATH = "data/category_summarize.json"


@st.cache_data
def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_data
def load_outfit_data():
    train_data = load_json(TRAIN_PATH)
    test_data = load_json(TEST_PATH)

    train_df = pd.DataFrame(train_data)
    test_df = pd.DataFrame(test_data)

    train_df["split"] = "train"
    test_df["split"] = "test"

    df = pd.concat([train_df, test_df], ignore_index=True)

    df["num_items"] = df["items_category"].apply(len)
    df["category_ids_text"] = df["items_category"].apply(
        lambda values: ", ".join(map(str, values))
    )

    return df


@st.cache_data
def load_category_summary():
    category_data = load_json(CATEGORY_SUMMARY_PATH)

    category_df = pd.DataFrame(category_data)

    if "items" in category_df.columns:
        category_df["num_item_examples"] = category_df["items"].apply(len)

    return category_df


def build_category_frequency(outfit_df, category_df):
    all_category_ids = []

    for categories in outfit_df["items_category"]:
        all_category_ids.extend(categories)

    frequency_counter = Counter(all_category_ids)

    frequency_df = pd.DataFrame(
        [
            {"id": category_id, "count_in_outfits": count}
            for category_id, count in frequency_counter.items()
        ]
    )

    frequency_df["id"] = frequency_df["id"].astype(int)
    category_df["id"] = category_df["id"].astype(int)

    merged_df = frequency_df.merge(
        category_df[["id", "name", "frequency"]],
        on="id",
        how="left",
    )

    merged_df = merged_df.sort_values(
        "count_in_outfits",
        ascending=False,
    )

    return merged_df


outfit_df = load_outfit_data()
category_df = load_category_summary()


st.title("Outfit Theme Research Dashboard")

st.write(
    """
    This dashboard explores the real outfit dataset used in a theme-aware outfit
    recommendation research project. It summarizes train/test splits, theme labels,
    outfit sizes, and category usage patterns.
    """
)


st.sidebar.header("Filters")

split_options = ["All"] + sorted(outfit_df["split"].unique().tolist())
selected_split = st.sidebar.selectbox("Dataset split", split_options)

theme_options = ["All"] + sorted(outfit_df["theme"].unique().tolist())
selected_theme = st.sidebar.selectbox("Theme", theme_options)

min_items = int(outfit_df["num_items"].min())
max_items = int(outfit_df["num_items"].max())

selected_item_range = st.sidebar.slider(
    "Number of items per outfit",
    min_value=min_items,
    max_value=max_items,
    value=(min_items, max_items),
)


filtered_df = outfit_df.copy()

if selected_split != "All":
    filtered_df = filtered_df[filtered_df["split"] == selected_split]

if selected_theme != "All":
    filtered_df = filtered_df[filtered_df["theme"] == selected_theme]

filtered_df = filtered_df[
    (filtered_df["num_items"] >= selected_item_range[0])
    & (filtered_df["num_items"] <= selected_item_range[1])
]


if filtered_df.empty:
    st.warning("No outfits match the selected filters.")
    st.stop()


st.subheader("Dataset Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Outfits", len(filtered_df))

with col2:
    st.metric("Themes", filtered_df["theme"].nunique())

with col3:
    st.metric("Categories", len(category_df))

with col4:
    st.metric("Average Items", round(filtered_df["num_items"].mean(), 2))

with col5:
    st.metric("Max Items", int(filtered_df["num_items"].max()))


st.subheader("Split Summary")

split_summary = (
    outfit_df.groupby("split")
    .agg(
        total_outfits=("set_id", "count"),
        average_items=("num_items", "mean"),
        min_items=("num_items", "min"),
        max_items=("num_items", "max"),
    )
    .reset_index()
)

split_summary["average_items"] = split_summary["average_items"].round(2)

st.dataframe(split_summary, use_container_width=True)


st.subheader("Theme Distribution")

theme_counts = filtered_df["theme"].value_counts()

fig, ax = plt.subplots()
ax.bar(theme_counts.index, theme_counts.values)
ax.set_xlabel("Theme")
ax.set_ylabel("Number of Outfits")
ax.set_title("Theme Distribution")
plt.xticks(rotation=30)

st.pyplot(fig)


st.subheader("Outfit Size Distribution")

size_counts = filtered_df["num_items"].value_counts().sort_index()

fig, ax = plt.subplots()
ax.bar(size_counts.index.astype(str), size_counts.values)
ax.set_xlabel("Number of Items")
ax.set_ylabel("Number of Outfits")
ax.set_title("Outfit Size Distribution")

st.pyplot(fig)


st.subheader("Theme-Level Summary")

theme_summary = (
    filtered_df.groupby("theme")
    .agg(
        total_outfits=("set_id", "count"),
        average_items=("num_items", "mean"),
        min_items=("num_items", "min"),
        max_items=("num_items", "max"),
    )
    .reset_index()
    .sort_values("total_outfits", ascending=False)
)

theme_summary["average_items"] = theme_summary["average_items"].round(2)

st.dataframe(theme_summary, use_container_width=True)


st.subheader("Top Category Usage")

category_frequency_df = build_category_frequency(filtered_df, category_df)

top_n = st.slider(
    "Number of top categories to show",
    min_value=5,
    max_value=30,
    value=15,
)

top_categories = category_frequency_df.head(top_n)

fig, ax = plt.subplots()
ax.barh(top_categories["name"], top_categories["count_in_outfits"])
ax.set_xlabel("Count in Filtered Outfits")
ax.set_ylabel("Category")
ax.set_title("Most Frequent Categories")
ax.invert_yaxis()

st.pyplot(fig)

st.dataframe(top_categories, use_container_width=True)


st.subheader("Category Metadata")

category_display_columns = ["id", "name", "frequency"]

if "num_item_examples" in category_df.columns:
    category_display_columns.append("num_item_examples")

st.dataframe(
    category_df[category_display_columns].sort_values(
        "frequency",
        ascending=False,
    ),
    use_container_width=True,
)


st.subheader("Real Outfit Records")

display_columns = [
    "set_id",
    "split",
    "theme",
    "num_items",
    "category_ids_text",
]

st.dataframe(
    filtered_df[display_columns].head(300),
    use_container_width=True,
)


st.subheader("Portfolio Note")

st.write(
    """
    This project transforms research preprocessing files into an interactive dashboard.
    It demonstrates practical skills in Python, data cleaning, exploratory analysis,
    visualization, and research data presentation.
    """
)