# SerafinoSignal

SerafinoSignal is a restaurant review intelligence project that analyzes 1,100 customer reviews across 100 restaurants to identify meaningful complaint and experience themes.

The project compares TF IDF K Means, SentenceTransformer K Means, and UMAP with HDBSCAN. SentenceTransformer embeddings with K Means were selected as the final model for their balance of semantic coherence, review coverage, and interpretability.

## Key Features

- Restaurant review cleaning and exploratory analysis
- Semantic clustering of customer reviews
- Identification of 11 interpretable review themes
- Complaint analysis across individual restaurants
- Comparison of themes across restaurant types
- Interactive Streamlit dashboard for stakeholder exploration

## Tools

Python, Pandas, Scikit learn, SentenceTransformers, UMAP, HDBSCAN, Matplotlib, Seaborn, Plotly, Streamlit

## Project Files

- `app.py`: Streamlit dashboard
- `serafino_reviews.csv`: Processed data used by the dashboard
- `requirements.txt`: Application dependencies
- Jupyter Notebook: Full analysis and modeling workflow
