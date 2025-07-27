import os
import streamlit as st
import requests
import plotly.graph_objects as go
import collections
import random
from datetime import datetime, timedelta

# Read environment variables
DUNE_API_KEY = os.getenv('DUNE_API_KEY')
DUNE_QUERY_ID = os.getenv('DUNE_QUERY_ID')

# Custom CSS for dark black font without shadow
st.markdown("""
<style>
    .main .block-container h1 {
        color: #000000 !important;
        text-shadow: none !important;
        font-weight: bold !important;
    }
    .stSelectbox label {
        color: #000000 !important;
        text-shadow: none !important;
        font-weight: bold !important;
    }
    .stSubheader {
        color: #000000 !important;
        text-shadow: none !important;
        font-weight: bold !important;
    }
    /* Override any Plotly text styling */
    .plotly .sankey text {
        fill: #000000 !important;
        stroke: none !important;
        text-shadow: none !important;
        font-weight: bold !important;
    }
</style>
<script>
// Remove any undefined text
function removeUndefined() {
    const elements = document.querySelectorAll('*');
    elements.forEach(element => {
        if (element.textContent && element.textContent.includes('undefined')) {
            element.textContent = element.textContent.replace(/undefined/g, '');
        }
    });
}
// Run on page load and periodically
document.addEventListener('DOMContentLoaded', removeUndefined);
setInterval(removeUndefined, 1000);
</script>
""", unsafe_allow_html=True)

st.title('CryptoFlow')

if not DUNE_API_KEY:
    st.error('DUNE_API_KEY must be set as environment variable.')
    st.stop()

# Dune API endpoints for both queries
DUNE_API_URL_YESTERDAY = f"https://api.dune.com/api/v1/query/5539788/results"  # Yesterday (2 days ago)
DUNE_API_URL_TODAY = "https://api.dune.com/api/v1/query/5536308/results"  # Today (last day)

headers = {
    'x-dune-api-key': DUNE_API_KEY
}

def fetch_dune_data(query_url):
    response = requests.get(query_url, headers=headers)
    if response.status_code != 200:
        st.error(f"Failed to fetch data from Dune API: {response.status_code}")
        st.stop()
    data = response.json()
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

# Fetch data from both APIs
rows_yesterday = fetch_dune_data(DUNE_API_URL_YESTERDAY)
rows_today = fetch_dune_data(DUNE_API_URL_TODAY)

# Display data summary
total_volume_yesterday = sum(row['value'] for row in rows_yesterday)
total_volume_today = sum(row['value'] for row in rows_today)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Volume (USD) - Yesterday", f"${total_volume_yesterday:,.0f}")
with col2:
    st.metric("Total Volume (USD) - Today", f"${total_volume_today:,.0f}")

# Calculate percentage change
if total_volume_yesterday > 0:
    volume_change = ((total_volume_today - total_volume_yesterday) / total_volume_yesterday) * 100
    st.metric("Volume Change (%)", f"{volume_change:.1f}%", delta=f"{volume_change:.1f}%")

st.info(f"Yesterday: {len(rows_yesterday)} flows | Today: {len(rows_today)} flows")

# Get all unique tokens for selection
tokens = sorted(set([row['source'] for row in rows_yesterday] + [row['target'] for row in rows_yesterday] +
                    [row['source'] for row in rows_today] + [row['target'] for row in rows_today]))
# Set ETH as default if available, otherwise use first token
default_token = "ETH" if "ETH" in tokens else tokens[0] if tokens else "ETH"
selected_token = st.selectbox("Select a token to view flows:", tokens, index=tokens.index(default_token) if default_token in tokens else 0)

# Calculate metrics for selected token
inflow_volume_yesterday = sum(row['value'] for row in rows_yesterday if row['target'] == selected_token)
outflow_volume_yesterday = sum(row['value'] for row in rows_yesterday if row['source'] == selected_token)

inflow_volume_today = sum(row['value'] for row in rows_today if row['target'] == selected_token)
outflow_volume_today = sum(row['value'] for row in rows_today if row['source'] == selected_token)

col1, col2 = st.columns(2)
with col1:
    st.metric(f"Inflow to {selected_token} - Yesterday", f"${inflow_volume_yesterday:,.0f}")
    st.metric(f"Inflow to {selected_token} - Today", f"${inflow_volume_today:,.0f}")
    if inflow_volume_yesterday > 0:
        inflow_change = ((inflow_volume_today - inflow_volume_yesterday) / inflow_volume_yesterday) * 100
        st.metric("Inflow Change (%)", f"{inflow_change:.1f}%", delta=f"{inflow_change:.1f}%")
with col2:
    st.metric(f"Outflow from {selected_token} - Yesterday", f"${outflow_volume_yesterday:,.0f}")
    st.metric(f"Outflow from {selected_token} - Today", f"${outflow_volume_today:,.0f}")
    if outflow_volume_yesterday > 0:
        outflow_change = ((outflow_volume_today - outflow_volume_yesterday) / outflow_volume_yesterday) * 100
        st.metric("Outflow Change (%)", f"{outflow_change:.1f}%", delta=f"{outflow_change:.1f}%")

# Show comparison for selected token
st.subheader(f"Flow Comparison for {selected_token}")

# Get flows where selected_token is target (inflows)
inflow_rows_yesterday = [row for row in rows_yesterday if row['target'] == selected_token]
inflow_rows_yesterday = sorted(inflow_rows_yesterday, key=lambda x: x['value'], reverse=True)[:10]

inflow_rows_today = [row for row in rows_today if row['target'] == selected_token]
inflow_rows_today = sorted(inflow_rows_today, key=lambda x: x['value'], reverse=True)[:10]

if inflow_rows_yesterday or inflow_rows_today:
    st.write(f"**Top Inflows to {selected_token}**")
    
    # Nice color palette
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    # Create separate charts for yesterday and today
    if inflow_rows_yesterday:
        st.write("**Yesterday's Inflows**")
        label_list, source_indices, target_indices, values = build_sankey_data(inflow_rows_yesterday)
        node_colors = [colors[i % len(colors)] for i in range(len(label_list))]

        fig_yesterday = go.Figure(data=[go.Sankey(
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

        fig_yesterday.update_layout(
            font=dict(color="black", size=14),
            title_font_color="black",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig_yesterday.update_traces(textfont=dict(color="black"))
        st.plotly_chart(fig_yesterday, use_container_width=True)

    if inflow_rows_today:
        st.write("**Today's Inflows**")
        label_list, source_indices, target_indices, values = build_sankey_data(inflow_rows_today)
        node_colors = [colors[i % len(colors)] for i in range(len(label_list))]

        fig_today = go.Figure(data=[go.Sankey(
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

        fig_today.update_layout(
            font=dict(color="black", size=14),
            title_font_color="black",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig_today.update_traces(textfont=dict(color="black"))
        st.plotly_chart(fig_today, use_container_width=True)
else:
    st.warning(f"No inflows to {selected_token} found in the data for both periods.")

# Get flows where selected_token is source (outflows)
outflow_rows_yesterday = [row for row in rows_yesterday if row['source'] == selected_token]
outflow_rows_yesterday = sorted(outflow_rows_yesterday, key=lambda x: x['value'], reverse=True)[:10]

outflow_rows_today = [row for row in rows_today if row['source'] == selected_token]
outflow_rows_today = sorted(outflow_rows_today, key=lambda x: x['value'], reverse=True)[:10]

if outflow_rows_yesterday or outflow_rows_today:
    st.write(f"**Top Outflows from {selected_token}**")
    
    # Nice color palette for outflows
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    # Create separate charts for yesterday and today
    if outflow_rows_yesterday:
        st.write("**Yesterday's Outflows**")
        label_list, source_indices, target_indices, values = build_sankey_data(outflow_rows_yesterday)
        node_colors = [colors[i % len(colors)] for i in range(len(label_list))]

        fig_yesterday = go.Figure(data=[go.Sankey(
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

        fig_yesterday.update_layout(
            font=dict(color="black", size=14),
            title_font_color="black",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig_yesterday.update_traces(textfont=dict(color="black"))
        st.plotly_chart(fig_yesterday, use_container_width=True)

    if outflow_rows_today:
        st.write("**Today's Outflows**")
        label_list, source_indices, target_indices, values = build_sankey_data(outflow_rows_today)
        node_colors = [colors[i % len(colors)] for i in range(len(label_list))]

        fig_today = go.Figure(data=[go.Sankey(
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

        fig_today.update_layout(
            font=dict(color="black", size=14),
            title_font_color="black",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig_today.update_traces(textfont=dict(color="black"))
        st.plotly_chart(fig_today, use_container_width=True)
else:
    st.warning(f"No outflows from {selected_token} found in the data for both periods.") 