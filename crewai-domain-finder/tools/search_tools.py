import json
import os
from bs4 import BeautifulSoup
import requests
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

duck_search_tool=DuckDuckGoSearchRun()


class SearchTools():
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")

    @tool("Search the internet")
    def search_internet(self, query):
        """Useful to search the internet about a given topic and return relevant results"""
        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raises a HTTPError if the response status code is 4XX/5XX

            if 'organic' not in response.json():
                return "Sorry, I couldn't find anything about that, there could be an error with your SERPER API key."
            else:
                results = response.json()['organic']
                string = []
                for result in results[:top_result_to_return]:
                    string.append('\n'.join([
                        f"Title: {result['title']}", f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
                return '\n'.join(string)
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {str(e)}"
        
    @tool("fetch_company_data")
    def fetch_company_data(self, query):
        """Retrieve the entire data results from SERPER"""
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raises a HTTPError if the response status code is 4XX/5XX
            print(response)
            data = response.json()
            knowledge_graph = data.get('knowledgeGraph', {})
            return data, knowledge_graph
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {str(e)}")
            return {}

    def extract_top_links(self, data, links=None, max_links=5):
        """Recursively extracts up to 5 max_links links from the SERPER results."""
        if links is None:
            links = []

        if len(links) >= max_links:
            return links

        if isinstance(data, dict):
            for value in data.values():
                self.extract_top_links(value, links, max_links)
                if len(links) >= max_links:
                    break
        elif isinstance(data, list):
            for item in data:
                self.extract_top_links(item, links, max_links)
                if len(links) >= max_links:
                    break
        elif isinstance(data, str) and (data.startswith('http://') or data.startswith('https://')):
            links.append(data)

        return links[:max_links]

    @tool("link_extraction")
    def link_search(self, query):
        """Performs a links search to find domain links in the search results."""
        data = self.fetch_company_data(query)
        top_links = self.extract_top_links(data, links=None, max_links=5)
        print(json.dumps(top_links, indent=4))
        return top_links


@tool("parse webpage")
def parse_webpage(url):
    """Fetches a webpage by URL and parses all paragraph elements using Beautiful Soup.

    Args:
        url (str): The URL of the webpage to parse.

    Returns:
        list: A list of all paragraph texts found in the webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX

        # Parse the webpage content with Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all paragraph elements
        paragraphs = soup.find_all('p')
        paragraph_texts = [p.get_text() for p in paragraphs]
        
        return paragraph_texts
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the webpage: {str(e)}"
    except Exception as e:
        return f"An error occurred while parsing the webpage: {str(e)}"

