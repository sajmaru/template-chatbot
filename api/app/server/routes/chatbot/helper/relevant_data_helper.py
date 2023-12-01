"""
This script takes the user query and converts it into vectors/embeddings using the same model the usedd to embedd training data.
It employs a TF-IDF (Term Frequency-Inverse Document Frequency) vectorizer to process text queries and utilizes cosine similarity to assess the relevance of file chunks to these queries.

Key Components:
- TfidfVectorizer_model: A machine learning model loaded from a GCP bucket, used to transform text queries into a vectorized format.
- metadata_embeddings: Pre-computed embeddings for doc metadata, used to compare against the query vector for relevance.
- find_most_relevant_docs: A function that takes a user query, processes it through the TF-IDF model, and then computes similarity scores with doc metadata to find the most relevant docs.
- get_relevant_docs: A function that prepares the contextual information about relevant docs based on the user's query keywords.

Usage:
1. Load the TF-IDF model and metadata embeddings from a GCP bucket.
2. Use `find_most_relevant_docs` to find the indices of the most relevant docs based on the user's query.
3. Use `get_relevant_docs` to construct a detailed response containing information about these relevant docs.

Dependencies:
- numpy and sklearn: Used for mathematical operations and machine learning processes.
- pickle: For loading the pre-trained model and embeddings.
- custom modules from 'app.server.routes.data_finder.helper': These might contain specific utilities for data handling and processing relevant to the application's architecture.
"""
############################################################

import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .data_helper import *

blob = read_from_bucket('template-chatbot', 'Models/TfidfVectorizer_model.pkl')
TfidfVectorizer_model = pickle.loads(blob.download_as_string(client=None))

blob = read_from_bucket('template-chatbot', 'Embeddings/Tfidf_embeddings.pkl')
embeddings = pickle.loads(blob.download_as_string(client=None))

def find_most_relevant_docs(query, top_n=3):
    # Preprocess the query into a vector
    query_embedding = TfidfVectorizer_model.transform([query])

    # Compute cosine similarities between the query and doc metadata
    cosine_similarities = cosine_similarity(query_embedding, embeddings).flatten()

    # Sort docs by similarity scores and select top N
    top_indices = np.argsort(cosine_similarities)[::-1][:top_n]

    return top_indices

def get_relevant_docs(query_keywords, data):
    # Retrieve indices of related docs based on the query
    relevant_docs = find_most_relevant_docs(query_keywords)

    # Prepare context for prompt by aggregating information from relevant docs
    context = "\n".join([str(data[doc]) for doc in relevant_docs])    
    
    return context
