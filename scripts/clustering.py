import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
import plotly.express as px


def calculate_centroid(X, Y):
    """
    Given an array of 'x' and 'y' arrays of coordinates, returns the center the figure defined by them
    """
    return np.sum(X) / len(X), np.sum(Y) / len(Y)


def kmeans_elbow_plot(X, k_range):
    """
    Returns the elbow plot of a K-Means model that will be trained by 
    the features in 'X'.

    'k_range' identifies the range number of clusters to use to train the algorithm
    """
    distortions = []
    K = range(k_range[0], k_range[1])

    for cluster_size in K:
        kmeans = KMeans(n_clusters=cluster_size, init='k-means++')
        kmeans = kmeans.fit(X)
        distortions.append(kmeans.inertia_)

    df = pd.DataFrame({'Clusters': K, 'Distortions': distortions})
    fig = (px.line(df, x='Clusters', y='Distortions', template='seaborn')
           ).update_traces(mode='lines+markers')
    fig.show()


def get_clusters(df, model):
    """
    From a given dataframe 'df' and a clustering 'model'
    it trains and returns a numpy array containing the clusters where
    each row in 'df' is assigned to.
    """
    # transforming df features to numpy arrays
    X = df.to_numpy()
    # fit the model
    model.fit(X)
    # assign a cluster to each example
    if hasattr(model, 'predict'):
        clusters = model.predict(X)
    else:
        clusters = model.fit_predict(X)
    print(f'{len(np.unique(clusters))} different clusters have been generated')
    return clusters
