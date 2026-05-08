# Outfit Theme Analysis Dashboard

A Streamlit dashboard for exploring outfit themes, fashion categories, and basic dataset statistics.

## Project Overview

This project is based on an outfit recommendation research topic.  
It provides an interactive dashboard for analyzing outfit data by theme, category, and outfit size.

The dashboard can use a built-in sample dataset or a user-uploaded CSV file.

## Current Themes in Sample Data

- Office Look
- Ceremony
- Travel
- Sports

## Features

- Load built-in sample outfit data
- Upload a custom CSV file
- Validate required CSV columns
- Filter outfits by theme
- Filter outfits by number of items
- Show dataset overview metrics
- Show theme distribution chart
- Show category frequency table
- Show theme-level summary
- Display filtered outfit data

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