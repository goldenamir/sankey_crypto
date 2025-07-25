import os
import streamlit as st
import requests
import plotly.graph_objects as go

# Read environment variables
DUNE_API_KEY = os.getenv('DUNE_API_KEY')
DUNE_QUERY_ID = os.getenv('DUNE_QUERY_ID')

st.title('Crypto Coin-to-Coin Volume Flows (Sankey)')

if not DUNE_API_KEY or not DUNE_QUERY_ID:
    st.error('DUNE_API_KEY and DUNE_QUERY_ID must be set as environment variables.')
    st.stop()

# Dune API endpoint
DUNE_API_URL = f"https://api.dune.com/api/v1/query/{DUNE_QUERY_ID}/results"

headers = {
    'x-dune-api-key': DUNE_API_KEY
}

def fetch_dune_data():
    response = requests.get(DUNE_API_URL, headers=headers)
    if response.status_code != 200:
        st.error(f"Failed to fetch data from Dune API: {response.status_code}")
        st.stop()
    data = response.json()
    # Expecting data['result']['rows'] to be a list of dicts with 'source', 'target', 'volume'
    return data['result']['rows']

def build_sankey_data(rows):
    sources = []
    targets = []
    values = []
    labels = set()
    for row in rows:
        sources.append(row['source'])
        targets.append(row['target'])
        values.append(row['value'])
        labels.add(row['source'])
        labels.add(row['target'])
    label_list = list(labels)
    label_map = {label: i for i, label in enumerate(label_list)}
    source_indices = [label_map[s] for s in sources]
    target_indices = [label_map[t] for t in targets]
    return label_list, source_indices, target_indices, values

rows = fetch_dune_data()
label_list, source_indices, target_indices, values = build_sankey_data(rows)

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=label_list
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values
    )
)])

fig.update_layout(title_text="Coin-to-Coin Volume Flows", font_size=10)
st.plotly_chart(fig, use_container_width=True) 