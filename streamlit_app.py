import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- Configuration ---
TICKER = "IRCTC.NS"

st.set_page_config(page_title="Live Stock Price Tracker", layout="wide")

st.title("📈 Live Stock Price Tracker")
st.markdown(f"Tracking stock prices for **{TICKER}** using Yahoo Finance.")

# Placeholder for price
price_placeholder = st.empty()
time_placeholder = st.empty()
chart_placeholder = st.empty()

# Store historical data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Date', 'Time', 'Price'])

# Button to clear data
if st.button("Clear Data"):
    st.session_state.data = pd.DataFrame(columns=['Date', 'Time', 'Price'])

# Main loop
while True:
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')

    # Fetch latest price
    stock = yf.Ticker(TICKER)
    data = stock.history(period="1d", interval="1m")

    if not data.empty:
        price = round(data['Close'].iloc[-1], 2)
    else:
        price = None

    if price is not None:
        # Update session state
        new_row = pd.DataFrame({
            'Date': [date_str],
            'Time': [time_str],
            'Price': [price]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

        # Display price
        price_placeholder.metric("Current Price", f"₹{price}")
        time_placeholder.text(f"Last updated at {time_str}")

        # Show line chart
        chart_placeholder.line_chart(st.session_state.data[['Price']])
    else:
        price_placeholder.error("No data available.")

    # Wait before next update
    time.sleep(10)
