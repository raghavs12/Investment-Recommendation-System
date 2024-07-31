import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import plotly.graph_objs as go
from streamlit_autorefresh import st_autorefresh

# Set the page config
# st.set_page_config(page_title="Virtual Trading App", layout="wide")

# Auto-refresh every 5 seconds (adjust as needed)
st_autorefresh(interval=5000)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.portfolio = {"AAPL": 0, "GOOGL": 0, "AMZN": 0, "TSLA": 0, "MSFT": 0, "META": 0, "NVDA": 0, "NFLX": 0}
    st.session_state.balance = 10000
    st.session_state.transaction_history = []
    st.session_state.average_cost = {"AAPL": 0, "GOOGL": 0, "AMZN": 0, "TSLA": 0, "MSFT": 0, "META": 0, "NVDA": 0, "NFLX": 0}
    st.session_state.RR = 0

def adjust_rr(successful_trade, sustainable_investment):
    base_rr = 20
    if successful_trade:
        base_rr += 5
    if sustainable_investment:
        base_rr += 5
    st.session_state.RR += base_rr

@st.cache_data(ttl=5)  # Cache for 5 seconds
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d', interval='1m')
    
    if not data.empty:
        latest = data.iloc[-1]
        return {
            "Ticker": ticker,
            "Last": latest['Close'],
            "Bid": latest['Low'],
            "Ask": latest['High'],
            "Volume": latest['Volume'],
            "High": data['High'].max(),
            "Low": data['Low'].min(),
        }
    else:
        return {
            "Ticker": ticker,
            "Last": None,
            "Bid": None,
            "Ask": None,
            "Volume": None,
            "High": None,
            "Low": None,
        }

def buy_stock(stock, amount):
    price = get_stock_data(stock)['Last']
    if price is None:
        st.error("Failed to retrieve stock price.")
        return
    cost = price * amount
    if st.session_state.balance >= cost:
        st.session_state.portfolio[stock] += amount
        st.session_state.balance -= cost
        
        total_cost = st.session_state.average_cost[stock] * (st.session_state.portfolio[stock] - amount) + cost
        st.session_state.average_cost[stock] = total_cost / st.session_state.portfolio[stock]
        
        st.session_state.transaction_history.append({
            'Type': 'Buy',
            'Stock': stock,
            'Amount': amount,
            'Price': price,
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        adjust_rr(successful_trade=True, sustainable_investment=True)
        st.success(f"Bought {amount} shares of {stock} at ${price:.2f} each")
    else:
        st.error("Insufficient funds to complete this transaction")

def sell_stock(stock, amount):
    if st.session_state.portfolio[stock] >= amount:
        price = get_stock_data(stock)['Last']
        if price is None:
            st.error("Failed to retrieve stock price.")
            return
        revenue = price * amount
        st.session_state.portfolio[stock] -= amount
        st.session_state.balance += revenue
        st.session_state.transaction_history.append({
            'Type': 'Sell',
            'Stock': stock,
            'Amount': amount,
            'Price': price,
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        adjust_rr(successful_trade=True, sustainable_investment=False)
        st.success(f"Sold {amount} shares of {stock} at ${price:.2f} each")
    else:
        st.error("Not enough shares to sell")

@st.cache_data(ttl=5)  # Cache for 5 seconds
def plot_stock(stock):
    data = yf.Ticker(stock).history(period='1d', interval='1m')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    fig.update_layout(title=f'{stock} Stock Price', xaxis_title='Date', yaxis_title='Price (USD)')
    return fig

def update_portfolio_data():
    portfolio_data = []
    total_value = 0
    total_cost = 0
    for stock, amount in st.session_state.portfolio.items():
        if amount > 0:
            market_data = get_stock_data(stock)
            price = market_data['Last']
            value = price * amount if price else 0
            cost = st.session_state.average_cost[stock] * amount
            profit_loss = value - cost
            total_value += value
            total_cost += cost
            portfolio_data.append({
                "Stock": stock,
                "Amount": amount,
                "Price": price,
                "Value": value,
                "Average Cost": st.session_state.average_cost[stock],
                "Profit/Loss": profit_loss
            })
    return portfolio_data, total_value, total_cost

def virtual_trading():
    st.header("Virtual Trading")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Balance")
        balance_container = st.empty()

        st.subheader("Portfolio")
        portfolio_container = st.empty()
        portfolio_summary_container = st.empty()

        st.subheader("Market Grid")
        market_grid_container = st.empty()

    with col2:
        st.subheader("Buy Stock")
        stock_to_buy = st.selectbox("Select stock to buy", list(st.session_state.portfolio.keys()), key="buy_stock")
        amount_to_buy = st.number_input("Amount to Buy", min_value=1, key="buy_amount")
        if st.button("Buy"):
            buy_stock(stock_to_buy, amount_to_buy)
        
        st.subheader("Sell Stock")
        stock_to_sell = st.selectbox("Select stock to sell", list(st.session_state.portfolio.keys()), key="sell_stock")
        amount_to_sell = st.number_input("Amount to Sell", min_value=1, key="sell_amount")
        if st.button("Sell"):
            sell_stock(stock_to_sell, amount_to_sell)
        
        st.subheader("Transaction History")
        transaction_history_container = st.empty()

    st.subheader("Real-Time Stock Price Chart")
    selected_chart_stock = st.selectbox("Select stock to view chart", list(st.session_state.portfolio.keys()), key="chart_stock")
    chart_container = st.empty()

    # Update balance
    balance_container.write(f"${st.session_state.balance:.2f}")

    # Update portfolio data
    portfolio_data, total_value, total_cost = update_portfolio_data()
    portfolio_df = pd.DataFrame(portfolio_data)
    portfolio_container.dataframe(portfolio_df)
    portfolio_summary_container.write(f"Total Portfolio Value: ${total_value:.2f}")
    portfolio_summary_container.write(f"Total Profit/Loss: ${total_value - total_cost:.2f}")

    # Update market grid
    market_data = [get_stock_data(stock) for stock in st.session_state.portfolio.keys()]
    market_df = pd.DataFrame(market_data)
    market_grid_container.dataframe(market_df)

    # Update transaction history
    if st.session_state.transaction_history:
        df = pd.DataFrame(st.session_state.transaction_history)
        transaction_history_container.dataframe(df)
    else:
        transaction_history_container.write("No transactions yet")

    # Update chart
    fig = plot_stock(selected_chart_stock)
    chart_container.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    virtual_trading()