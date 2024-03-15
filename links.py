import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

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
                for link in internal_links:
                    st.markdown(f"- [{link}]({url + link})")
            else:
                st.warning("No internal links found on the provided URL.")

if __name__ == "__main__":
    main()
