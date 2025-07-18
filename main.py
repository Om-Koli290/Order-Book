import streamlit as st
import pandas as pd
import time

from Orderbook import OrderBook
from Simulator import simulate_random_orders

# --- Setup ---
st.set_page_config(layout="wide")
st.title("📊 Live Order Book Visualizer")

# Initialize session state for order book
if "orderbook" not in st.session_state:
    st.session_state.orderbook = OrderBook()

orderbook = st.session_state.orderbook

# --- Optional: Background simulation ---
with st.sidebar:
    st.header("⚙️ Simulator Settings")
    simulate = st.checkbox("Run Simulated Orders", value=True)
    n_orders = st.slider("Orders per refresh", 0, 10, 2)
    if simulate:
        simulate_random_orders(orderbook, n_orders)

# --- User Order Input ---
st.sidebar.header("📥 Place Your Own Order")
side = st.sidebar.selectbox("Side", ["buy", "sell"])
price = st.sidebar.number_input("Price", min_value=1.0, step=0.5)
quantity = st.sidebar.number_input("Quantity", min_value=1, step=1)
submit = st.sidebar.button("Submit Order")

if submit:
    orderbook.place_limit_order(side=side, price=price, quantity=quantity)
    st.sidebar.success("Order submitted!")

# --- Order Book Display ---
st.subheader("📈 Order Book")
col1, col2 = st.columns(2)

# Buy side (bids)
bids = pd.DataFrame(orderbook.get_book_snapshot()[0], columns=["Price", "Quantity"])
if not bids.empty:
    bids = bids.sort_values(by="Price", ascending=False)
col1.write("### 🟢 Bids")
col1.dataframe(bids, use_container_width=True)

# Sell side (asks)
asks = pd.DataFrame(orderbook.get_book_snapshot()[1], columns=["Price", "Quantity"])
if not asks.empty:
    asks = asks.sort_values(by="Price", ascending=True)
col2.write("### 🔴 Asks")
col2.dataframe(asks, use_container_width=True)

# --- Trade Log ---
st.subheader("💥 Executed Trades")
trade_log = orderbook.get_trade_log()
if trade_log:
    trades_df = pd.DataFrame(trade_log)
    trades_df["timestamp"] = pd.to_datetime(trades_df["timestamp"], unit='s')
    st.dataframe(trades_df.sort_values("timestamp", ascending=False), use_container_width=True)
else:
    st.info("No trades have been executed yet.")

