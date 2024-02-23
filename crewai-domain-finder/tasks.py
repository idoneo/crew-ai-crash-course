from crewai import Task
from textwrap import dedent


class DataTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 salary boost!"

    def find_official_webpage(self,agent,company_name,headquarters,company_contact):
        return Task(
            description=dedent(
                f"""
            **Task**: Find the Official Webpage
            **Description**: Given the 3 parameters, find the most likely official webpage for the Company.Matching the parameters
            to available information on the internet compare Company Name and Headquarters location, find relevant high level company employees
            such as CEO, Founders, COO, Investors and other high level stakeholders that may align with the Company Contact. If the company contact
            has a sub-page on the website then that should be considered highly significant. Domain names sometimes do not have the exact
            company name,find other information in the retrieved data that may signify a match.Use Fuzzy Matchng for Company Names and Company Contacts as there may be slight variations in spelling. For Headquarters location it does not have to be exact. 
            There may be more than one Headquarters and the parameter should be considered a match if any one of the headquarters is a match. 
            Also the Headquarter actual location can be approximate, For example If the Headquarters is Brooklyn, NY and the retrieved information
            data headquarters is New York, NY then this is a match, because Brooklyn is in New York. If you decide you have found a match.
            You MUST state why it is a match, include fuzzy match statistics if available

            **Parameters**: 
            - Company Name: {company_name}
            - Headquarters: {headquarters}
            - Company Contact: {company_contact}

            **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
        )

    def search_internet(self, agent, company_name,headquarters,company_contact):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Search the internet for information using the parameters
                    **Description**: Analyze and select the best city for the trip based on specific 
                        criteria such as weather patterns, seasonal events, and travel costs. 
                        This task involves comparing multiple cities, considering factors like current weather 
                        conditions, upcoming cultural or seasonal events, and overall travel expenses. 
                        Your final answer must be a detailed report on the chosen city, 
                        including actual flight costs, weather forecast, and attractions.


                **Parameters**: 
                - Company Name: {company_name}
                - Headquarters: {headquarters}
                - Company Contact: {company_contact}

                **Note**: {self.__tip_section()}
            """
            ),
            agent=agent,
        )

    def parse_internet_data(self, agent, company_name,headquarters,company_contact):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Use the search results and parse out relevant information
                    **Description**: Parse out the data from the relevant web pages retrieved in the search
                    find key values that align with the parameters.

                **Parameters**: 
                - Company Name: {company_name}
                - Headquarters: {headquarters}
                - Company Contact: {company_contact}

                **Note**: {self.__tip_section()}
            """
            ),
            agent=agent,
        )
