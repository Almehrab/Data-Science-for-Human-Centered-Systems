import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
st.set_page_config(page_title="Vancouver Business Similarity Explorer",layout="wide")
@st.cache_data
def load_data():
    composition = pd.read_csv("clean_area_composit.csv",index_col=0)
    summary = pd.read_csv("clean_area_summary.csv",index_col=0)
    composition = composition.apply(pd.to_numeric,errors="coerce")
    summary["business_count"] = pd.to_numeric(summary["business_count"],errors="coerce")
    summary["latitude"] = pd.to_numeric(summary["latitude"],errors="coerce")
    summary["longitude"] = pd.to_numeric(summary["longitude"], errors="coerce")
    composition = composition.fillna(0)
    summary = summary.dropna(
        subset=["business_count","latitude","longitude"])
    common_areas = composition.index.intersection(summary.index)
    composition = composition.loc[common_areas]
    summary = summary.loc[common_areas]
    return composition, summary
area_composition, area_summary = load_data()

st.title("Vancouver Business Similarity")
st.write("Explore which Vancouver neighbourhoods have similar business ")


# sidebar
st.sidebar.title("Controls")
max_clusters = min(8,len(area_composition) - 1)
k = st.sidebar.slider("Number of clusters",min_value=2,max_value=max_clusters,value=min(4, max_clusters),help=(
        "Choose how many groups K-means should create "
        " visualizations update automatically"))

st.sidebar.markdown("---")
st.sidebar.write("Neighbourhoods are compared using the percentage of businesses""belonging to each business type")
kmeans = KMeans(n_clusters=k,random_state=42,n_init=10)
cluster_labels = kmeans.fit_predict(area_composition)
pca = PCA(n_components=2,random_state=42)
pca_values = pca.fit_transform(area_composition)
results = area_summary.copy()
results["cluster"] = cluster_labels
results["cluster_label"] = ("Cluster " + results["cluster"].astype(str))
results["PC1"] = pca_values[:, 0]
results["PC2"] = pca_values[:, 1]
results["neighbourhood"] = results.index
results = results.sort_values(["cluster", "business_count"],ascending=[True, False])
col1, col2, col3, col4 = st.columns(4)
col1.metric("Neighbourhoods",len(results))
col2.metric("Business Types",area_composition.shape[1])
col3.metric("Selected Clusters",k)
col4.metric("PCA Variance",f"{pca.explained_variance_ratio_.sum():.1%}")

#  navigation tabs
tab1, tab2, tab3, tab4 = st.tabs([ " Geographic Map","PCA Similarity"," Cluster Membership","Data Explorer"])
with tab1:
    st.subheader("Geographic Cluster Map")
    st.write("Each point represents a neighbourhood. Point size shows the ""number of business licences, while colour shows cluster membership.")
    map_figure = px.scatter_map(results,lat="latitude",lon="longitude",color="cluster_label",size="business_count",hover_name="neighbourhood", hover_data={
            "cluster_label": True,"business_count": ":,","latitude": False,"longitude": False},zoom=10,height=650,size_max=45,labels={"cluster_label": "Cluster","business_count": "Businesses"})
    map_figure.update_layout(margin={"r": 0,"t": 10,"l": 0,"b": 0},legend_title_text="Cluster")
    st.plotly_chart(map_figure,use_container_width=True)
with tab2:
    st.subheader("PCA View of Business Similarity")
    st.write("neighbourhoods positioned close together have more similar ""business type compositions.")
    pca_figure = px.scatter(results,x="PC1",y="PC2",color="cluster_label",size="business_count",hover_name="neighbourhood",hover_data={"cluster_label": True,"business_count": ":,","PC1": ":.2f","PC2": ":.2f" },
        size_max=45,
        labels={"PC1": "Principal Component 1","PC2": "Principal Component 2","cluster_label": "Cluster", "business_count": "Businesses"})
    pca_figure.update_traces(marker={"opacity": 0.8,"line": {"width": 1}})
    pca_figure.update_layout(height=650,legend_title_text="Cluster")
    st.plotly_chart(pca_figure,use_container_width=True)
    st.info(f"The first two principal components explain "f"{pca.explained_variance_ratio_.sum():.1%} ""of the variation in neighbourhood business composition.")
with tab3:
    st.subheader("Cluster Membership")
    cluster_summary = (results.groupby("cluster_label").agg(neighbourhoods=("neighbourhood", "count"),total_businesses=("business_count", "sum"),average_businesses=("business_count", "mean")).round(1).reset_index())
    st.dataframe(cluster_summary,use_container_width=True,hide_index=True,column_config={"cluster_label": "Cluster","neighbourhoods": "Neighbourhoods","total_businesses": st.column_config.NumberColumn("Total Businesses",format="%d"),
            "average_businesses": st.column_config.NumberColumn("Average Businesses",format="%.1f")})
    st.markdown("---")
    for cluster_number in sorted( results["cluster"].unique()):
        cluster_rows = results[results["cluster"] == cluster_number][
            ["neighbourhood","business_count"]]
        with st.expander( f"Cluster {cluster_number} "f"- {len(cluster_rows)} neighbourhoods"):
            st.dataframe(cluster_rows,use_container_width=True,hide_index=True,column_config={ "neighbourhood": "Neighbourhood","business_count": st.column_config.NumberColumn("Businesses",format="%d")})

with tab4:
    st.subheader("Neighbourhood Cluster Data")
    selected_clusters = st.multiselect("Filter by cluster",options=sorted(results["cluster"].unique()),default=sorted(results["cluster"].unique()))
    filtered_results = results[results["cluster"].isin(selected_clusters)]
    display_columns = ["neighbourhood","cluster_label","business_count","PC1","PC2"]
    st.dataframe(filtered_results[display_columns],use_container_width=True, hide_index=True, column_config={"neighbourhood": "Neighbourhood","cluster_label": "Cluster","business_count": st.column_config.NumberColumn("Businesses",format="%d"),"PC1": st.column_config.NumberColumn("PC1",format="%.2f"),
            "PC2": st.column_config.NumberColumn("PC2",format="%.2f")})
    csv_data = filtered_results[display_columns].to_csv( index=False)
    st.download_button(label="Download Cluster Assignments",data=csv_data,file_name="vancouver_neighbourhood_clusters.csv", mime="text/csv")

    ## Used Personal Access Token to download data from GitHub. The token is stored in a .env file and accessed using the os module. This is a secure way to handle sensitive information like access tokens.
    # used Perplixity to polish UI and Code. It helped to make the code more readable and maintainable, and also suggested improvements to the UI for better user experience.
    