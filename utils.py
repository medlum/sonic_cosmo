from bs4 import BeautifulSoup
import requests
import datetime
import json
from youtubesearchpython import VideosSearch


def contains_any_keyword(string: str, keywords: list) -> bool:
    # Convert the string to lowercase for case-insensitive comparison
    string_lower = string.lower()
    # Check if any keyword is in the string
    return any(keyword.lower() in string_lower for keyword in keywords)


def video_search(query: str) -> str:
    videosSearch = VideosSearch(query, limit=1)
    search = videosSearch.result()
    for key in search["result"]:
        link = key['link'][32:]
    return f"https://www.youtube.com/embed/{link}"


def news_headlines():
    url = "https://www.channelnewsasia.com"
    response = requests.get(url)
    if response.status_code == 200:
        news = []
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find('body').find_all('h6')  # headlines at h6
        for index, headline in enumerate(headlines):
            news.append(f"{index+1}. {headline.text.strip()}.")
            if index == 10:
                break
        return '\n'.join(news)
    else:
        return "No response from news provider."


def timer():
    weekdays_map = {i: ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday', 'Sunday'][i] for i in range(7)}
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    day = weekdays_map[current_datetime.weekday()]
    return formatted_datetime, day


def weather_forecast():
    url = "https://api-open.data.gov.sg/v2/real-time/api/twenty-four-hr-forecast"
    res = requests.get(url)
    data = json.dumps(res.json(), indent=4)
    return data


news_var = news_headlines()
datetime_var = timer()
weather_var = weather_forecast()

# custom CSS for buttons
custom_css = """
<style>
    .stButton > button {
        color: #383736; 
        border: none; /* No border */
        padding: 5px 22px; /* Reduced top and bottom padding */
        text-align: center; /* Centered text */
        text-decoration: none; /* No underline */
        display: inline-block; /* Inline-block */
        font-size: 8px !important;
        margin: 4px 2px; /* Some margin */
        cursor: pointer; /* Pointer cursor on hover */
        border-radius: 30px; /* Rounded corners */
        transition: background-color 0.3s; /* Smooth background transition */
    }
    .stButton > button:hover {
        color: #383736; 
        background-color: #c4c2c0; /* Darker green on hover */
    }
</style>
"""

# ------ set up question button -----#

EXAMPLE_PROMPTS = [
    "Latest News",
    "Weather forecast",
    "Translate in Chinese",
    "Eric Clapton - Tears In Heaven (Official Video)",
]


intro = """
Meet Sonic Cosmo, your ultimate conversational companion! By harnessing the cutting-edge technology of HuggingFace's InferenceClient and the latest Large Language Models, Sonic Cosmo brings together the perfect blend of intelligence and charm. With its super-speedy responses and warm, friendly demeanor, Sonic Cosmo is always ready to lend a helping hand - whether you're tackling tricky homework, exploring new hobbies, or just need someone to share your thoughts with. So why wait? Dive into a conversation with Sonic Cosmo and discover a world of helpful, engaging, and lightning-fast interactions that will leave you smiling!
"""
