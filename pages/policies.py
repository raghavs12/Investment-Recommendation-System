import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_updates():
    url = 'https://www.india.gov.in/my-government/documents/policy'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    updates = []
    # Find the section containing updates (adjust the selector as needed)
    update_section = soup.find_all('div', class_='views-row')
    
    for update in update_section:
        title = update.find('a').get_text(strip=True)
        link = update.find('a')['href']
        description = update.find('div', class_='field-content').get_text(strip=True)
        
        updates.append({'title': title, 'link': link, 'description': description})
    
    return updates

def main():
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<h1>Latest Government Updates</h1>', unsafe_allow_html=True)
    
    st.markdown('<p>Fetching the latest updates about government moves making people\'s lives easier...</p>', unsafe_allow_html=True)
    
    updates = fetch_updates()
    
    if updates:
        for update in updates:
            st.markdown(f"### [{update['title']}]({update['link']})")
            st.markdown(f"{update['description']}")
    else:
        st.markdown('<p>No updates found.</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
