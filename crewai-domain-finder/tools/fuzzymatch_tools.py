import json
import os
import fuzzywuzzy

import requests
from langchain.tools import tool

class FuzzyMatchTools():

    @tool("Fuzzily Match Strings")
    def fuzzymatch():
        """
        This tool will calculate the Levenstien distance between 2 strings
        """
        pass