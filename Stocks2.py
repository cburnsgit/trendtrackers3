import streamlit as st
import feedparser
import pandas as pd
import numpy as np
import requests
import os
import yfinance as yf
import plotly.graph_objects as go
 

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go  # Ensure this is imported

# Sidebar for ETF selection
st.sidebar.write("Select a Sector-Specific ETF")
selected_option = st.sidebar.radio(
    "Select any option",
    options=(
        'XLC for Communication Services',
        'XLY for Consumer Discretionary',
        'XLP for Consumer Staples',
        'XLE for Energy',
        'XLF for Financials',
        'XLV for Health Care',
        'XLI for Industrials',
        'XLK for Information Technology',
        'XLB for Materials',
        'XLRE for Real Estate',
        'XLU for Utilities',
    )
)

# Map ETF options to Yahoo Finance ticker symbols
etf_tickers = {
    'XLC for Communication Services': 'XLC',
    'XLY for Consumer Discretionary': 'XLY',
    'XLP for Consumer Staples': 'XLP',
    'XLE for Energy': 'XLE',
    'XLF for Financials': 'XLF',
    'XLV for Health Care': 'XLV',
    'XLI for Industrials': 'XLI',
    'XLK for Information Technology': 'XLK',
    'XLB for Materials': 'XLB',
    'XLRE for Real Estate': 'XLRE',
    'XLU for Utilities': 'XLU',
}

# Main section
st.title("ETF vs. S&P 500 Dashboard")
st.write(f'You selected: <span style="color:blue;">{selected_option}</span> vs <span style="color:red;">S&P500</span>', unsafe_allow_html=True)


# Get the ticker symbol for the selected ETF and S&P 500
ticker_symbol = etf_tickers[selected_option]
sp500_symbol = "^GSPC"  # Ticker for S&P 500

try:
    # Fetch historical data for the selected ETF and S&P 500
    etf_data = yf.Ticker(ticker_symbol).history(period="1y")
    sp500_data = yf.Ticker(sp500_symbol).history(period="1y")

   

    # Calculate relative performance for both ETF and S&P 500
    etf_data['Relative Performance'] = (etf_data['Close'] / etf_data['Close'].iloc[0] - 1) * 100
    sp500_data['Relative Performance'] = (sp500_data['Close'] / sp500_data['Close'].iloc[0] - 1) * 100







    # Create a multi-line chart using Plotly
    fig = go.Figure()

    # Add ETF relative performance line
    fig.add_trace(
        go.Scatter(
            x=etf_data.index,
            y=etf_data['Relative Performance'],
            mode='lines',
            name=f"{selected_option} Relative Performance",
            line=dict(color='blue'),
        )
    )

    # Add S&P 500 relative performance line
    fig.add_trace(
        go.Scatter(
            x=sp500_data.index,
            y=sp500_data['Relative Performance'],
            mode='lines',
            name="S&P 500 Relative Performance",
            line=dict(color='red'),
        )
    )

    # Customize chart layout
    fig.update_layout(
        title=f"{selected_option} vs. S&P 500 - Relative Performance Comparison",
        xaxis_title="Date",
        yaxis_title="Relative Performance (%)",
        legend=dict(x=0, y=1, traceorder="normal", font=dict(size=12)),
    )

    # Render the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)



     # Calculate the difference in performance

    etf_performance = etf_data['Relative Performance'].iloc[-1]
    sp500_performance = sp500_data['Relative Performance'].iloc[-1]



    performance_diff = etf_performance - sp500_performance

    st.markdown(f"<h3 style='font-size: 24px;'>Sector vs S&P Performance Difference: {performance_diff:.2f}%</h3>", unsafe_allow_html=True)



except Exception as e:
    st.error(f"Failed to fetch data. Error: {e}")


# Start of Google news feed
st.title("Google News: Top 10 Headlines")

# Google News RSS feed URL for the United States in English
rss_url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"

# Parse the feed
st.write("Fetching the latest news from Google News...")
news_feed = feedparser.parse(rss_url)

# Display the top 10 news headlines
if len(news_feed.entries) > 0:
    st.subheader("Top Headlines")
    for entry in news_feed.entries[:10]:  # Limit to the first 10 entries
        st.markdown(f"**{entry.title}**")
        st.markdown(f"[Read more]({entry.link})")
else:
    st.warning("No news articles found. Please try again later.")