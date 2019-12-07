import requests
import re
from bs4 import BeautifulSoup

def extract_summary(url):
    try:
        r = requests.get(url).content
        
    except Exception as e:
        print(e)
        
    try:
        soup = BeautifulSoup(r, 'html.parser')
        
        # Get wiki page title
        
        page_title = soup.find('h1').get_text()
        
        # get page body text
        
        page_body_text = [txt.get_text() for txt in soup.find_all('p')]
        
        # Clean the body text
        ## remove the next line
        
        [page_body_text.pop(i) for i, x in enumerate(page_body_text) if x == '\n']
        
        ## remove annotation from the page
        
        page_body_text = [re.sub(r"\[([0-9]+)\].*", '', txt) for txt in page_body_text]
        
        ## remove new line from within each text
        
        page_body_text = [txt.replace('\n', '') for txt in page_body_text]

        return page_body_text
        
    except Exception as e:
        print(e)