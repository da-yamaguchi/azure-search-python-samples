# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_simple_query.py
DESCRIPTION:
    This sample demonstrates how to get search results from a basic search text
    from an Azure Search index.
USAGE:
    python sample_simple_query.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_SEARCH_SERVICE_ENDPOINT - the endpoint of your Azure Cognitive Search service
    2) AZURE_SEARCH_INDEX_NAME - the name of your search index (e.g. "hotels-sample-index")
    3) AZURE_SEARCH_API_KEY - your search API key
"""

import os

os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"] = "https://link-tech-cognitive-search.search.windows.net"
os.environ["AZURE_SEARCH_INDEX_NAME"] = "vector-kitei"
os.environ["AZURE_SEARCH_API_KEY"] = "xxx"

service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]


def simple_text_query():
    # [START simple_query]
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient

    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

    results = search_client.search(search_text="代休")

    results = list(results)  # ページング結果をリストに変換
    if results:
        print("chunk: {}".format(results[0]["chunk"]))
        print("title: {}".format(results[0]["title"]))

    # for result in results:
        # print("    Name: {}".format(result["chunk"]))

    # [END simple_query]


if __name__ == "__main__":
    simple_text_query()
