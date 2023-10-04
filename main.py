# Importing the necessary packages
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, date

# Streamlit app title
st.set_page_config(layout="wide")
st.title("Extracted News Articles")

# Inputting the Ticker and Number of Phrases Wanted from the sidebar
ticker = st.sidebar.text_input("Ticker", value='', max_chars=4)
topNum = st.sidebar.number_input("Number of Outputs Wanted", min_value=1, max_value=100, value=10)

def newsArticle(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
    agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=agent)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('tr.cursor-pointer.has-label')

    titles = []
    links = []
    times = []
    last_date = None  # Used to store the last encountered date

    for row in rows:
        title = row.select_one('.tab-link-news').get_text()
        link = row.select_one('.tab-link-news')['href']
        time = row.select_one('td[width="130"]').get_text().strip()

        # Handle the "Today" case
        if time.startswith("Today"):
            time = date.today().strftime('%b-%d-%y') + ' ' + time.split(" ")[1]

        # Check if the time string contains a date
        if len(time.split()) > 1:
            last_date = time.rsplit(' ', 2)[0]
        else:
            time = last_date + ' ' + time

        titles.append(title)
        links.append(link)
        times.append(time)

    return pd.DataFrame({
        "Release Time": times,
        "Article Name": titles,
        "Article Link": links
    })

if ticker:
    data = newsArticle(ticker)

    # Displaying data in a table with column names
    st.table(data.head(topNum))

    # Fetch stock price data
    stock_data = yf.download(ticker, start="2023-01-01", end="2023-12-31")

    # Create figure with stock price data
    fig = go.Figure()

    # Adding stock price data as a line chart
    fig.add_trace(go.Scatter(x=stock_data.index,
                            y=stock_data['Close'],
                            mode='lines',
                            name='Stock Price'))

    # Create lists to collect dates with news and their respective close prices
    news_dates = []
    news_prices = []
    hover_texts = []

    # Populate the lists
    for date, grouped_data in data.groupby('Release Time'):
        news_date = datetime.strptime(date, '%b-%d-%y %I:%M%p').strftime('%Y-%m-%d')
        if news_date in stock_data.index:
            news_dates.append(news_date)
            news_prices.append(stock_data.loc[news_date, 'Close'])
            articles = "<br>".join(grouped_data['Article Name'])
            hover_texts.append(f"Date: {news_date}<br>{articles}")

    # Add scatter plot for dates with news
    fig.add_trace(go.Scatter(x=news_dates, y=news_prices, hovertext=hover_texts, mode='markers',
                            marker=dict(size=10, color='red', symbol='circle'),
                            name='News Date'))

    fig.update_traces(hoverinfo="text")
    fig.update_layout(title=f"Stock Price and News Articles for {ticker.upper()}",
                    xaxis_title="Date",
                    yaxis_title="Stock Price",
                    hovermode="closest")
    st.plotly_chart(fig)
