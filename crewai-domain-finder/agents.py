from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

from tools.search_tools import SearchTools
from tools.fuzzymatch_tools import FuzzyMatchTools
from tools.search_tools import *


class DataAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        #self.Ollama=Ollama(model="openhermes")

    def expert_data_interpreter(self):
        return Agent(
            role="Expert Data Interpreter",
            backstory=dedent(
                f"""Expert in finding connections in disparate data content. 
                I have decades of experience in all types of data formats."""),
            goal=dedent(f"""
                        Given 3 parameters, Company Name, Company Headquarters and Company Contact, find the 
                        most likely official website for the company. 
                        """),
            tools=[
                SearchTools.search_internet,
                FuzzyMatchTools.fuzzymatch
            ],
            verbose=True,
            allow_delegation=True,
            llm=self.OpenAIGPT4,
        )

    def web_search_expert(self):
        return Agent(
            role="Web Search Expert",
            backstory=dedent(f"""Knowledgeable in using best search engine optimization query techniques to
                             get the best results from a Google Serper web search"""),
            goal=dedent(
                f"""Use the provided parameters to get the most detailed and relevant information"""),
            tools=[SearchTools.search_internet,SearchTools.fetch_company_data],
            verbose=True,
            allow_delegation=False,
            llm=self.OpenAIGPT4,
        )
    def data_extraction_expert(self):
        return Agent(
            role="Data Extraction Expert",
            backstory=dedent(
                f"""Expert at parsing HTML and finding key values that are related to the 
                given parameters"""),
            goal=dedent(
                f"""Find the most relevnt url links and create expertly curated infomation from scraped 
                HTML pages and search results by focusing on the goal of finding the Official webpage
                """),
            tools=[SearchTools.link_search,duck_search_tool,parse_webpage],
            verbose=True,
            allow_delegation=False,
            llm=self.OpenAIGPT4,
            )
