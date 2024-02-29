import requests
import math
from datetime import datetime
from bs4 import BeautifulSoup

def get_meeting_information(meeting_url, cookies):
    
    """
    The get_meeting_information function takes in a meeting_url and cookies as parameters.
    The function then makes a GET request to the meeting_url using the cookies provided.
    The response is converted into JSON format, and attendees are extracted from it. 
    A for loop iterates through each attendee's information, extracting their id, name, duration (in minutes), join time string (Join Time), and leave time string (Leave Time). 
    Each attendee's information is stored in an output dictionary which is appended to data list that will be returned by this function.
    
    :param meeting_url: Specify the url of the meeting you want to get information from
    :param cookies: Pass the cookies from the login function to this function
    :return: A list of dictionaries
    :doc-author: Sabari
    """
    response = requests.get(
        meeting_url,
        cookies=cookies
    ).json()
    attendees = response["attendees"]
    data = []
    for response in attendees:
        output = {
            "id": response["id"],
            "name": response["name"],
            "duration": math.ceil(response["duration"]/60),
            "Join Time": response["joinTimeStr"],
            "Leave Time": response["leaveTimeStr"],
        }
        data.append(output)

    return data   

def get_meeting_ids(report_url, cookies):
    
    """
    The get_meeting_ids function takes in a report_url and cookies,
        then returns a list of meeting ids and the total number of meetings.
        
        Args:
            report_url (str): The url to the Zoom Report page.
            cookies (dict): A dictionary containing your session cookie information.
    
    :param report_url: Get the meeting ids
    :param cookies: Authenticate the user
    :return: A tuple with the meeting ids and the total number of meetings
    :doc-author: Sabari
    """
    response = requests.get(
        report_url,
        cookies=cookies
    )

    soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    table = soup.find("table", {"id": "meeting_list"})
    a_tags = table.find_all("a")
    # https://us06web.zoom.us/account/my/report/participants/list?meetingId=sFkYred8TISmhrUZv7y62g%3D%3D&accountId=c_FufX0BTD-vfbPY_piJug
    meeting_ids = []
    for a_tag in a_tags:
        meeting_ids.append(a_tag.attrs["data-id"])
    total = soup.find("span", {"name": "totalRecords"}).text
    # next_element_class = soup.find("div", {"id": "paginationDivMeeting"}).find_all("li")[1].attrs["class"]
    return meeting_ids, int(total)

def load_cookies_from_file(filename):
    """
    The load_cookies_from_file function takes a filename as an argument and returns a dictionary of cookies.
    The file should contain the contents of the browser's cookie jar, one cookie per line.
    
    :param filename: Specify the file that contains the cookies
    :return: A dictionary of cookies
    :doc-author: Sabari
    """
    lines = []
    with open(filename, "r") as f:
        lines = f.readlines()
    cookies_string = "".join(lines).replace("\n", "")
    cookies = {}
    for cookie in cookies_string.split(";"):
        try:
            key, value = cookie.split("=")
            cookies[key] = value
        except:
            pass
    return cookies

def get_last_day_of_month(month=None, year=None):
    """
    The get_last_day_of_month function returns the last day of the month for a given date.
        Args:
            None.
        Returns: 
            The last day of the month as a datetime object.
    
    :return: The last day of the month
    :doc-author: Sabari
    """
    today = datetime.now()
    if not year:
        year = today.year
    if not month:
        month = today.month
    day = 31
    while True:
        try:
            date = datetime(year, month, day)
            break
        except ValueError as e:
            if "day is out of range" in str(e):
                day -= 1
            else:
                break
    return date


def generate_report(cookies, user_id, start_date=None, end_date=None):
    
    """
    The generate_report function takes in a user's cookies, user_id, start_date and end_date.
    It then uses the get_last_day function to determine the last day of the month. It then creates a report url using 
    the date information and gets all meeting ids for that day from that url. Then it loops through each meeting id and creates
    a new url with that id to get participant information for each meeting on that day.
    
    :param cookies: Pass in the cookies that are needed to access the zoom api
    :param user_id: Specify the user id of the zoom account
    :param start_date: Set the starting date for the report
    :param end_date: Specify the end date of the report
    :return: A list of dictionaries
    :doc-author: Sabari
    """
    date = get_last_day_of_month()
    year = date.year
    month = date.month

    meeting_participant_info = []
    for day in range(1, date.day + 1):
        report_url = f'https://zoom.us/account/my/report?from={month}/{day}/{year}&to={month}/{day}/{year}&id={id}#'
        meeting_ids = get_meeting_ids(report_url, cookies)
        for meeting_id in meeting_ids:
            meeting_url = f"https://us06web.zoom.us/account/my/report/participants/list?meetingId={meeting_id}&accountId={user_id}"
            meeting_info = get_meeting_information(meeting_url, cookies)
            meeting_participant_info.extend(meeting_info)