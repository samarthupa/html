import streamlit as st
from requests_html import HTMLSession
from urllib.parse import urljoin, urlparse

# Function to extract links from the webpage
def extract_links(url):
    session = HTMLSession()
    response = session.get(url)
    response.html.render()

    links = []

    # Extracting <a> tags
    for link in response.html.absolute_links:
        links.append(link)

    return links

# Streamlit app
def main():
    st.title('Internal Link Checker')
    st.write('Enter the URL of the webpage to check internal links:')

    # Input URL
    url = st.text_input('URL')

    if st.button('Check Links'):
        if url:
            st.write(f'Fetching links from {url}...')
            links = extract_links(url)
            st.write(f'Found {len(links)} links:')
            for link in links:
                st.write(link)
        else:
            st.write('Please enter a valid URL.')

if __name__ == '__main__':
    main()
