# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy everything to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir streamlit==1.17.1 openai==0.27.0 yfinance==0.1.74 pandas==1.5.3 numpy==1.23.5 scikit-learn==1.2.0 joblib

# Expose port Streamlit runs on
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
