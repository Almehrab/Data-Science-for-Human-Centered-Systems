from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
st.set_page_config(page_title="SerafinoSignal",layout="wide",initial_sidebar_state="expanded",)
APP_TITLE = "SerafinoSignal"
APP_SUBTITLE = "Restaurant Review Theme Intelligence"
OPERATIONAL_THEMES = [ "Price & Value","Waiting Time & Service Friction", "Staff & Service Quality","Cleanliness, Ambience & Environment",]
RATING_GROUP_ORDER = ["NEGATIVE (1-2)","MIXED (3)","POSITIVE (4-5)",]
REQUIRED_COLUMNS = ["business_name","text_original","rating","rating_category","rating_group","review_word_count","final_cluster","theme","theme_confidence","restaurant_type",]
DATA_CANDIDATES = ["serafino_reviews.csv","streamlit_reviews.csv",]
# styling
st.markdown(
    """
    <style>
        :root {--ink: #18181b;--muted: #71717a;--panel: #ffffff;--panel-soft: #f8fafc;--line: #e4e4e7;--accent: #b45309;--accent-soft: #fff7ed;}

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 12%,0%, rgba(180,83,9,.07), transparent 24rem),
                linear-gradient(180deg, #fcfcfd 0%, #f7f7f8 100%);
        }
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stMetric"] label,
[data-testid="stSidebar"] [data-testid="stMetric"] label *,
[data-testid="stSidebar"] [data-testid="stMetricValue"],
[data-testid="stSidebar"] [data-testid="stMetricValue"] * {
    color: #18181b !important;
}
        [data-testid="stSidebar"] {background: #111113; }
        [data-testid="stSidebar"] * { color: #f4f4f5;}
        [data-testid="stSidebar"] input { color: #18181b !important;}
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {color: #18181b !important;}
        [data-testid="stMain"] p,
        [data-testid="stMain"] span,
        [data-testid="stMain"] label,
        [data-testid="stMain"] div {color: inherit; }
        [data-testid="stMain"] input,
        [data-testid="stMain"] textarea {color: #18181b !important;background: #ffffff !important;}
        [data-testid="stMain"] [data-baseweb="select"] > div {background: #ffffff !important; color: #18181b !important; }
        [data-testid="stMain"] [data-baseweb="tag"] {color: #ffffff !important;}
        [data-testid="stMain"] [data-testid="stDataFrame"] {background: #ffffff; border-radius: 14px;}
        .block-container {max-width: 1450px;padding-top: 1.6rem;padding-bottom: 4rem;}
        h1, h2, h3 {letter-spacing: -0.025em; }
        .hero {
            background:
                linear-gradient(135deg, rgba(17,17,19,.98), rgba(39,39,42,.96));
            color: white;
            border-radius: 24px;
            padding: 2rem 2.1rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 18px 50px rgba(0,0,0,.12);
            
        }
.hero,
.hero h1,
.hero h2,
.hero h3,
.hero p,
.hero span,
.hero div {
    color: #ffffff !important;
}

.hero .hero-eyebrow {
    color: #fdba74 !important;
}

.hero .hero-subtitle {
    color: #d4d4d8 !important;
}
        .hero-eyebrow {
            display: inline-block;
            font-size: .76rem;
            font-weight: 700;
            letter-spacing: .14em;
            text-transform: uppercase;
            color: #fdba74;
            margin-bottom: .7rem;
        }

        .hero-title {
            font-size: 2.5rem;
            line-height: 1.02;
            font-weight: 800;
            margin: 0;
        }

        .hero-subtitle {
            color: #d4d4d8;
            font-size: 1rem;
            max-width: 800px;
            margin-top: .75rem;
            margin-bottom: 0;
        }

        .section-label {
            color: var(--muted);
            font-size: .78rem;
            text-transform: uppercase;
            letter-spacing: .11em;
            font-weight: 750;
            margin: .6rem 0 .2rem 0;
        }

        .section-title {
            color: var(--ink);
            font-size: 1.55rem;
            font-weight: 780;
            margin: 0 0 .85rem 0;
        }

        .insight-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1.1rem 1.15rem;
            min-height: 158px;
            box-shadow: 0 8px 30px rgba(0,0,0,.035);
        }

        .insight-kicker {
            color: var(--muted);
            font-size: .72rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            font-weight: 750;
        }

        .insight-value {
            color: var(--ink);
            font-size: 1.65rem;
            line-height: 1.12;
            font-weight: 800;
            margin-top: .45rem;
        }

        .insight-detail {
            color: var(--muted);
            font-size: .83rem;
            margin-top: .5rem;
            line-height: 1.4;
        }

        .callout {
            background: var(--accent-soft);
            border: 1px solid #fed7aa;
            border-radius: 16px;
            padding: 1rem 1.15rem;
            color: #7c2d12;
            margin: .8rem 0 1.1rem 0;
        }

        .method-card {
    background: #18181b;
    border-radius: 16px;
    padding: 20px 22px;
    color: #f4f4f5 !important;
}

/* Force ALL nested text to stay visible */
.method-card,
.method-card p,
.method-card span,
.method-card div,
.method-card li {
    color: #f4f4f5 !important;
}

.method-card strong {
    color: #fdba74 !important;
}

        .method-card strong {
            color: #fdba74;
        }
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e4e4e7;
    border-radius: 14px;
    padding: 14px 16px;
}

[data-testid="stMetric"] label,
[data-testid="stMetric"] label * {
    color: #52525b !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #18181b !important;
}
        div[data-testid="stMetric"] {
            background: var(--panel);
            border: 1px solid var(--line);
            padding: .8rem 1rem;
            border-radius: 16px;
            box-shadow: 0 6px 24px rgba(0,0,0,.03);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: .4rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 44px;
            border-radius: 12px;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .stTabs [aria-selected="true"] {
            background: #18181b;
            color: white;
        }

        .small-note {
            color: var(--muted);
            font-size: .84rem;
            line-height: 1.45;
        }

        .footer {
            color: var(--muted);
            font-size: .78rem;
            text-align: center;
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Data loading + validation
def validate_columns(dataframe: pd.DataFrame):
    missing = [c for c in REQUIRED_COLUMNS if c not in dataframe.columns]
    return missing


@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def normalize_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    data = dataframe.copy()

    data["rating"] = pd.to_numeric(data["rating"], errors="coerce")
    data["review_word_count"] = pd.to_numeric(
        data["review_word_count"], errors="coerce"
    )
    data["final_cluster"] = pd.to_numeric(
        data["final_cluster"], errors="coerce"
    )

    for col in ["business_name","text_original","rating_category","rating_group","theme", "theme_confidence", "restaurant_type",]:
        data[col] = data[col].astype(str)

    return data


def find_local_data():
    here = Path(__file__).resolve().parent
    for filename in DATA_CANDIDATES:
        candidate = here / filename
        if candidate.exists():
            return candidate
    return None


local_path = find_local_data()

st.sidebar.markdown("## SerafinoSignal")
st.sidebar.caption("Stakeholder exploration dashboard")



if local_path is not None:
    raw_df = load_csv(str(local_path))
    data_source_name = local_path.name
else:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-eyebrow">IAT 461 / Final Project</div>
            <div class="hero-title">SerafinoSignal</div>
            <div class="hero-subtitle">
                The dashboard is ready, but it needs the final review-level export from the notebook.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.error("No final model export was found beside `app.py`.")
    st.markdown(
        """
        Run the export cell supplied with this app. It creates
        **`serafino_reviews.csv`**. Put that file beside `app.py`, then refresh.
        """
    )
    st.stop()

missing_columns = validate_columns(raw_df)
if missing_columns:
    st.error(
        "This CSV is not the final notebook export. Missing columns: "
        + ", ".join(missing_columns)
    )
    st.caption(
        "Use the export cell supplied with this app instead of the original reviews.csv."
    )
    st.stop()

df = normalize_data(raw_df)




# Shared calculations
TOTAL_REVIEWS = len(df)
TOTAL_RESTAURANTS = df["business_name"].nunique()
restaurant_theme_counts = pd.crosstab(df["business_name"],df["theme"],)
restaurant_theme_percent = (restaurant_theme_counts.div(restaurant_theme_counts.sum(axis=1),axis=0,)* 100)
theme_summary = (df.groupby("theme").agg(reviews=("text_original", "count"),restaurants=("business_name", "nunique"),average_rating=("rating", "mean"), median_rating=("rating", "median"), ).reset_index())
theme_summary["coverage_percent"] = (theme_summary["restaurants"] / TOTAL_RESTAURANTS * 100)
rating_group_percent = (
    pd.crosstab(
        df["theme"],
        df["rating_group"],
        normalize="index"
    ) * 100
)
type_restaurant_counts = (df[["business_name", "restaurant_type"]].drop_duplicates()["restaurant_type"].value_counts())
supported_types = [
    restaurant_type
    for restaurant_type in type_restaurant_counts[
        type_restaurant_counts >= 3
    ].index.tolist()
    if restaurant_type != "Other / Unknown"
]


# Global filters
st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")
all_themes = sorted(df["theme"].unique())
all_types = sorted(df["restaurant_type"].unique())
all_restaurants = sorted(df["business_name"].unique())
selected_rating_groups = st.sidebar.multiselect("Rating group",RATING_GROUP_ORDER,default=RATING_GROUP_ORDER,)
selected_themes = st.sidebar.multiselect( "Theme",all_themes,default=all_themes,)

selected_types = st.sidebar.multiselect("Restaurant type",all_types, default=all_types,)
selected_restaurants = st.sidebar.multiselect("Restaurant",all_restaurants,default=[],placeholder="All restaurants",)
filtered = df[
    df["rating_group"].isin(selected_rating_groups)
    & df["theme"].isin(selected_themes)
    & df["restaurant_type"].isin(selected_types)
].copy()

if selected_restaurants:
    filtered = filtered[
        filtered["business_name"].isin(selected_restaurants)
    ].copy()
st.sidebar.markdown("---")
st.sidebar.metric("Visible reviews", f"{len(filtered):,}")
st.sidebar.caption(f"Data source: {data_source_name}")

if filtered.empty:
    st.warning("No reviews match the current filters.")
    st.stop()

# Header
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-eyebrow">IAT 461 - Final Project</div>
        <div class="hero-title">{APP_TITLE}</div>
        <div class="hero-subtitle">
            {APP_SUBTITLE} - turning 1,100 raw reviews into interpretable
            themes, restaurant-level signals, and exploratory restaurant-type patterns.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tabs
overview_tab, themes_tab, restaurants_tab, types_tab = st.tabs(
    ["Executive Overview","Theme Intelligence","Restaurant Drilldown","Restaurant Types",])


# Executive Overview
with overview_tab:
    st.markdown('<div class="section-label">Stakeholder snapshot</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">What is happening across the review platform?</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reviews in dataset", f"{TOTAL_REVIEWS:,}")
    c2.metric("Restaurants", f"{TOTAL_RESTAURANTS:,}")
    c3.metric("Visible average rating", f"{filtered['rating'].mean():.2f}")
    c4.metric(
        "Operational-theme share",
        f"{filtered['theme'].isin(OPERATIONAL_THEMES).mean() * 100:.1f}%",
    )
    st.markdown('<div class="section-label">Operational signals</div>', unsafe_allow_html=True)

    operational_cols = st.columns(4)
    for col, theme in zip(operational_cols, OPERATIONAL_THEMES):
        row = theme_summary[theme_summary["theme"] == theme].iloc[0]

        neg_mixed_share = 0.0
        if theme in rating_group_percent.index:
            for group in ["NEGATIVE (1-2)", "MIXED (3)"]:
                if group in rating_group_percent.columns:
                    neg_mixed_share += rating_group_percent.loc[theme, group]

        col.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-kicker">{theme}</div>
                <div class="insight-value">{int(row['reviews'])} reviews</div>
                <div class="insight-detail">
                    {int(row['restaurants'])} restaurants / {row['coverage_percent']:.0f}% coverage<br>
                    Avg. rating {row['average_rating']:.2f} / {neg_mixed_share:.0f}% negative/mixed
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    left, right = st.columns([1.35, 1])

    with left:
        filtered_theme_counts = (
            filtered["theme"]
            .value_counts()
            .rename_axis("theme")
            .reset_index(name="reviews")
            .sort_values("reviews")
        )

        fig = px.bar(
            filtered_theme_counts,
            x="reviews",
            y="theme",
            orientation="h",
            title="Theme Distribution",
            labels={"reviews": "Reviews", "theme": ""},
            template="plotly_white",
        )
        fig.update_layout(
            height=560,
            margin=dict(l=10, r=10, t=60, b=10),
            title_font_size=18,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        rating_counts = (
            filtered["rating"]
            .value_counts()
            .sort_index()
            .rename_axis("rating")
            .reset_index(name="reviews")
        )

        fig = px.bar(
            rating_counts,
            x="rating",
            y="reviews",
            title="Star Rating Distribution",
            template="plotly_white",
        )
        fig.update_xaxes(dtick=1)
        fig.update_layout(
            height=310,
            margin=dict(l=10, r=10, t=60, b=10),
            title_font_size=18,
        )
        st.plotly_chart(fig, use_container_width=True)

        group_counts = (
            filtered["rating_group"]
            .value_counts()
            .reindex(RATING_GROUP_ORDER)
            .fillna(0)
            .rename_axis("rating_group")
            .reset_index(name="reviews")
        )

        fig = px.bar(
            group_counts,
            x="rating_group",
            y="reviews",
            title="Rating Groups",
            template="plotly_white",
        )
        fig.update_layout(
            height=310,
            margin=dict(l=10, r=10, t=60, b=10),
            title_font_size=18,
            xaxis_title="",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="callout">
            <strong>How to use this dashboard:</strong>
            Treat the themes as signals for outreach and investigation, not as definitive restaurant rankings.
            Each restaurant has only 11 reviews, so one review changes a restaurant-level percentage by about 9.1 points.
        </div>
        """,
        unsafe_allow_html=True,
    )


# Theme 
with themes_tab:
    st.markdown('<div class="section-label">Theme intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Inspect one theme from platform-level pattern to review evidence</div>', unsafe_allow_html=True)
    default_theme = (
        "Waiting Time & Service Friction"
        if "Waiting Time & Service Friction" in all_themes
        else all_themes[0]
    )
    theme = st.selectbox(
        "Theme",
        all_themes,
        index=all_themes.index(default_theme),
        key="theme_detail_select",
    )

    theme_df = df[df["theme"] == theme].copy()
    summary_row = theme_summary[theme_summary["theme"] == theme].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reviews", f"{int(summary_row['reviews']):,}")
    c2.metric("Restaurants", int(summary_row["restaurants"]))
    c3.metric("Restaurant coverage", f"{summary_row['coverage_percent']:.0f}%")
    c4.metric("Average rating", f"{summary_row['average_rating']:.2f}")
    top_rows = []
    if theme in restaurant_theme_percent.columns:
        for restaurant in restaurant_theme_percent.index:
            count = int(restaurant_theme_counts.loc[restaurant, theme])
            if count == 0:
                continue

            share = float(restaurant_theme_percent.loc[restaurant, theme])
            top_rows.append(
                {
                    "Restaurant": restaurant,
                    "Reviews in theme": count,
                    "Theme share (%)": round(share, 1),
                    "Evidence": "Stronger" if count >= 3 else "Limited",
                }
            )

    top_df = (
        pd.DataFrame(top_rows)
        .sort_values(
            ["Theme share (%)", "Reviews in theme"],
            ascending=[False, False],
        )
        .head(12)
    )

    left, right = st.columns([1.25, 1])
    with left:
        chart_data = top_df.sort_values("Theme share (%)")
        fig = px.bar(
            chart_data,
            x="Theme share (%)",
            y="Restaurant",
            orientation="h",
            text="Reviews in theme",
            title="Where This Theme Concentrates",
            template="plotly_white",
        )
        fig.update_layout(
            height=500,
            margin=dict(l=10, r=10, t=60, b=10),
            title_font_size=18,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        profile = (
            theme_df["rating_group"]
            .value_counts()
            .reindex(RATING_GROUP_ORDER)
            .fillna(0)
            .rename_axis("rating_group")
            .reset_index(name="reviews")
        )
        profile["share"] = profile["reviews"] / profile["reviews"].sum() * 100

        fig = px.bar(
            profile,
            x="rating_group",
            y="share",
            text_auto=".1f",
            title="Rating Profile",
            labels={"share": "Share of theme reviews (%)", "rating_group": ""},
            template="plotly_white",
        )
        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=60, b=10),
            title_font_size=18,
        )
        st.plotly_chart(fig, use_container_width=True)

        confidence = theme_df["theme_confidence"].mode().iloc[0]
        st.markdown(
            f"""
            <div class="method-card">
                <strong>Interpretation confidence:</strong> {confidence}<br><br>
                The final label was assigned after inspecting representative reviews,
                cluster keywords, ratings, and restaurant coverage.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Highest-concentration restaurants")
    st.dataframe(
        top_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### Review evidence")
    evidence = (
        theme_df[
            [
                "business_name",
                "rating",
                "rating_group",
                "rating_category",
                "text_original",
            ]
        ]
        .sort_values(["rating", "business_name"])
        .rename(
            columns={
                "business_name": "Restaurant",
                "rating": "Rating",
                "rating_group": "Rating group",
                "rating_category": "Rating category",
                "text_original": "Review",
            }
        )
    )

    st.dataframe(
        evidence.head(25),
        use_container_width=True,
        hide_index=True,
        height=520,
    )


# restaurant Drilldown
with restaurants_tab:
    st.markdown('<div class="section-label">Restaurant drilldown</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">What dominates the available reviews for a single restaurant?</div>', unsafe_allow_html=True)
    chosen_restaurant = st.selectbox("Restaurant",all_restaurants, key="restaurant_select",)

    restaurant_df = df[df["business_name"] == chosen_restaurant].copy()
    theme_counts = restaurant_df["theme"].value_counts()
    dominant_theme = theme_counts.index[0]
    dominant_count = int(theme_counts.iloc[0])
    dominant_share = dominant_count / len(restaurant_df) * 100
    restaurant_type = restaurant_df["restaurant_type"].mode().iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reviews", len(restaurant_df))
    c2.metric("Average rating", f"{restaurant_df['rating'].mean():.2f}")
    c3.metric("Restaurant type", restaurant_type)
    c4.metric("Dominant theme share", f"{dominant_count}/11 ({dominant_share:.1f}%)")

    st.markdown(
        f"""
        <div class="callout">
            <strong>Dominant signal:</strong> {dominant_theme}. 
            This restaurant has {dominant_count} of 11 reviews in that theme.
            Interpret this as a signal to investigate, not a population estimate.
        </div>
        """,
        unsafe_allow_html=True,
    )

    profile = (
        theme_counts.rename_axis("theme")
        .reset_index(name="reviews")
    )
    profile["share"] = profile["reviews"] / len(restaurant_df) * 100

    fig = px.bar(
        profile.sort_values("share"),x="share",y="theme",orientation="h", text="reviews",title=f"Theme Profile - {chosen_restaurant}",labels={"share": "Share of restaurant reviews (%)", "theme": ""},template="plotly_white",
    )
    fig.update_layout(
        height=520,
        margin=dict(l=10, r=10, t=60, b=10),
        title_font_size=18,
    )
    st.plotly_chart(fig, use_container_width=True)

    operational_here = profile[
        profile["theme"].isin(OPERATIONAL_THEMES)
    ].sort_values("reviews", ascending=False)

    if not operational_here.empty:
        st.markdown("#### Operational issues in this restaurant")
        op_table = operational_here.rename(
            columns={
                "theme": "Operational theme",
                "reviews": "Reviews",
                "share": "Share (%)",
            }
        )
        op_table["Share (%)"] = op_table["Share (%)"].round(1)
        st.dataframe(op_table,use_container_width=True, hide_index=True,
        )

    st.markdown("#### All 11 reviews")
    restaurant_reviews = restaurant_df[
        [ "rating", "rating_group", "theme", "text_original"]
    ].rename(
        columns={"rating": "Rating", "rating_group": "Rating group","theme": "Theme","text_original": "Review",})

    st.dataframe(restaurant_reviews, use_container_width=True, hide_index=True,height=520,)

# Restaurant Types
with types_tab:
    st.markdown('<div class="section-label">Exploratory type comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Which operational themes over- or under-index by supported restaurant type?</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="callout">
            Restaurant type is not provided directly by the dataset. It is derived conservatively from
            clear business-name indicators. Only categories represented by at least 3 restaurants are
            shown, and <strong>Other / Unknown</strong> is excluded.
        </div>
        """,
        unsafe_allow_html=True,
    )

    supported_df = df[df["restaurant_type"].isin(supported_types)].copy()
    support_table = (
        supported_df.groupby("restaurant_type")
        .agg(
            Restaurants=("business_name", "nunique"),
            Reviews=("text_original", "count"),
            Average_Rating=("rating", "mean"),
        )
        .reset_index()
        .rename(columns={"restaurant_type": "Restaurant type"})
    )
    support_table["Average_Rating"] = support_table["Average_Rating"].round(2)

    st.dataframe(
        support_table.sort_values("Restaurants", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    type_theme_counts = pd.crosstab(
        supported_df["restaurant_type"],
        supported_df["theme"],
    )

    type_theme_percent = (
        type_theme_counts.div(
            type_theme_counts.sum(axis=1),
            axis=0,
        )
        * 100
    )

    available_operational = [
        t for t in OPERATIONAL_THEMES if t in type_theme_percent.columns
    ]

    operational_percent = type_theme_percent[
        available_operational
    ]

    platform_percent = (
        df["theme"]
        .value_counts(normalize=True)
        .mul(100)
        .reindex(available_operational)
    )

    lift = operational_percent.subtract(
        platform_percent,
        axis="columns",
    )

    selected_operational_theme = st.selectbox(
        "Compare restaurant types for",
        available_operational,
        key="type_theme_select",
    )

    type_comparison = pd.DataFrame(
        {
            "Restaurant type": operational_percent.index,
            "Share of reviews (%)": operational_percent[
                selected_operational_theme
            ].values,
            "Difference from platform (pp)": lift[
                selected_operational_theme
            ].values,
        }
    ).sort_values("Difference from platform (pp)", ascending=False)

    left, right = st.columns([1.2, 1])

    with left:
        fig = px.bar(
            type_comparison,
            x="Restaurant type",
            y="Difference from platform (pp)",
            text_auto=".1f",
            title=f"Over / Under Index - {selected_operational_theme}",
            template="plotly_white",
        )
        fig.add_hline(y=0)
        fig.update_layout(
            height=430,
            margin=dict(l=10, r=10, t=60, b=10),
            title_font_size=18,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### Comparison table")
        display_type_comparison = type_comparison.copy()
        display_type_comparison["Share of reviews (%)"] = (
            display_type_comparison["Share of reviews (%)"].round(1)
        )
        display_type_comparison["Difference from platform (pp)"] = (
            display_type_comparison["Difference from platform (pp)"].round(1)
        )
        st.dataframe(display_type_comparison,use_container_width=True,hide_index=True,)

    st.markdown("Full operational-theme lift matrix")

    fig = px.imshow( lift.round(1), text_auto=".1f", aspect="auto",title="Difference from Platform Average (percentage points)",labels={"x": "Operational theme","y": "Restaurant type","color": "Difference (pp)",},template="plotly_white",)
    fig.update_layout( height=500,margin=dict(l=10, r=10, t=60, b=10),title_font_size=18, )
    st.plotly_chart(fig, use_container_width=True)

    # //**AI Usage: ChatGPT was used as a development assistant to help troubleshoot Python and Streamlit errors, refine dashboard styling UI readability, organize code and suggest fixes for implementation issues. 
    # The project analysis, modeling decisions, interpretation of results, and final design choices were reviewed and implemented by me.