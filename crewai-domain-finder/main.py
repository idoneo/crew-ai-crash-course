from crewai import Crew
from textwrap import dedent
from agents import DataAgents
from tasks import DataTasks
from langchain_community.tools import DuckDuckGoSearchRun

from dotenv import load_dotenv
load_dotenv()


class DomainCrew:
    def __init__(self, company_name,headquarters,company_contact):
        self.company_name = company_name
        self.headquarters = headquarters
        self.company_contact = company_contact


    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = DataAgents()
        tasks = DataTasks()

        # Define your custom agents and tasks here
        expert_data_interpreter= agents.expert_data_interpreter()
        web_search_expert = agents.web_search_expert()
        data_extraction_expert = agents.data_extraction_expert()

        # Custom tasks include agent name and variables as input
        find_official_webpage = tasks.find_official_webpage(
            expert_data_interpreter,
            self.company_name,
            self.headquarters,
            self.company_contact
        )

        search_internet = tasks.search_internet(
            web_search_expert,
            self.company_name,
            self.headquarters,
            self.company_contact
        )

        parse_internet_data = tasks.parse_internet_data(
            data_extraction_expert,
            self.company_name,
            self.headquarters,
            self.company_contact
        )

        # Define your custom crew here
        crew = Crew(
            agents=[expert_data_interpreter,
                    web_search_expert,
                    data_extraction_expert
                    ],
            tasks=[
                find_official_webpage,
                search_internet,
                parse_internet_data
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to the GD Domian Finder Crew")
    print('-------------------------------')
    company_name = input(
        dedent("""
      What is the Company name?
    """))
    headquarters = input(
        dedent("""
      What is the headquarters location? (format as City, ST)
    """))
    company_contact = input(
        dedent("""
      Who is the Client contact? (only one name allowed)
    """))


    domain_crew = DomainCrew(company_name, headquarters,company_contact)
    result = domain_crew.run()
    print("\n\n########################")
    print("## Here are the results ")
    print("########################\n")
    print(result)
