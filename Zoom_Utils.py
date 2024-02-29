import requests
import math
from datetime import datetime
from bs4 import BeautifulSoup

def get_meeting_information(meeting_url, cookies):
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
    :doc-author: Trelent
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
    :doc-author: Trelent
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
