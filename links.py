import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_internal_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        internal_links = set()
        # Find all anchor tags with 'href' attribute
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Check if the link is internal
            if href.startswith('/') or url in href:
                internal_links.add(href)
        return internal_links
    except Exception as e:
        st.error(f"An error occurred: {e}")

def get_http_status(url):
    try:
        response = requests.get(url)
        return response.status_code
    except Exception as e:
        return str(e)

def main():
    st.title("Internal Links Extractor")
    url = st.text_input("Enter the URL:")
    if st.button("Extract Internal Links"):
        if not url:
            st.warning("Please enter a URL.")
        else:
            st.info("Processing...")
            internal_links = get_internal_links(url)
            if internal_links:
                st.success("Internal links found:")
                table_data = []
                for link in internal_links:
                    full_link = url + link if link.startswith('/') else link
                    status_code = get_http_status(full_link)
                    table_data.append((full_link, status_code))
                st.table(table_data, headers=['Link', 'Status Code'])
            else:
                st.warning("No internal links found on the provided URL.")

if __name__ == "__main__":
    main()
