# CryptoFlow - Crypto Volume Flow Visualization

A Python Streamlit web application that visualizes coin-to-coin crypto volume flows using data from the Dune Analytics API. The app presents Sankey diagrams showing inflows and outflows for selected tokens, with comparison between different time periods.

## 🚀 Features

- **Sankey Diagram Visualization**: Interactive flow diagrams showing crypto volume movements
- **Time Period Comparison**: Compare volume flows between yesterday and today
- **Token Selection**: Choose any token to analyze its inflows and outflows
- **Volume Metrics**: Real-time calculations of total volume and percentage changes
- **Colorful Visualization**: Beautiful color-coded nodes and flows
- **Responsive Design**: Works on desktop and mobile devices

## 📊 Data Sources

The app fetches data from two Dune Analytics queries:
- **Yesterday's Data**: Query ID `5539788` (2 days ago volume data)
- **Today's Data**: Query ID `5536308` (last day volume data)

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- Dune Analytics API key

### Environment Variables

Create a `.env` file in the project root:

```env
DUNE_API_KEY=your_dune_api_key_here
DUNE_QUERY_ID=5539788
```

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd sankey_crypto
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**:
   ```bash
   export DUNE_API_KEY=your_api_key_here
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and go to `http://localhost:8501`

### Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Access the app** at `http://localhost:8501`

## 📈 Usage

1. **Select a Token**: Use the dropdown to choose any cryptocurrency token
2. **View Metrics**: See total volume, inflow/outflow volumes, and percentage changes
3. **Analyze Flows**: Examine Sankey diagrams showing:
   - **Yesterday's Inflows**: Top sources flowing into the selected token
   - **Today's Inflows**: Current day's inflow patterns
   - **Yesterday's Outflows**: Where the token flowed to yesterday
   - **Today's Outflows**: Current day's outflow patterns

## 🏗️ Project Structure

```
sankey_crypto/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose orchestration
├── README.md            # This file
└── .env                 # Environment variables (create this)
```

## 🔧 Configuration

### Dune Analytics API

1. **Get API Key**: Sign up at [Dune Analytics](https://dune.com)
2. **Create Queries**: Set up queries for different time periods
3. **Update Query IDs**: Modify the query IDs in `app.py` if needed

### Customization

- **Color Palette**: Modify the `colors` array in `app.py`
- **Flow Limits**: Change the `[:10]` slice to show more/fewer flows
- **Time Periods**: Update the query IDs for different time ranges

## 🚀 Deployment Options

### Streamlit Community Cloud
1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets for `DUNE_API_KEY`
4. Deploy

### Render.com
1. Connect GitHub repository
2. Set environment variables
3. Deploy as web service

### Railway.app
1. Import from GitHub
2. Set environment variables
3. Deploy

## 📊 Data Schema

The app expects Dune query results with the following structure:
```json
{
  "result": {
    "rows": [
      {
        "day": "2025-01-27",
        "source": "USDC",
        "target": "ETH",
        "value": 1234567.89
      }
    ]
  }
}
```

## 🎨 Features

- **Real-time Data**: Fetches live data from Dune Analytics
- **Interactive Charts**: Hover for details, zoom, and pan
- **Responsive Layout**: Works on all screen sizes
- **Dark Text**: Clean, readable labels without shadows
- **Volume Comparison**: Side-by-side analysis of time periods

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

---

**Built with ❤️ using Streamlit, Plotly, and Dune Analytics**