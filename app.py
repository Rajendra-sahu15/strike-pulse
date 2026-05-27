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
    
    # Ticker format setup
    if symbol == "NIFTY50":
        ticker_symbol = "^NSEI"
    elif symbol == "BANKNIFTY":
        ticker_symbol = "^NSEBANK"
    elif symbol == "SENSEX":
        ticker_symbol = "^BSESN"
    elif symbol == "FINNIFTY":
        ticker_symbol = "NIFTY_FIN_SERVICE.NS"
    else:
        ticker_symbol = f"{symbol}.NS"
        
    try:
        # Hamesha chalne wala Daily Data (Pichle 1 mahine ka history)
        df = yf.download(ticker_symbol, period="1mo", interval="1d")
        
        if not df.empty:
            # Agar Multi-index columns hain toh unhe simple karein
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            df = df.dropna(subset=['Close'])
            
            fig = go.Figure()
            
            # Base price calculation safely
            base_price = float(df['Close'].iloc[0])
            
            # Line 1 (Strike 1)
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df['Close'] * (strike1 / base_price), 
                mode='lines+markers', # Dots bhi dikhenge
                name=f"Strike {strike1} {option_type1}", 
                line=dict(color='#00FFCC', width=2)
            ))
            
            # Line 2 (Strike 2)
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df['Close'] * (strike2 / base_price), 
                mode='lines+markers', 
                name=f"Strike {strike2} {option_type2}", 
                line=dict(color='#FF3366', width=2)
            ))
            
            fig.update_layout(
                title=f"{symbol} Multi-Strike Trend Chart (Pichle 1 Mahine Ka Daily Data)", 
                xaxis_title="Date", 
                yaxis_title="Value (Scaled)", 
                template="plotly_dark",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Yahoo Finance se data nahi mil pa raha hai. Kripya thodi der baad try karein.")
    except Exception as e:
        st.error(f"Graph banane mein dikkat hui: {e}")

# Disclaimer & Affiliate space
st.markdown("---")
st.caption("⚠️ Disclaimer: Yeh website sirf educational purpose ke liye hai. Hum SEBI registered advisor nahi hain.")
st.sidebar.markdown("---")
st.sidebar.subheader("💰 Free Partner Link")
st.sidebar.markdown("[👉 Open Free Account](#)")
