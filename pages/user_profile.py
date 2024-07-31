import streamlit as st
import json
import os

# Path to the local storage file
STORAGE_FILE = 'user_data.json'

def load_user_data():
    """Load user data from the local storage file."""
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as file:
            return json.load(file)
    return {}

def calculate_rr_addition(investments):
    """Calculate RR based on investment behavior."""
    if len(investments) == 0:
        return -20  # Penalty if no investments

    # Example logic to calculate RR based on investments
    total_invested = sum(investment['amount'] for investment in investments)
    average_investment = total_invested / len(investments)
    
    rr = 0
    if average_investment > 0:
        rr += 20  # Basic RR addition for investments
    
    # Example adjustment based on sustainability or performance (dummy values)
    rr += 5  # Additional RR for sustainable investments or performance

    return rr

def calculate_performance(rr):
    """Calculate the virtual trading performance level based on RR."""
    if rr >= 200:
        return "Level 4"
    elif rr >= 150:
        return "Level 3"
    elif rr >= 100:
        return "Level 2"
    elif rr >= 50:
        return "Level 1"
    else:
        return "Unrated"

def display_profile():
    """Display the user profile page."""
    st.markdown(
        """
        <style>
        .profile-container {
            background-color: #1f1f1f;
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            max-width: 800px;
            margin: auto;
        }
        .profile-header {
            text-align: center;
            border-bottom: 2px solid #FF4500;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        .profile-stats {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .profile-stats div {
            text-align: center;
            padding: 10px;
            background-color: #333;
            border-radius: 5px;
            margin: 0 10px;
        }
        .profile-stats h3 {
            margin: 0;
            font-size: 18px;
        }
        .profile-stats p {
            font-size: 16px;
            margin: 5px 0;
        }
        .profile-header h2 {
            margin: 0;
            font-size: 24px;
        }
        .profile-header p {
            font-size: 14px;
            color: #ddd;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown("<div class='profile-container'>", unsafe_allow_html=True)

    user_data = load_user_data()
    username = st.session_state.get('username', 'Guest')
    user_info = user_data.get(username, {})

    # Retrieve user information
    first_name = user_info.get('first_name', 'Not Provided')
    last_name = user_info.get('last_name', 'Not Provided')
    email = user_info.get('email', 'Not Provided')

    # Retrieve investment data
    investments = user_info.get('monthly_investments', [])
    
    # Example RR calculation based on the logic
    rr = calculate_rr_addition(investments)
    performance = calculate_performance(rr)

    st.markdown("<div class='profile-header'>", unsafe_allow_html=True)
    st.markdown(f"<h2>{first_name} {last_name}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{email}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='profile-stats'>", unsafe_allow_html=True)
    st.markdown(f"<div><h3>Rank</h3><p>Silver II</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div><h3>Virtual Trading Performance</h3><p>{performance}</p></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
