# use the elasticsearch client's helpers class for _bulk API
from elasticsearch import Elasticsearch, helpers
from elasticsearch.client import IndicesClient
import pandas as pd

# Instantiate a client instance
es = Elasticsearch("http://absolute_zero:guessthissucker@localhost:9200")

# CHECKING FOR DUPLICATE ENTRIES MANUALLY
# REMOVING DUPLICATE CONTENT IF ANY

df = pd.read_json("C:/Users/srich/Downloads/nvd.json")

if(df.title.value_counts()[0] > 1):
    df_new = df.drop_duplicates(subset=['title'])

# INDEXING VALUES

mappings = {
    "mappings": {
        "properties": {
            "title": {
                "type": "keyword",
            },
            "desc": {
                "type": "text",
            },
            "modified": {
                "type": "date"
            },
            "published": {
                "type": "date"
            },
            "severity_cvss_2": {
                "type": "text",
                "index": 'false',
            },
            "severity_cvss_3": {
                "type": "text",
                "index": 'false',
            },
            "cwe_links": {
                "type": "text",
            },
            "further_details": {
                "type": "text",
                "index": 'false',
            },
            "warning": {
                "type": "text",
                "index": 'false',
            },
        }
    }
}

# DeprecationWarning: The 'body' parameter is deprecated for the 'create' API and will be removed in a future version.
# Use mappings=mappings in the future version (replace body with mappings)
es.indices.create(index='nvd_index', body=mappings, ignore=400)

for i in df_new.values:
    doc = dict(zip(df_new.columns, i))
    es.index(index = 'nvd_index', id = doc['title'], doc_type="_doc", document = doc)

# changing max results shown

index_client = IndicesClient(es)
index_client.put_settings(body={
    'index.max_result_window': 1000000
})