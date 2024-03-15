import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def extract_urls_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()
    # Extract URLs from anchor tags
    for link in soup.find_all('a', href=True):
        urls.add(link['href'])
    # Extract URLs from CSS
    css_urls = re.findall(r'url\((.*?)\)', soup.text)
    urls.update(css_urls)
    # Extract URLs from JavaScript
    js_urls = re.findall(r'src="(.*?)"', soup.text)
    urls.update(js_urls)
    return urls

def process_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.success(f"Successfully fetched URL: {url}")
            extracted_urls = extract_urls_from_html(response.text)
            st.write("Extracted URLs from the page:")
            for extracted_url in extracted_urls:
                st.write(extracted_url)
        else:
            st.error(f"Failed to fetch URL: {url}. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.title("URL Extractor")
    url = st.text_input("Enter a URL:")
    if st.button("Extract URLs"):
        if url:
            process_url(url)
        else:
            st.warning("Please enter a URL.")

if __name__ == "__main__":
    main()
