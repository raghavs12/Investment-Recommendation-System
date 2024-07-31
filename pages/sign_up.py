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

def save_user_data(data):
    """Save user data to the local storage file."""
    with open(STORAGE_FILE, 'w') as file:
        json.dump(data, file)

def signup():
    """Create a new user account."""
    st.markdown(
        """
        <style>
        .main {
            background-color: #000000;
        }
        .stTextInput > div > div > input {
            background-color: #C0C0C0;
        }
        .stButton > button {
            background-color: #FF4500;
            color: white;
            border-radius: 5px;
            width: 100%;
            padding: 10px;
            font-size: 18px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center; color: white;'>Create Account</h1>", unsafe_allow_html=True)

    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    email = st.text_input('Email Address')
    username = st.text_input('Username')
    pin = st.text_input('Set PIN', type='password')
    confirm_pin = st.text_input('Confirm PIN', type='password')
    pan_number = st.text_input('PAN Number')
    bank_details = st.text_input('Bank Details')

    if st.button('Create Account'):
        user_data = load_user_data()

        if pin != confirm_pin:
            st.error('PINs do not match.')
            return

        if username in user_data:
            st.error('Username already exists.')
        else:
            user_data[username] = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'pin': pin,
                'pan_number': pan_number,
                'bank_details': bank_details
            }
            save_user_data(user_data)
            st.success('Account created successfully!')

def signin():
    """Sign in an existing user."""
    st.markdown(
        """
        <style>
        .main {
            background-color: #000000;
        }
        .stTextInput > div > div > input {
            background-color: #C0C0C0;
        }
        .stButton > button {
            background-color: #FF4500;
            color: white;
            border-radius: 5px;
            width: 100%;
            padding: 10px;
            font-size: 18px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center; color: white;'>Sign In</h1>", unsafe_allow_html=True)

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Sign In'):
        user_data = load_user_data()
        
        if username not in user_data:
            st.error('Username does not exist.')
        elif user_data[username]['pin'] != password:
            st.error('Incorrect password.')
        else:
            st.session_state.signed_in = True
            st.session_state.username = username
            st.success('Signed in successfully!')
            st.rerun()

def main():
    """Main function to switch between sign-in and investment page."""
    st.sidebar.title('Menu')
    if 'signed_in' not in st.session_state:
        st.session_state.signed_in = False

    if st.session_state.signed_in:
        import pages.investment_page as investment
        investment.main()
    else:
        signin()

if __name__ == '__main__':
    main()
