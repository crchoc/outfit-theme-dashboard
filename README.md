# Outfit Theme Research Dashboard

A Streamlit dashboard for exploring outfit themes, fashion categories, and basic dataset statistics.

## Project Overview

This project is an interactive Streamlit dashboard for exploring a real outfit recommendation research dataset.

The dashboard analyzes outfit theme labels, train/test splits, outfit size distributions, and fashion category usage patterns. It is based on data preprocessing files used in a theme-aware outfit recommendation research project.

## Features

- Load real train/test outfit JSON files
- Analyze theme distribution
- Compare train and test splits
- Explore outfit size distribution
- Show most frequent fashion categories
- View category metadata
- Filter by split, theme, and number of outfit items
- Display real outfit records

## Tech Stack

- Python
- Streamlit
- pandas
- NumPy
- matplotlib

## Required CSV Format

To upload your own dataset, the CSV file should contain these columns:

```csv
outfit_id,theme,top_category,bottom_category,shoe_category,accessory_category,num_items
```

Example:
```csv
outfit_id,theme,top_category,bottom_category,shoe_category,accessory_category,num_items
O001,Office Look,Blouse,Trousers,Loafers,Watch,4
O002,Sports,T-shirt,Shorts,Running Shoes,Cap,4
```

## Project Structure

```bash
outfit-theme-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── sample_outfits.csv
```

## How to Run

Clone the repository:
```bash
git clone YOUR_REPOSITORY_URL
cd outfit-theme-dashboard
```

Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the dashboard:
```bash
streamlit run app.py
```

## Version History
### Version 1
- Created basic Streamlit dashboard
- Added sample outfit dataset
- Added theme distribution chart
- Added category summary table

### Version 2
- Added CSV upload
- Added required column validation
- Added theme filter
- Added outfit size filter
- Added theme-level summary

## Future Improvements
- Add model result visualization
- Add FITB evaluation dashboard
- Add category grouping analysis
- Add model comparison charts
- Add downloadable reports