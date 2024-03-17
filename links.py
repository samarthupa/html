# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import time

def fetch_links(url):
    st.write("Fetching links from:", url)
    st.info("Please wait while links are being fetched...")
    
    # Fetch links using requests and BeautifulSoup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    base_url = page.url  # Get the base URL after redirects
    links = soup.find_all('a', href=True)
    
    # Fetch links using Selenium for JavaScript-rendered content
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    time.sleep(5)  # Allow time for JavaScript to render
    js_links = driver.find_elements_by_tag_name('a')
    for link in js_links:
        href = link.get_attribute('href')
        if href:
            absolute_url = urljoin(base_url, href)
            links.append(absolute_url)
    driver.quit()
    
    return links

def main():
    st.title("Internal Link Checker")
    url = st.text_input("Enter the URL of the webpage:")
    
    if st.button("Check Links"):
        if url:
            links = fetch_links(url)
            st.write("Total number of links detected:", len(links))
            st.write("List of links:")
            for link in links:
                st.write(link)
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
