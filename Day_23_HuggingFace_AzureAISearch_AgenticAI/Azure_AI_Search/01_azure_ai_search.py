import os
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchableField,
    SimpleField,
    SearchFieldDataType,
)
from dotenv import load_dotenv

# 1. Read the service endpoint and admin key from .env
load_dotenv(Path(__file__).resolve().parent / '.env')
endpoint = os.getenv('AZURE_SEARCH_ENDPOINT', '').strip().rstrip('/')
api_key = os.getenv('AZURE_SEARCH_ADMIN_KEY', '').strip()
index_name = 'resort-faq-demo'

if not endpoint or not api_key:
    raise SystemExit('Set AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_ADMIN_KEY in .env first.')

credential = AzureKeyCredential(api_key)
index_client = SearchIndexClient(endpoint=endpoint, credential=credential)

# 2. Define the index schema and create it if missing
fields = [
    SimpleField(name='id', type=SearchFieldDataType.String, key=True),
    SearchableField(name='title', type=SearchFieldDataType.String),
    SearchableField(name='content', type=SearchFieldDataType.String),
    SimpleField(name='category', type=SearchFieldDataType.String, filterable=True),
]

if index_name not in list(index_client.list_index_names()):
    index_client.create_index(SearchIndex(name=index_name, fields=fields))
    print('Created index:', index_name)
else:
    print('Using existing index:', index_name)

# 3. Sample data (no external document or Blob Storage needed)
documents = [
    {'id': '1', 'title': 'Check-in and Check-out', 'category': 'Stay',
     'content': 'Check-in begins at 2 PM. Check-out is by 11 AM. Early check-in depends on room availability.'},
    {'id': '2', 'title': 'Breakfast', 'category': 'Dining',
     'content': 'Breakfast is served daily from 7 AM to 10 AM. It is included with all room bookings.'},
    {'id': '3', 'title': 'Parking', 'category': 'Facilities',
     'content': 'Free parking is available for guests. One parking space is provided per room.'},
    {'id': '4', 'title': 'Pet Policy', 'category': 'Stay',
     'content': 'Pets are not permitted inside guest rooms. Registered service animals are allowed.'},
    {'id': '5', 'title': 'Cancellation Policy', 'category': 'Booking',
     'content': 'Guests receive a full refund if they cancel at least 48 hours before arrival.'},
]

# 4. Upload records to Azure AI Search
search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
results = search_client.upload_documents(documents=documents)
if not all(r.succeeded for r in results):
    raise RuntimeError('Some documents failed to upload; inspect indexing results.')
print('Uploaded records:', len(results))
print('Search index is ready. Search for breakfast, parking, pets, cancellation, or check-in.')

# 5. Query the search index
while True:
    question = input('\nSearch (or type exit): ').strip()
    if question.lower() == 'exit':
        break
    if not question:
        continue

    matches = search_client.search(search_text=question, top=3)
    print('\nTOP MATCHING DOCUMENTS')
    found = False
    for match in matches:
        found = True
        print('-' * 55)
        print('Title:', match['title'])
        print('Category:', match['category'])
        print('Score:', round(match['@search.score'], 4))
        print('Content:', match['content'])

    if not found:
        print('No matching documents found.')
