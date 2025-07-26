import os
import streamlit as st
import requests
import plotly.graph_objects as go
import collections
import random

# Read environment variables
DUNE_API_KEY = os.getenv('DUNE_API_KEY')
DUNE_QUERY_ID = os.getenv('DUNE_QUERY_ID')

st.title('CryptoFlow')

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

# Get all unique tokens for selection
tokens = sorted(set([row['source'] for row in rows] + [row['target'] for row in rows]))
# Set ETH as default if available, otherwise use first token
default_token = "ETH" if "ETH" in tokens else tokens[0] if tokens else "ETH"
selected_token = st.selectbox("Select a token to view inflows/outflows:", tokens, index=tokens.index(default_token) if default_token in tokens else 0)

# Inflows: where selected_token is the target
inflow_rows = [row for row in rows if row['target'] == selected_token]
if inflow_rows:
    st.subheader(f"Inflows to {selected_token}")
    label_list, source_indices, target_indices, values = build_sankey_data(inflow_rows)

    # Nice color palette
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    # Cycle through colors
    node_colors = [colors[i % len(colors)] for i in range(len(label_list))]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=label_list,
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            color=node_colors
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values
        )
    )])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info(f"No inflows to {selected_token} found.")

# Outflows: where selected_token is the source
outflow_rows = [row for row in rows if row['source'] == selected_token]
if outflow_rows:
    st.subheader(f"Outflows from {selected_token}")
    label_list, source_indices, target_indices, values = build_sankey_data(outflow_rows)

    # Color the links based on source node
    link_colors = [node_colors[source_indices[i]] for i in range(len(source_indices))]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=label_list,
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            color=node_colors
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=link_colors  # Add colorful links
        )
    )])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info(f"No outflows from {selected_token} found.") 