import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

def get_stock_data(stock_name, period='1y', interval='1d'):
    stock = yf.Ticker(stock_name)
    data = stock.history(period=period, interval=interval)
    if data.empty:
        return None
    return data

def main():
    st.title('Smit Stock Market App')

    # Display top companies' stock prices
    st.subheader('Top 10 Companies Stock Prices')

    # Define the top 10 companies
    top_companies = {
        'Apple': 'AAPL',
        'Meta': 'META',
        'Amazon': 'AMZN',
        'Google': 'GOOGL',
        'Microsoft': 'MSFT',
        'Tesla': 'TSLA',
        'Facebook': 'FB',
        'Alibaba': 'BABA',
        'Tencent': 'TCEHY',
        'Netflix': 'NFLX'
    }

    # Fetching data and displaying prices
    for company, symbol in top_companies.items():
        data = get_stock_data(symbol)
        if data is not None:
            current_price = data['Close'].iloc[-1]
            previous_price = data['Close'].iloc[-2]
            price_change = current_price - previous_price
            price_change_percent = (price_change / previous_price) * 100
            st.write(f"{company}: ${current_price:.2f} ({'+' if price_change >= 0 else ''}{price_change:.2f}, {'+' if price_change_percent >= 0 else ''}{price_change_percent:.2f}%)")

    # Search for a specific stock symbol
    st.subheader('Search for a Stock')
    stock_name = st.text_input('Enter stock symbol (e.g., AAPL for Apple):')

    if st.button('Search'):
        data = get_stock_data(stock_name.upper())
        if data is not None:
            current_price = data['Close'].iloc[-1]
            previous_price = data['Close'].iloc[-2]
            price_change = current_price - previous_price
            price_change_percent = (price_change / previous_price) * 100
            st.write(f"{stock_name.upper()} Current Price: ${current_price:.2f} ({'+' if price_change >= 0 else ''}{price_change:.2f}, {'+' if price_change_percent >= 0 else ''}{price_change_percent:.2f}%)")

            # Choose chart library (matplotlib or plotly)
            chart_library = st.radio("Choose Chart Library:", ("Matplotlib", "Plotly"))

            # Plot price history
            if chart_library == "Matplotlib":
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(data.index, data['Close'])
                ax.set_title(f"{stock_name.upper()} Price History (1 Year)")
                ax.set_xlabel("Date")
                ax.set_ylabel("Closing Price")
                st.pyplot(fig)
            elif chart_library == "Plotly":
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
                fig.update_layout(title=f"{stock_name.upper()} Price History (1 Year)", xaxis_title="Date", yaxis_title="Closing Price")
                st.plotly_chart(fig)

if __name__ == "__main__":
    main()
