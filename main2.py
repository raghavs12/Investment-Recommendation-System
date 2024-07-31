import streamlit as st
import pandas as pd
import numpy as np


# Load financial data
def load_financial_data():
    try:
        df = pd.read_csv('financial_data.csv')
        return df
    except FileNotFoundError:
        st.error("CSV file not found. Please run the fetch_and_store.py script first.")
        return None


# Format value
def format_value(value):
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        return value


# Recommend investments based on risk tolerance and filter
def recommend_investments(total_money, max_risk, duration, investment_type=None):
    df = load_financial_data()
    if df is None:
        return []

    recommendations = []

    for index, row in df.iterrows():
        try:
            annualized_risk = float(row['annualized_risk'])
            if max_risk * 0.95 <= annualized_risk <= max_risk * 1.05:
                if investment_type:
                    if row['type'] == investment_type:
                        recommendations.append(row.to_dict())
                else:
                    recommendations.append(row.to_dict())
        except ValueError:
            continue

    if investment_type and len(recommendations) == 0:
        st.warning(f"No recommendations found for the selected filter: {investment_type}")

    return recommendations


# Display recommended investments with Apply button
def display_recommendations(recommendations):
    st.write("\nRecommended Investment Vehicles:")
    st.write("-----------------------------------------------------------------------------------")
    for idx, recommendation in enumerate(recommendations):
        st.write(f"Name: {recommendation['name']}")
        st.write(f"Type: {recommendation['type']}")
        st.write(f"Annualized Risk: {format_value(recommendation['annualized_risk'])}%")
        st.write(f"Annualized Return: {format_value(recommendation['annualized_return'])}%")
        if st.button(f"Apply for {recommendation['name']}", key=f"apply_{idx}"):
            st.write(f"Applied for {recommendation['name']}")
        st.write("-----------------------------------------------------------------------------------")


# Recommend portfolio based on recommendations
def recommend_portfolio(recommendations, total_money):
    if total_money <= 0:
        st.error("Total money to be invested must be greater than zero.")
        return [], 0, 0

    num_investments = len(recommendations)
    if num_investments == 0:
        return [], 0, 0

    # Calculate portfolio weights using inverse volatility weighting
    total_inverse_volatility = sum(
        1 / float(r['annualized_risk']) for r in recommendations if r['annualized_risk'] != 'N/A')
    weights = [1 / (float(r['annualized_risk']) * total_inverse_volatility) if r['annualized_risk'] != 'N/A' else 0 for
               r in recommendations]

    # Normalize weights
    weights = [w / sum(weights) for w in weights]

    portfolio = []
    for i, recommendation in enumerate(recommendations):
        allocation = int(total_money * weights[i])
        portfolio.append({
            'name': recommendation['name'],
            'type': recommendation['type'],
            'allocation': allocation,
            'weight': (allocation / total_money) * 100,
            'annualized_risk': float(recommendation['annualized_risk']),
            'annualized_return': float(recommendation['annualized_return'])
        })

    # Calculate portfolio risk
    portfolio_risk = np.sqrt(sum((item['weight'] / 100) ** 2 * item['annualized_risk'] ** 2 for item in portfolio))

    # Calculate portfolio expected return
    portfolio_return = sum(item['weight'] / 100 * item['annualized_return'] for item in portfolio)

    return portfolio, portfolio_risk, portfolio_return


# Display portfolio with Apply button
def display_portfolio(portfolio, portfolio_risk, portfolio_return):
    st.write("\nRecommended Portfolio Allocation:")
    st.write("-----------------------------------------------------------------------------------")
    for idx, item in enumerate(portfolio):
        st.write(f"Name: {item['name']}")
        st.write(f"Type: {item['type']}")
        st.write(f"Allocation: {item['allocation']:,.2f}")
        st.write(f"Weight: {item['weight']:.2f}%")
        st.write(f"Annualized Risk: {item['annualized_risk']:.2f}%")
        st.write(f"Annualized Return: {item['annualized_return']:.2f}%")
        if st.button(f"Apply for {item['name']}", key=f"portfolio_apply_{idx}"):
            st.write(f"Applied for {item['name']}")
        st.write("-----------------------------------------------------------------------------------")

    st.write(f"\nOverall Portfolio Annualized Risk: {portfolio_risk:.2f}%")
    st.write(f"Expected Annualized Return: {portfolio_return:.2f}%")


# Main function
def main():
    st.title("Investment Page")

    # Input fields
    total_money = st.number_input("Enter the total amount of money to be invested:", min_value=0.0, step=1000.0,
                                  key="total_money")
    duration = st.number_input("Enter the duration of investment (in years):", min_value=1, step=1, key="duration")
    investment_goal = st.text_input("Enter your investment goal:", "", key="investment_goal")

    # Filter
    investment_type = st.selectbox("Filter:", [None, 'Equity', 'ETFs', 'Gold', 'Futures', 'Mutual Fund'],
                                   key="investment_type")

    # Risk tolerance quiz
    questions = [
        "1. In general, how would your best friend describe you as a risk taker?",
        "2. You are on a TV game show and can choose one of the following. Which would you take?",
        "3. You have just finished saving for a 'once-in-a-lifetime' vacation. Three weeks before you plan to leave, you lose your job. You would:",
        "4. If you unexpectedly received $20,000 to invest, what would you do?",
        "5. In terms of experience, how comfortable are you investing in stocks or stock mutual funds?",
        "6. When you think of the word 'risk' which of the following words comes to mind first?",
        "7. Some experts are predicting prices of assets such as gold, jewels, collectibles, and real estate (hard assets) to increase in value; bond prices may fall, however, experts tend to agree that government bonds are relatively safe. Most of your investment assets are now in high interest government bonds. What would you do?",
        "8. Given the best and worst case returns of the four investment choices below, which would you prefer?",
        "9. In addition to whatever you own, you have been given $1,000. You are now asked to choose between:",
        "10. In addition to whatever you own, you have been given $2,000. You are now asked to choose between:",
        "11. Suppose a relative left you an inheritance of $100,000, stipulating in the will that you invest ALL the money in ONE of the following choices. Which one would you select?",
        "12. If you had to invest $20,000, which of the following investment choices would you find most appealing?",
        "13. Your trusted friend and neighbor, an experienced geologist, is putting together a group of investors to fund an exploratory gold mining venture. The venture could pay back 50 to 100 times the investment if successful. If the mine is a bust, the entire investment is worthless. Your friend estimates the chance of success is only 20%. If you had the money, how much would you invest?"
    ]

    options = [
        ['a. A real gambler', 'b. Willing to take risks after completing adequate research', 'c. Cautious',
         'd. A real risk avoider'],
        ['a. $1,000 in cash', 'b. A 50% chance at winning $5,000', 'c. A 25% chance at winning $10,000',
         'd. A 5% chance at winning $100,000'],
        ['a. Cancel the vacation', 'b. Take a much more modest vacation',
         'c. Go as scheduled, reasoning that you need the time to prepare for a job search',
         'd. Extend your vacation, because this might be your last chance to go first-class'],
        ['a. Deposit it in a bank account, money market account, or an insured CD',
         'b. Invest it in safe high quality bonds or bond mutual funds',
         'c. Invest it in stocks or stock mutual funds'],
        ['a. Not at all comfortable', 'b. Somewhat comfortable', 'c. Very comfortable'],
        ['a. Loss', 'b. Uncertainty', 'c. Opportunity', 'd. Thrill'],
        ['a. Hold the bonds',
         'b. Sell the bonds, put half the proceeds into money market accounts, and the other half into hard assets',
         'c. Sell the bonds and put the total proceeds into hard assets'],
        ['a. $0 gain best case; $0 loss worst case', 'b. $800 gain best case; $200 loss worst case',
         'c. $2,600 gain best case; $800 loss worst case', 'd. $4,800 gain best case; $2,400 loss worst case'],
        ['a. A sure gain of $500', 'b. A 50% chance to gain $1,000 and a 50% chance to gain nothing'],
        ['a. A sure gain of $1,500', 'b. A 50% chance to gain $3,000 and a 50% chance to gain nothing'],
        ['a. A savings account or money market mutual fund', 'b. A mutual fund that owns stocks and bonds',
         'c. A portfolio of 15 common stocks', 'd. Commodities like gold, silver, and oil'],
        ['a. The safety of US Government Bonds', 'b. The high returns of stock market investments'],
        ['a. $0', 'b. $1,000', 'c. $5,000', 'd. $10,000']
    ]

    # Risk tolerance scoring
    risk_scores = {
        'a': [4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'b': [3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        'c': [2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        'd': [1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    }

    responses = []
    for i, question in enumerate(questions):
        st.write(question)
        response = st.radio("", options[i], key=f"q{i + 1}")
        responses.append(response[0].lower())  # Store the response key (a, b, c, d)

    # Calculate risk tolerance
    total_score = sum(risk_scores[response][i] for i, response in enumerate(responses))
    max_risk = min(max(1, total_score / len(questions)), 10) * 10

    # Proceed with recommendations only after quiz
    if total_money > 0 and investment_goal:
        # Recommend investments
        recommendations = recommend_investments(total_money, max_risk, duration, investment_type)

        # Display recommendations
        display_recommendations(recommendations)

        # Recommend and display portfolio
        if recommendations:
            portfolio, portfolio_risk, portfolio_return = recommend_portfolio(recommendations, total_money)
            display_portfolio(portfolio, portfolio_risk, portfolio_return)

    # Display the concluding paragraph
    st.write("""
        Capital markets, particularly equity investments, have historically outperformed gold and real estate over long periods, offering investors a compelling alternative to these traditional assets. While gold and real estate have their merits, capital markets present unique advantages that can lead to potentially higher returns.

        The primary market, particularly Initial Public Offerings (IPOs), offers investors opportunities that are simply not available in gold or real estate markets. When a promising company goes public, early investors can acquire shares at the ground level, potentially setting themselves up for substantial gains as the company grows. This type of high-growth potential is rarely seen in gold or real estate investments. For instance, investors who participated in the IPOs of major tech companies over the past few decades have seen returns that far outpaced those of gold or real estate in the same period.

        In the secondary market, investors can easily buy and sell shares of established companies, many of which have consistently delivered returns that surpass the appreciation rates of gold and real estate. Unlike physical assets like gold or property, stocks represent ownership in businesses that can grow, innovate, and expand their operations, potentially leading to higher returns. Moreover, many stocks pay dividends, providing a regular income stream that gold cannot offer and that often exceeds rental yields from real estate.

        While gold is often seen as a safe haven during economic uncertainty, and real estate as a stable long-term investment, capital markets offer a broader range of options for mid and long-term financial goals. Investors can choose from a diverse array of sectors and companies, allowing for more nuanced strategies to match specific financial objectives. This flexibility is not available with gold, which is essentially a single asset, or real estate, which often requires significant capital and is less liquid.

        It's true that capital markets can entail more short-term volatility compared to gold or real estate. However, this volatility often translates to higher potential returns over the long run. Historical data shows that despite periodic downturns, stock markets have generally trended upward over time, often outpacing the growth rates of both gold and real estate. Investors who can tolerate some volatility and maintain a long-term perspective may find that the potential rewards in capital markets outweigh the risks.

        Furthermore, capital markets provide a level of liquidity that is unmatched by real estate and often superior to gold. Investors can easily buy or sell securities, allowing for quick adjustments to their portfolio or access to funds when needed. This liquidity also means lower transaction costs compared to buying or selling property, and often lower costs than dealing in physical gold.

        Capital markets also play a crucial role in economic growth by providing companies with access to funding. This not only potentially benefits investors through higher returns but also contributes to overall economic development. In contrast, investments in gold do not directly contribute to economic productivity, and real estate investments, while important, do not typically fuel innovation and economic expansion to the same degree as capital markets.

        Lastly, the volatility in capital markets, while sometimes unnerving, can create opportunities for significant wealth accumulation. Market downturns allow investors to acquire quality assets at discounted prices, setting the stage for substantial gains when markets recover. This dynamic is less pronounced in gold markets and rarely occurs in real estate, where opportunities to buy at significant discounts are less frequent.

        In conclusion, while gold and real estate have their place in a diversified investment portfolio, capital markets offer unique advantages that can lead to potentially higher returns. The combination of growth potential, liquidity, dividend income, and the ability to easily diversify makes capital markets an attractive option for investors looking to build wealth over the long term. By understanding and leveraging these advantages, investors may find that capital markets offer a more dynamic and potentially rewarding investment avenue compared to traditional options like gold and real estate.
    """)


if __name__ == "__main__":
    main()
