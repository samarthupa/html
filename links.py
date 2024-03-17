import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse

# Function to extract links from the webpage
def extract_links(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)

    links = []

    # Extracting <a> tags
    elements = driver.find_elements_by_tag_name('a')
    for element in elements:
        href = element.get_attribute('href')
        # Handling relative URLs
        if href:
            links.append(urljoin(url, href))

    driver.quit()

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
