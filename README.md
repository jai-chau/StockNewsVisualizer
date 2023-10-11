<h1>StockNewsVisualizer</h1>

<p>
        StockNewsVisualizer is an application built to visualize stock prices and annotate them with relevant news articles extracted from Finviz. This offers users insights into how news events might influence stock price movements.
    </p>

<h2>Features</h2>
    <ul>
        <li>Fetch and display news articles related to a specific stock ticker.</li>
        <li>Visual representation of stock prices using line charts.</li>
        <li>Annotate stock prices with significant news events.</li>
    </ul>

<h2>Prerequisites</h2>
    <ul>
        <li>Pandas</li>
        <li>Requests</li>
        <li>BeautifulSoup</li>
        <li>Streamlit</li>
        <li>YFinance</li>
        <li>Plotly</li>
    </ul>

<h2>Setup and Run</h2>
    <ol>
        <li>Clone the repository: <code>git clone [your-repo-link]</code></li>
        <li>Navigate to the directory: <code>cd StockNewsVisualizer</code></li>
        <li>Install the necessary packages: <code>pip install -r requirements.txt</code></li>
        <li>Run the Streamlit app: <code>streamlit run app.py</code></li>
    </ol>

<h2>Usage</h2>
    <p>Input a stock ticker and select the number of news articles you want to display. The application will fetch the stock price data and relevant news articles, and then visualize them on a chart.</p>
