# 📊 Live Order Book Visualizer

This project is a real-time financial order book simulator and visualizer built using **Streamlit**. It allows users to:

- Place manual buy/sell limit orders
- Visualize top bid and ask levels dynamically
- Monitor a trade execution log
- Run a background simulator that mimics live market behavior

---

## 🚀 Features

- 🧾 Manual order input (side, price, quantity)
- 🔁 Live simulation of random buy/sell limit orders
- 📈 Real-time visualization of top bid/ask levels
- 💥 Execution log of matched trades
- 🧠 Session state management using Streamlit

---

## ⚙️ Requirements

- Python 3.7+
- Streamlit
- Pandas
- sortedcontainers


▶️ How to Run

Clone the repository or download the code.

Make sure all dependencies are installed.

Run the app with:

streamlit run main.py

The app will open in your browser. You can:

Toggle the simulator on/off from the sidebar.

Place manual orders.

View the order book and recent trades.

🧪 Example Usage
Place a Buy order at 99.5 for 50 units.

Observe how it matches with existing sell orders if prices align.

Enable the simulator to observe a stream of market-like orders.

📌 Notes
Orders are matched using price-time priority.

The order book depth is limited to the top 5 bid/ask levels.

The trade log shows the last 20 matched trades.

