# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_vector_search.py
DESCRIPTION:
    This sample demonstrates how to get search results from a basic search text
    from an Azure Search index.
USAGE:
    python sample_vector_search.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - the endpoint of your Azure Cognitive Search service
    2) AZURE_SEARCH_INDEX_NAME - the name of your search index (e.g. "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - your search API key
"""

import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.models import VectorizedQuery

os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"] = "https://link-tech-cognitive-search.search.windows.net"
os.environ["AZURE_SEARCH_INDEX_NAME"] = "vector-kitei"
os.environ["AZURE_SEARCH_API_KEY"] = "xxx"
os.environ["OpenAIEndpoint"] = "https://link-tech-test-on-your-data-aoai.openai.azure.com/"
os.environ["OpenAIKey"] = "xxx"

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]

def get_embeddings(text: str):
    # There are a few ways to get embeddings. This is just one example.
    import openai

    open_ai_endpoint = os.getenv("OpenAIEndpoint")
    open_ai_key = os.getenv("OpenAIKey")

    client = openai.AzureOpenAI(
        azure_endpoint=open_ai_endpoint,
        api_key=open_ai_key,
        api_version="2023-09-01-preview",
    )
    embedding = client.embeddings.create(input=[text], model="text-embedding-ada-002")
    return embedding.data[0].embedding

def single_vector_search():
    # [START single_vector_search]
    # query = "Top hotels in town"
    # query = "代休について教えて"
    query = "チャットプレイグラウンドについて教えて"

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))
    # vector_query = VectorizedQuery(vector=get_embeddings(query), k_nearest_neighbors=3, fields="descriptionVector")
    vector_query = VectorizedQuery(vector=get_embeddings(query), k_nearest_neighbors=3, fields="vector")

    results = search_client.search(
        vector_queries=[vector_query],
        # select=["hotelId", "hotelName"],
        select=["chunk", "title"],
    )

    for result in results:
        print(result)
    # [END single_vector_search]


def single_vector_search_with_filter():
    # [START single_vector_search_with_filter]
    # query = "Top hotels in town"
    query = "代休について教えて"

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))
    # vector_query = VectorizedQuery(vector=get_embeddings(query), k_nearest_neighbors=3, fields="descriptionVector")
    vector_query = VectorizedQuery(vector=get_embeddings(query), k_nearest_neighbors=3, fields="vector")

    results = search_client.search(
        search_text="",
        vector_queries=[vector_query],
        filter="category eq 'Luxury'", # カテゴリが"Luxury"であるドキュメントのみを結果として取得します。
        # select=["hotelId", "hotelName"],
        select=["chunk", "title"],
    )

    for result in results:
        print(result)
    # [END single_vector_search_with_filter]


def simple_hybrid_search():
    # [START simple_hybrid_search]
    # query = "Top hotels in town"
    query = "代休について教えて"

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))
    # vector_query = VectorizedQuery(vector=get_embeddings(query), k_nearest_neighbors=3, fields="descriptionVector")
    vector_query = VectorizedQuery(vector=get_embeddings(query), k_nearest_neighbors=3, fields="vector")

    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        # select=["hotelId", "hotelName"],
        select=["chunk", "title"],
    )
    print(results.get_answers())
    for result in results:
        print(result)
    # [END simple_hybrid_search]


if __name__ == "__main__":
    credential = AzureKeyCredential(key)
    index_client = SearchIndexClient(service_endpoint, credential)
    client = SearchClient(service_endpoint, index_name, credential)

    single_vector_search()
    # single_vector_search_with_filter() フィルタはいったん使わないでおく。便利そう
    # simple_hybrid_search() ハイブリッドはいったん使わないでおく。
