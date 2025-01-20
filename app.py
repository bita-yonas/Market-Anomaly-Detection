import streamlit as st
import pandas as pd
import numpy as np
import openai
import os
import yfinance as yf
from datetime import datetime
import joblib  # To load the saved model

openai.api_key = os.getenv("OPENAI_API_KEY")


model = joblib.load('investment_strategy_model.pkl')  

# Fetch market data (e.g., VIX, S&P 500)
def fetch_market_data():
    tickers = ['^VIX', '^GSPC']
    market_data = {}
    market_data['timestamp'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S EST")
    
    for ticker in tickers:
        try:
            ticker_data = yf.Ticker(ticker)
            history = ticker_data.history(period="1d")
            market_data[ticker] = history["Close"].iloc[-1]
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
            market_data[ticker] = None
    
    return market_data

# Predict market crash likelihood based on VIX and S&P 500
def market_crash_prediction(vix, sp500):
    features = np.array([vix, sp500]).reshape(1, -1)  # Model expects a 2D array for prediction
    prediction = model.predict(features)  # Predict crash (1 for crash, 0 for no crash)
    
    if prediction == 1:
        return "Market Crash Likely"
    else:
        return "Market is Stable"

# Generate investment strategy using Groq's Llama model
def generate_investment_strategy(vix, sp500):
    context = f"Based on the market data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\nVIX: {vix}\nS&P 500: {sp500}\nWhat is a recommended investment strategy?"

    response = openai.Completion.create(
        model="llama-3.1-8b-instant",  
        prompt=context,
        max_tokens=150
    )

    return response.choices[0].text.strip()

# Generate a more detailed explanation using the Groq's Llama model
def generate_explanation(strategy, user_question):
    context = f"Explain the investment strategy '{strategy}' in simple terms. {user_question}"

    response = openai.Completion.create(
        model="llama-3.1-8b-instant",  # Using Groq's Llama model
        prompt=context,
        max_tokens=200
    )
    
    return response.choices[0].text.strip()

# Streamlit UI configuration
st.set_page_config(page_title="Investment Strategy Bot", page_icon="💹")

# App title and sidebar info
st.title("💹 Market Crash Detector & Investment Strategy Bot")
st.sidebar.header("How it works")
st.sidebar.write("""
    This bot provides personalized investment strategy recommendations based on current market data (VIX, S&P500).
    Ask me about the market, and I'll suggest strategies based on real-time data like VIX and S&P500.
""")

# Prediction and Strategy Section
st.write("### Prediction and Strategy")
    
market_data = fetch_market_data()  # Fetch real-time market data

if market_data['^VIX'] is None or market_data['^GSPC'] is None:
    st.error("Error fetching market data. Please try again later.")
else:
    vix = market_data['^VIX']
    sp500 = market_data['^GSPC']

    # Make prediction and generate strategy
    market_condition = market_crash_prediction(vix, sp500)
    prediction_label = market_condition
    strategy = "Minimize exposure to high-risk assets" if market_condition == "Market Crash Likely" else "Optimize for growth"

    st.write(f"**Prediction:** {prediction_label}")
    st.write(f"**Investment Strategy:** {strategy}")

# AI-Driven Bot for Strategy Explanation
st.write("### Ask the Bot")
user_question = st.text_input("Ask about the investment strategy or market conditions:")

if user_question:
    response = generate_explanation(strategy, user_question)
    st.write(f"**Bot Response:** {response}")

# Refresh button for market data
if st.button("Refresh Market Data"):
    with st.spinner("Refreshing data..."):
        market_data = fetch_market_data()
        st.success(f"Market data updated at {market_data['timestamp']}")

# Display the fetched market data
st.write("### Current Market Data (as of {})".format(market_data['timestamp']))
st.write(f"**VIX (Volatility Index):** {market_data['^VIX']}")
st.write(f"**S&P 500 (Market Performance):** {market_data['^GSPC']}")

# Additional features for data analysis
st.sidebar.header("Additional Features")
additional_feature = st.sidebar.selectbox("Choose an Analysis", ["Risk Mitigation Strategy", "Market Trend Insights"])

if additional_feature == "Risk Mitigation Strategy":
    st.write("### Risk Mitigation Strategy")
    st.write("""
        In times of market volatility (high VIX), the strategy typically involves shifting investments into **safe assets** like bonds, gold, and cash.
        When the market is stable or bullish (low VIX), focusing on **growth stocks** and **equity-based investments** is typically beneficial.
    """)
    st.write("### Strategy Recommendation:")
    st.write("""
        If VIX is high, we recommend reducing exposure to equities and focusing on **low-risk assets** to mitigate losses.
        If VIX is low and the S&P 500 is trending upwards, **investing in equities** and **growth stocks** becomes more viable for maximizing returns.
    """)
elif additional_feature == "Market Trend Insights":
    st.write("### Market Trend Insights")
    st.write("""
        - **VIX** (Volatility Index) above 30 often indicates high market fear and risk, often followed by market corrections.
        - A **bullish market** typically occurs when the S&P 500 is trending upwards with a VIX below 20.
    """)
    st.write("### Current Market Insights:")
    if market_data['^VIX'] > 30:
        st.write("The market is experiencing high volatility. Consider focusing on risk mitigation strategies.")
    elif market_data['^GSPC'] > 4500:
        st.write("The market is currently stable. A growth-focused strategy is recommended.")
    else:
        st.write("Market trends are uncertain. Monitor closely and adjust your portfolio as needed.")

# Display helpful tips for user interaction
st.sidebar.write("""
    - The app will automatically fetch and display the latest VIX and S&P 500 data.
    - Ask the bot for insights on specific market strategies or conditions.
    - Use the options in the sidebar to explore additional analysis features.
""")

# Add a footer for user engagement
st.markdown("""
    <footer style="text-align: center; padding: 20px;">
    <p>Powered by Streamlit, OpenAI, and Yahoo Finance</p>
    </footer>
""", unsafe_allow_html=True)
