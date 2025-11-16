# Climate Change – Interactive Visualization (Dash & Plotly)

An interactive web application built with **Python**, **Dash**, and **Plotly** to explore global land surface temperature trends over time.  
The app is deployed on **Render** and allows users to visualize long-term climate patterns for different cities around the world.

🌐 **Live app:** https://climate-analysis-shr.onrender.com  

---

## 🧊 Project Overview

This project uses historical temperature records to help users:

- Explore **temperature trends over time** for specific cities or regions  
- Visualize **long-term warming patterns** using interactive line charts and other visualizations  
- Filter data by **city**, **time range**, or other attributes (depending on the app’s controls)  
- Gain an intuitive understanding of how **global warming** has affected different parts of the world  

The goal is to make climate data **accessible**, **visual**, and **interactive** for students, researchers, and anyone interested in climate change.

---

## 📊 Dataset

The data used in this project comes from **Berkeley Earth** and is publicly available on Kaggle:

- **Source:** *Climate Change: Earth Surface Temperature Data*  
- **File used:** `GlobalLandTemperaturesByCity.csv`  
- **Kaggle link:**  
  https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

> **Note:** Due to Kaggle’s terms, you need to manually download the dataset from Kaggle and place it in the project folder (see instructions below).

---

## 🧱 Main Features

- Built with **Dash** (Plotly’s web framework for Python)
- Interactive **time-series plots** of land temperatures
- City-level or region-level filtering (depending on your implementation)
- Basic **data cleaning** and **preprocessing** for the Kaggle dataset
- Deployed as a web app using **Render**

---

## 🗂 Project Structure

A typical structure for this project might look like:

```bash
.
├── app.py                # Main Dash application
├── requirements.txt      # Python dependencies
├── data/
│   └── GlobalLandTemperaturesByCity.csv
├── assets/               # (Optional) CSS or static assets for Dash
└── README.md
