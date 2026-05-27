import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Website ka Title aur Setup
st.set_page_config(page_title="StrikePulse Dashboard", layout="wide")
st.title("📊 StrikePulse: Multi-Strike Options Dashboard")
st.write("Google/Yahoo Finance ke live data ke sath strikes compare karein (Free Beta Version)")

# Sidebar Inputs
st.sidebar.header("🎯 Options Settings")
symbol = st.sidebar.selectbox(
    "Index ya Stock Chuniye", 
    ["NIFTY50", "BANKNIFTY", "FINNIFTY", "SENSEX", "RELIANCE", "SBIN"]
)

# Strike Prices Inputs
strike1 = st.sidebar.number_input("Strike Price 1", value=23000, step=50)
strike2 = st.sidebar.number_input("Strike Price 2", value=24000, step=50)

option_type1 = st.sidebar.selectbox("Type 1", ["CE", "PE"], key="t1")
option_type2 = st.sidebar.selectbox("Type 2", ["CE", "PE"], key="t2")

# Show Graph Button
if st.sidebar.button("Show Graph 📈"):
    st.info("Data fetch ho raha hai... Kripya thoda intezar karein.")
    
    # Ticker format setup (Google/Yahoo common format)
    if symbol == "NIFTY50":
        ticker_symbol = "^NSEI"
    elif symbol == "BANKNIFTY":
        ticker_symbol = "^NSEBANK"
    elif symbol == "SENSEX":
        ticker_symbol = "^BSESN"
    else:
        ticker_symbol = f"{symbol}.NS"
        
    try:
        # Data fetch karna (1 din ka data, 5 minute ki candle)
        df = yf.download(ticker_symbol, period="1d", interval="5m")
        
        if not df.empty:
            fig = go.Figure()
            
            # Line 1 (Strike 1)
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df['Close'] * (strike1 / df['Close'].iloc[0]), 
                mode='lines', 
                name=f"Strike {strike1} {option_type1}", 
                line=dict(color='#00FFCC', width=2) # Neon Color 1
            ))
            
            # Line 2 (Strike 2)
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df['Close'] * (strike2 / df['Close'].iloc[0]), 
                mode='lines', 
                name=f"Strike {strike2} {option_type2}", 
                line=dict(color='#FF3366', width=2) # Neon Color 2
            ))
            
            fig.update_layout(
                title=f"Multi-Strike Comparison Chart", 
                xaxis_title="Time", 
                yaxis_title="Value", 
                template="plotly_dark"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Abhi data available nahi hai. Market hours mein check karein.")
    except Exception as e:
        st.error(f"Data laane mein dikkat hui: {e}")

# Disclaimer & Affiliate space
st.markdown("---")
st.caption("⚠️ Disclaimer: Yeh website sirf educational purpose ke liye hai. Hum SEBI registered advisor nahi hain.")
st.sidebar.markdown("---")
st.sidebar.subheader("💰 Free Partner Link")
st.sidebar.markdown("[👉 Open Free Account](#)")
