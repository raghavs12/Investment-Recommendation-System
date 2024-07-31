import streamlit as st

# Initialize session state for sign-in status and current page
if 'signed_in' not in st.session_state:
    st.session_state.signed_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Profile"

def set_page(page):
    st.session_state.current_page = page

def nav_bar():
    pages = ["Profile", "Investment Page", "Virtual Trading", "Policies", "Support"]
    nav_items = ""
    for page in pages:
        if page == st.session_state.current_page:
            nav_items += f"<div class='nav-item active'>{page}</div>"
        else:
            nav_items += f"<div class='nav-item' onclick='switchPage(\"{page}\")'>{page}</div>"

    nav_html = f"<div class='nav-container'>{nav_items}</div>"
    st.markdown(nav_html, unsafe_allow_html=True)

def main():
    # Apply custom CSS
    st.markdown("""
        <style>
        .stApp {
            background-color: black;
        }
        .nav-container {
            display: flex;
            justify-content: space-around;
            background-color: #1E1E1E;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .nav-item {
            padding: 10px 20px;
            text-align: center;
            color: white;
            background-color: #FF4500;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .nav-item:hover {
            background-color: #FF6347;
        }
        .nav-item.active {
            background-color: #FF8C00;
        }
        </style>
    """, unsafe_allow_html=True)

    if not st.session_state.signed_in:
        import pages.sign_up as sign_up_page
        sign_up_page.signin()
    else:
        nav_bar()
        pages = ["Profile", "Investment Page", "Virtual Trading", "Policies", "Support"]
        selected_page = st.selectbox("Navigate to:", options=pages, index=pages.index(st.session_state.current_page))
        if selected_page != st.session_state.current_page:
            set_page(selected_page)

        if st.session_state.current_page == "Profile":
            import pages.user_profile as profile
            profile.display_profile()
        elif st.session_state.current_page == "Investment Page":
            import pages.investment_page as investment
            investment.main()
        elif st.session_state.current_page == "Virtual Trading":
            import pages.virtual_trading as trading
            trading.virtual_trading()
        elif st.session_state.current_page == "Policies":
            import pages.policies as policies
            policies.main()
        elif st.session_state.current_page == "Support":
            st.write("Support page content goes here")

if __name__ == "__main__":
    main()
