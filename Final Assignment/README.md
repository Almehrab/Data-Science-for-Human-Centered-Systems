# SerafinoSignal Streamlit App

## Files

- `app.py` — Streamlit dashboard
- `streamlit_reviews.csv` — export this from the final notebook
- `requirements.txt` — deployment dependencies

## Export data from the notebook

Run this after the final theme and restaurant-type columns have been created:

```python
streamlit_export = model_df[
    [
        'business_name',
        'text_original',
        'rating',
        'rating_category',
        'rating_group',
        'review_word_count',
        'final_cluster',
        'theme',
        'theme_confidence',
        'restaurant_type'
    ]
].copy()

streamlit_export.to_csv(
    'streamlit_reviews.csv',
    index=False
)

print('Saved:', streamlit_export.shape)
```

Copy `streamlit_reviews.csv` into the same folder as `app.py`.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
