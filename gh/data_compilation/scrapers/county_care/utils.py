import random
import time
import requests

# While USER_AGENTS_2 is the only user agent list currently being accessed,
# in the last scrape all three user agent lists were used at some point.
from .search_parameters.user_agents import USER_AGENTS_1, USER_AGENTS_2, USER_AGENTS_3
from .search_parameters.search_parameters import POST_DATA, PROVIDER_TYPES

# Posts made to this URL return the total possible number of search results on
# County Care's "Find a Provider" tool for a given search.
SEARCH_RESULTS_COUNT_URL = (
    "https://countycare.valence.care/member/rest/findAProvider/searchResultSize"
)

# This is the URL we post to in order to scrape the provider directory from
# County Care's website.
FIND_A_PROVIDER_URL = "https://countycare.valence.care/member/rest/findAProvider/search"

MANDATORY_FIELDS = [
    "providerTypeSelect",
    "mileRadiusForSearch",
    "mileRadius",
    "providerAddress",
    "searchAddress",
]


def ccare_post(
    search_values,
    url=FIND_A_PROVIDER_URL,
    monitoring=True,
    json_back=True,
    min_delay=4,
    max_delay=9,
    browser_list=USER_AGENTS_2,
):
    """
    Make a post to the find a provider part of county care's website with specific
    search parameters. This function sets a a random wait time before a post,
    selects a user-agent string to be used for the post and then uses an inputed
    dictionary of search terms to specify a post request.

    Inputs:

    search_values (dict of str:str pairs): A dictionary of "search_field", "search_value" pairs
    that specify which terms we are searching under on County Care's website. For
    the full list of possible fields, see POST_DATA in search_parameters/search_parameters.py.
    The mandatory fields to input into this function to get a response are:
    - "providerTypeSelect": A code that specifies which types of health care
       providers we are interested in. For the full list see "PROVDER_TYPES" under
       search_parameters/search_parameters.py.
    - "providerAddress": A string with a combination of the zipcode and state
       where we are searching form, such as: "60615, IL."
    - "searchAddress": A lat-long coordinate pair, given as a string, which specifies to county care
      the geographic point of reference it should use in querying providers.
    - "mileRadiusForSearch": A number, given as a string, that specifies how far
      out from "searchAddress" we want to look for matching providers.
    - "mileRadius": Same as above. This parameter is redundant, but the "Find A Provider"
       tool will not give a response without it.

    url (str): The url that we want to make a post to. The default is County
    Care's "find a provider" search url. We almost always want to use this url
    but this function does work, and is run with, the SEARCH_RESULTS_COUNT_URL
    above.

    monitoring (bool): A boolean value that tells our function if we want
    print statements on our terminal to inform us which specific query is
    being executed at a given minute. The default is true.

    json_back (bool): A boolean value that specifies if we want the output to
    be in json format, which is always the response value for this url.
    If set to false this function, will return the response object.

    min_delay (int): The minimum wait time before making a post.

    max_delay (int): The maximum wait time before making a post.

    browser_list (lst of strings): A specified list of browsers that
    the function can choose from in making the post. Three lists are accessed
    from the sub_directory search_parameters. If the user does not want to
    specify their own list, they are welcome to cycle through the three provided
    ones until all agents are on a watch list.

    returns: r or r.json(). The function returns the reponse object for a given
    request. The default is just to return the response in json format, but if
    json_back is set to False, this will return a requests "response" object.
    """

    # We randomly sets the wait before the post as a random float between a specified
    # minimum wait time and a specified maximum. The defaults are 4-9 seconds but you
    # might want to lower them if you are starting fresh and have not been flagged by
    # the website yet. The wait time is randomly selected so as to appear more
    # "human-like" to County Care's website.
    if min_delay > max_delay:
        raise ValueError(
            f"Could not execute post, the specified minimum delay of {min_delay}\
            seconds is greater than the specified maximum delay of {max_delay} seconds."
        )
    interval = max_delay - min_delay
    delay = min_delay + round(interval * (random.random()), 2)

    # We randomly select a different user-agent for every post. There are three
    # lists of user agents in search_parameters/user_agents, if one list is
    # getting a "connection closed without response" error frequently it is easy
    # to switch the user agents list by modifying the number next to
    # "USER_AGENTS_."
    max_length = len(browser_list)
    index = random.randrange(0, max_length, 1)
    headers = {"User-Agent": browser_list[index]}

    # check if all required keys are in the dictionary of post_data inputed to
    # this function.
    for parameter in MANDATORY_FIELDS:
        if parameter not in search_values.keys():
            raise ValueError(
                f"Could not complete post, mandatory search field {parameter}, must be included."
            )

    # We copy our global POST_DATA variable here so that the global variable
    # remains unchanged through iterations of posts.
    search_data = POST_DATA.copy()

    # We updated the copy of POST_DATA used on our post here to include the
    # searches specified in the search_values dictionary.
    for key, value in search_values.items():
        search_data[key] = value

    if monitoring is True:
        print("Waitin a few seconds before posting...")
    # Time to wait.
    time.sleep(delay)

    # This pulls out any search parameters beyond the required ones to use in
    # print statements while the scraper is running. Three of the fields in
    # MANDATORY_FIELDS are not informative as to which search is being run, so
    # we want to exclude those from our print statements.
    if monitoring is True:
        parameter_alerts = [
            search_values["searchAddress"],
            PROVIDER_TYPES[search_values["providerTypeSelect"]],
        ]
        for query, value in search_values.items():
            if query not in MANDATORY_FIELDS:
                parameter_alerts.append(value)
        query_string = ", ".join(parameter_alerts)
        print(f"Searching for County Care providers under: {query_string}")

    r = requests.post(url, json=search_data, headers=headers)

    # Most of the time, we just want the json data in the response back,
    # so we set that as the default, but we leave the option to specify returning
    # the response object for testing.
    if json_back is True:
        return r.json()

    return r
