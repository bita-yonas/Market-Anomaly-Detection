# Market-Anomaly-Detection


This project is a **Market Anomaly Detection** system built using **Streamlit**, **OpenAI**, and **Yahoo Finance**. It predicts market anomalies based on real-time financial data such as **VIX** (Volatility Index) and **S&P 500**, and recommends investment strategies accordingly. The system also provides AI-driven explanations for the suggested strategies.

## Features

- **Anomaly Detection**: Detects market anomalies based on **VIX** and **S&P 500** data.
- **Investment Strategy Recommendations**: Based on market anomalies, suggests strategies to either minimize risk or optimize growth.
- **AI-driven Explanations**: Uses **Groq's Llama model** to explain the recommended investment strategies in simple terms.
- **Real-time Data Fetching**: Fetches the latest **VIX** and **S&P 500** data from **Yahoo Finance**.
- **User Interaction**: Users can query the bot for detailed explanations of market conditions and strategies.

## Technologies Used

- **Streamlit**: For building the interactive web app.
- **OpenAI**: For generating AI-powered strategy explanations using the Llama model.
- **Yahoo Finance**: For fetching real-time market data like **VIX** and **S&P 500**.
- **joblib**: For loading a pre-trained machine learning model used for market anomaly detection.
- **Python**: Primary programming language.
