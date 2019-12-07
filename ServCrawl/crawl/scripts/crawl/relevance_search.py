import requests
import json
from bs4 import BeautifulSoup

#URL = "https://en.wikipedia.org/w/index.php?cirrusUserTesting=control&sort=relevance&search={}&title=Special:Search&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1"
URL = "https://en.wikipedia.org/w/index.php?title=Special:Search&limit=500&offset=0&ns0=1&search={}&advancedSearch-current={}"

class RelevantSearch:
    """ Searches Wikipedia for relevant data """
    
    def __init__(self, search_word):

            if search_word:
                self.url = URL.format(search_word, '')
    
    def check_url_authenticity(self):
        """ Checks for url authenticity """
        
        try:
            self.r = requests.get(self.url)
            jsonresponse = {
                'success' : True,
                'status_code' : self.r.status_code,
            }
            
            return jsonresponse
        
        except Exception as e:
            
            jsonresponse = {
                'success' : False,
                'status_code' : self.r.status_code,
                'error' : str(e)
            }
            
    def extract_relevant(self, title='True', link='True',
        article_size='False', total_article_words='False',
        date='False'):
        """ Returns extracted data from the search"""
        
        try:
            result_data = []

            r = self.r.content.decode('utf-8')
            soup = BeautifulSoup(r, 'html.parser')
            
            wiki_data = soup.select("li.mw-search-result")
            
            for se in wiki_data:
                
                current_data = {}

                if title == 'True':
                    _title = se.select("div a")[0]['title']
                    current_data['Title'] = _title
                
                if link == 'True':
                    href = se.select("div a")[0]['href']
                    _link = "https://en.wikipedia.org" + href
                    current_data['Link'] = _link
                    
                if article_size == 'True':
                    full_text = se.select("div.mw-search-result-data")[0].text
                    ft_text_split_1 = full_text.split(" (")
                    _article_size = ft_text_split_1[0]
                    current_data['Article Size'] = _article_size
                    
                if total_article_words == 'True':
                    ft_text_split_2 = ft_text_split_1[-1].split(") ")
                    _total_article_words = ft_text_split_2[0]
                    current_data['Total Article Words'] = _total_article_words

                if date == 'True':
                    _date = ft_text_split_2[-1].replace("- ", "")
                    current_data['Date'] = _date

                result_data.append(current_data)

            return result_data

        except Exception as e:
            print(e)

