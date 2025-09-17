import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import pytz

# --- Streamlit Config ---
st.set_page_config(page_title="Live Stock Price Tracker", layout="wide")

st.title("📈 Live Stock Price Tracker")

# --- Ticker input ---
ticker = st.text_input("Enter NSE Ticker (e.g., RELIANCE.NS, IRCTC.NS):", "IRCTC.NS")

# Auto-refresh every 10 seconds
st_autorefresh = st_autorefresh(interval=10 * 1000, limit=None)

# Placeholder for price, time, and chart
price_placeholder = st.empty()
time_placeholder = st.empty()
chart_placeholder = st.empty()

# --- Initialize session state for historical data ---
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Time", "Price"])

# --- Clear Data Button ---
if st.button("Clear Data"):
    st.session_state.data = pd.DataFrame(columns=["Date", "Time", "Price"])

# --- Fetch Data ---
try:
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", interval="1m")

    if not data.empty:
        price = round(data["Close"].iloc[-1], 2)

        # Correct IST time
        ist = pytz.timezone("Asia/Kolkata")
        now = datetime.now(ist)
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        # Append new row to session state
        new_row = pd.DataFrame({
            "Date": [date_str],
            "Time": [time_str],
            "Price": [price]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

        # Display price + chart
        price_placeholder.metric("Current Price", f"₹{price}")
        time_placeholder.text(f"Last updated at {time_str} IST")
        chart_placeholder.line_chart(st.session_state.data["Price"])
    else:
        price_placeholder.error("No data available for this ticker.")

except Exception as e:
    st.error(f"Error fetching data: {e}")

# --- CSV Download ---
if not st.session_state.data.empty:
    csv = st.session_state.data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{ticker}_live_data.csv",
        mime="text/csv"
    )
