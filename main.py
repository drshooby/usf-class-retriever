import json
import os

import requests

from course import Course
from cookies import get_cookies_from_login

url = "https://reg-prod.ec.usfca.edu/StudentRegistrationSsb/ssb/searchResults/searchResults"
params = {
    "txt_subject": "CS",
    "txt_term": "202520",
    "startDatepicker": "",
    "endDatepicker": "",
    "pageOffset": "0",
    "pageMaxSize": "10",
    "sortColumn": "subjectDescription",
    "sortDirection": "asc"
}

# Define the headers
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.8",
    "Referer": "https://reg-prod.ec.usfca.edu/StudentRegistrationSsb/ssb/classRegistration/classRegistration",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

def parse_json(data):
    courses = []
    class_info = data["data"]
    for item in class_info:
        term = item["termDesc"]
        subject = item["subject"]
        course_title = item["courseTitle"]
        course_number = item["courseNumber"]
        faculty_info = item["faculty"][0]
        prof_name = faculty_info["displayName"]
        prof_email = faculty_info["emailAddress"]
        meeting_info = item["meetingsFaculty"][0]["meetingTime"]
        building = meeting_info["building"]
        room = meeting_info["room"]
        meeting_type = meeting_info["meetingTypeDescription"]
        start_time = meeting_info["beginTime"]
        end_time = meeting_info["endTime"]
        days = [day for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] if meeting_info[day]]
        c = Course(subject=subject,
                   course_title=course_title,
                   course_number=course_number,
                   prof_name=prof_name,
                   prof_email=prof_email,
                   term=term,
                   building=building,
                   room=room,
                   days=days,
                   meeting_type=meeting_type,
                   start_time=start_time,
                   end_time=end_time,
                   )
        courses.append(c)
    return courses

sem_translate = {
    "fall": "10",
    "spring": "20",
    "summer": "30"
}

if __name__ == "__main__":

    cookies = None
    if not os.path.exists("cookies.txt"):
        print("Could not find cookies.txt. Fetching cookies...")
        cookies = get_cookies_from_login(sem_translate["spring"], 2025)
        if not cookies:
            exit(1)
        with open("cookies.txt", "w") as f:
            json.dump(cookies, f)
    else:
        print("Found cookies.txt. Fetching cookies...")
        with open("cookies.txt", "r") as f:
            cookies = json.load(f)

    page_offset = 0
    while True:
        print("Current page offset: ", page_offset)

        response = requests.get(url, headers=headers, params=params, cookies=cookies)
        json_data = response.json()

        c = parse_json(response.json())
        for course in c:
            print(course)

        if len(c) < 10:
            break

        i = input("Would you like to keep viewing classes (y/n): ")
        if i == "y" or i == "Y":
            page_offset += 10
            params["pageOffset"] = str(page_offset)
        else:
            break