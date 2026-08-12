# Data Science for Human-Centered Systems

This repository contains my coursework and final project for **Data Science for Human-Centered Systems**. The work focuses on applying data science and machine learning methods to human-centered problems, with an emphasis on transforming raw data into interpretable and actionable insights.

## Final Project: SerafinoSignal

**SerafinoSignal** is a restaurant review intelligence project that analyzes **1,100 customer reviews across 100 restaurants** to identify meaningful experience themes, operational concerns, and differences across restaurants and restaurant types.

The project combines exploratory data analysis, natural language processing, unsupervised machine learning, model comparison, and an interactive Streamlit dashboard. The goal is not only to discover statistical patterns, but to translate those patterns into findings that restaurant stakeholders can understand and act on.

## Project Workflow

* Dataset documentation and data quality assessment
* Data cleaning and preprocessing
* Exploratory data analysis
* Review text preprocessing
* TF-IDF with K-Means baseline clustering
* SentenceTransformer semantic embeddings
* Semantic K-Means clustering
* UMAP dimensionality reduction
* HDBSCAN density-based clustering experiment
* Quantitative and qualitative model evaluation
* Final model selection based on separation, coverage, coherence, and interpretability
* Human-readable theme identification
* Restaurant-level theme analysis
* Restaurant-type comparison
* Operational complaint analysis
* Platform baseline and theme lift analysis
* Stakeholder-focused interpretation
* Interactive Streamlit dashboard

## Final Modeling Approach

Three clustering approaches were evaluated:

1. **TF-IDF + K-Means** as an interpretable lexical baseline
2. **SentenceTransformer + K-Means** for semantic clustering
3. **UMAP + HDBSCAN** for discovering dense and potentially niche review patterns

SentenceTransformer embeddings with K-Means were selected as the primary model because they provided the strongest practical balance between semantic coherence, full review coverage, manageable cluster structure, and stakeholder interpretability.

The final model produced **11 interpretable review themes**, including:

* Food Taste & Satisfaction
* Regional / Specialty Food Experience
* Overall Dining Experience & Menu Variety
* Price & Value
* Pizza Experience
* Waiting Time & Service Friction
* Staff & Service Quality
* Cleanliness, Ambience & Environment
* Burger Experience
* Positive Overall Experience
* Short Positive Praise / Recommendation

## Stakeholder Analysis

The final analysis goes beyond identifying clusters by examining how themes vary across individual restaurants and supported restaurant types.

Operational themes such as **Price & Value**, **Waiting Time & Service Friction**, **Staff & Service Quality**, and **Cleanliness, Ambience & Environment** were compared against platform-level patterns to identify areas that over-index or under-index for different restaurant types.

Restaurant-type findings are limited to categories with sufficient representation in the dataset to avoid presenting weak comparisons as reliable findings.

## Interactive Dashboard

The project includes **SerafinoSignal**, an interactive dashboard built with Streamlit for stakeholder exploration.

The dashboard supports:

* Platform-level review intelligence
* Theme exploration
* Rating-group filtering
* Restaurant-type filtering
* Individual restaurant drilldowns
* Theme concentration analysis
* Rating profiles
* Restaurant-level evidence
* Cross-restaurant and restaurant-type comparisons

The dashboard is designed to make the modeling results accessible without requiring stakeholders to inspect the underlying notebook or machine learning code.

## Tools and Libraries

* Python
* Jupyter Notebook
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* SentenceTransformers
* UMAP
* HDBSCAN
* Streamlit
* Plotly

## Note

This repository is intended for academic and portfolio purposes. Some datasets, assignment instructions, or other course-restricted materials may be excluded from the public repository.
