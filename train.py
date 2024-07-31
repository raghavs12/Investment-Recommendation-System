import numpy as np
import yfinance as yf
import pandas as pd

# Gold prices data and calculations
years = list(range(1964, 2025))
prices = [
    63.25, 71.75, 83.75, 102.50, 162.00, 176.00, 184.00, 193.00, 202.00, 278.50,
    506.00, 540.00, 432.00, 486.00, 685.00, 937.00, 1330.00, 1670.00, 1645.00,
    1800.00, 1970.00, 2130.00, 2140.00, 2570.00, 3130.00, 3140.00, 3200.00,
    3466.00, 4334.00, 4140.00, 4598.00, 4680.00, 5160.00, 4725.00, 4045.00,
    4234.00, 4400.00, 4300.00, 4990.00, 5600.00, 5850.00, 7000.00, 10800.00,
    12500.00, 14500.00, 18500.00, 26400.00, 31050.00, 29600.00, 28006.50,
    26343.50, 28623.50, 29667.50, 31438.00, 35220.00, 48651.00, 48720.00,
    52670.00, 65330.00, 71510.00
]

returns = [(prices[i] - prices[i - 1]) / prices[i - 1] * 100 for i in range(1, len(prices))]
annualized_risk_gold = np.std(returns) * np.sqrt(1)

# Investment options
investment_options = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS', 'KOTAKBANK.NS',
    'ICICIBANK.NS', 'SBIN.NS', 'BAJFINANCE.NS', 'ITC.NS', 'AXISBANK.NS', 'LT.NS',
    'MARUTI.NS', 'TATAMOTORS.NS', 'SUNPHARMA.NS', 'YESBANK.NS', 'WIPRO.NS',
    'BHARTIARTL.NS', 'TITAN.NS', 'UPL.NS', 'ONGC.NS', 'BAJAJFINSV.NS', 'ADANIPORTS.NS',
    'SBILIFE.NS', 'HINDALCO.NS', 'GRASIM.NS', 'TATACONSUM.NS', 'ADANIGREEN.NS',
    'NTPC.NS', 'HDFCLIFE.NS', 'POWERGRID.NS', 'M&M.NS', 'INFIBEAM.NS', 'TATAMTRDVR.NS',
    'BPCL.NS', 'GAIL.NS', 'HEROMOTOCO.NS', 'DRREDDY.NS', 'BHEL.NS', 'MARICO.NS',
    'AMBUJACEM.NS', 'INDUSINDBK.NS', 'IOC.NS', 'TATAPOWER.NS', 'HDFCAMC.NS', 'LUPIN.NS',
    'TATASTEEL.NS', 'VEDL.NS', 'GODREJCP.NS',

    # ETFs
    'NIFTYBEES.NS', 'SETFNIF50.NS', 'ICICINXT50.NS', 'KOTAKBKETF.NS',
    'UTINEXT50.NS', 'ICICIGOLD.NS', 'GOLDETF.NS', 'HDFCNIFETF.NS', 'SBIETFIT.NS',
    'LIQUIDBEES.NS', 'ICICIM150.NS', 'MID150BEES.NS', 'BANKBEES.NS', 'HDFCPVTBAN.NS',
    'INDA', 'GOLDBEES.NS', '0P0000VCCU.BO',
    'UTIBANKETF.NS', 'SBIETFIT.NS', 'ICICI500.NS',

    # Futures
    '^NSEI', 'ES=F', 'YM=F', 'NQ=F',
    'RTY=F', 'ZB=F', 'ZN=F', 'ZF=F', 'ZT=F',
    'GC=F', 'MGC=F', 'SI=F', 'SIL=F', 'PL=F',
    'HG=F', 'PA=F', 'CL=F', 'HO=F',

    # Mutual Funds
    '0P0000XVSO.BO', '0P0000XW91.BO',
    '0P00009JAQ.BO', '0P00005V00.BO', '0P0000AEJZ.BO',
    '0P0000XW8F.BO', '0P00005WZZ.BO', '0P0000XV6O.BO', '0P00011MAX.BO', '0P0001OF68.BO',
    '0P00017844.BO', '0P00005UYJ.BO', '0P0000GB48.BO',
    '0P0001NQKD.BO'
]

def calculate_annualized_return(daily_returns):
    if len(daily_returns) == 0:
        return 'N/A'
    daily_returns_decimal = daily_returns / 100
    cumulative_return = np.prod(1 + daily_returns_decimal)
    annualized_return = (cumulative_return ** (252 / len(daily_returns_decimal))) - 1
    return annualized_return * 100

def calculate_annualized_risk(daily_returns):
    if len(daily_returns) == 0:
        return 'N/A'
    daily_std_dev = np.std(daily_returns)
    annualized_risk = daily_std_dev * np.sqrt(252)
    return annualized_risk

def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    if hist.empty:
        return None
    daily_returns = hist['Close'].pct_change().dropna() * 100

    annualized_return = calculate_annualized_return(daily_returns)
    annualized_risk = calculate_annualized_risk(daily_returns)

    info = stock.info

    # Fetch balance sheet data
    balance_sheet = stock.balance_sheet
    total_assets = balance_sheet.loc['Total Assets'].values[0] if 'Total Assets' in balance_sheet.index else 'N/A'
    total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'].values[0] if 'Total Liabilities Net Minority Interest' in balance_sheet.index else 'N/A'
    equity = float(total_assets) - float(total_liabilities) if total_assets != 'N/A' and total_liabilities != 'N/A' else 'N/A'

    def safe_get(key, default='N/A'):
        return info.get(key, default)

    def safe_float(key):
        try:
            return float(info.get(key, 'N/A'))
        except (ValueError, TypeError):
            return 'N/A'

    return {
        'name': safe_get('shortName'),
        'sector': safe_get('sector'),
        'price': safe_get('currentPrice'),
        'type': safe_get('quoteType'),
        'annualized_return': annualized_return,
        'annualized_risk': annualized_risk,
        'country': safe_get('country'),
        'currency': safe_get('currency'),
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'equity': equity,
        'longBusinessSummary': safe_get('longBusinessSummary'),
        'totalDebt': safe_float('totalDebt'),
        'totalCapital': safe_float('totalCapital'),
        'totalRetainedEarnings': safe_float('retainedEarnings'),
        'grossMargin': safe_float('grossMargins'),
        'operatingMargin': safe_float('operatingMargins'),
        'netMargin': safe_float('profitMargins'),
        'currentRatio': safe_float('currentRatio'),
        'quickRatio': safe_float('quickRatio'),
        'cashRatio': safe_float('cashRatio'),
        'debtToEquity': safe_float('debtToEquity'),
        'debtToCapital': safe_float('debtToCapital'),
        'debtToEV': safe_float('debtToEnterpriseValue'),
        'peRatio': safe_float('trailingPE'),
        'pegRatio': safe_float('pegRatio'),
        'pbRatio': safe_float('priceToBook'),
        'roe': safe_float('returnOnEquity'),
        'roa': safe_float('returnOnAssets'),
        'roic': safe_float('returnOnInvestedCapital')
    }

def store_financial_data():
    data_list = []
    for ticker in investment_options:
        data = get_financial_data(ticker)
        if data:
            data_list.append(data)

    df = pd.DataFrame(data_list)
    df.to_csv('financial_data.csv', index=False)

store_financial_data()
print("Financial data saved to financial_data.csv")
