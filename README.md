# Outfit Theme Analysis Dashboard

A Streamlit dashboard for exploring outfit themes, fashion categories, and basic dataset statistics.

## Project Overview

This project is based on an outfit recommendation research topic.  
It provides a simple interactive dashboard for analyzing outfit data by theme and category.

Current themes:

- Office Look
- Ceremony
- Travel
- Sports

## Features

- View total number of outfits
- Filter outfits by theme
- Show theme distribution chart
- Analyze category frequency
- Display sample outfit dataset

## Tech Stack

- Python
- Streamlit
- pandas
- NumPy
- matplotlib

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

## Future Improvements
- Add CSV upload
- Add theme prediction results
- Add model comparison charts
- Add FITB evaluation dashboard
- Add category grouping analysis

---

## 10. Push to GitHub

```bash
git init
git add .
git commit -m "Initial version of outfit theme dashboard"
```