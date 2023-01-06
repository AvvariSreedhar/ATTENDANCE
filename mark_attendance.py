import requests
import getpass
import os

from dotenv import load_dotenv
from cisco_modules import *

def main():

    load_dotenv()

    StSession = "2022-23"

    # CONNECT TO IITR VPN
    auth_cisco_vpn(os.getenv('VPN_USERNAME'), os.getenv(
        'VPN_PASSWORD'), "vpn.iitr.ac.in")

    r = requests.Session()

    # LOGIN
    print("\nEnter the credentials for login (same as Channeli): ")

    while (True):
        username = input("username: ")
        password = getpass.getpass("password: ")

        login_data = {
            "username": username,
            "password": password
        }
        login = r.post("http://10.22.0.107:8000/api/login", json=login_data)
        login = login.json()

        if login["status"] is False:
            print("Invalid credentials. Please try again!\n")
        else:
            break

    # UPDATING SESSION HEADERS
    r.headers.update({"username": username})
    r.headers.update({"token": login["data"]["AccessToken"]})

    # GET STUDENT INFO
    student_info_data = {
        "EnrollmentNo": username
    }
    student_info = r.post(
        "http://10.22.0.107:8000/api/student/getStudentInfo", json=student_info_data)
    student_info = student_info.json()

    # GET STUDENT REGISTERED SUBJECTS
    student_registered_subjects_data = {
        "EnrollmentNo": username,
        "SemesterID": student_info["data"]["SemesterID"],
        "StSession": StSession
    }
    student_registered_subjects = r.post(
        "http://10.22.0.107:8000/api/student/getStudentRegisteredSubjects", json=student_registered_subjects_data)
    student_registered_subjects = student_registered_subjects.json()

    # MARK ATTENDANCE
    print(f"\n\nHey {student_info['data']['Name']}!")
    print("Choose the subject to mark attendance:\n")
    for idx, course in enumerate(student_registered_subjects["data"]):
        print(
            f"  ---> {idx} for {course['SubjectName']} [{course['SubjectAlphaCode']}]")

    course = -1
    while (True):
        course = int(input())

        if (course < 0 or course > len(student_registered_subjects["data"])-1):
            print("Invalid course. Please select a valid course")
        else:
            break

    data = {
        "SubjectId": student_registered_subjects["data"][course]["SubjectID"],
        "ProgramID": student_registered_subjects["data"][course]["ProgrameID"],
        "SubjectCode": student_registered_subjects["data"][course]["SubjectAlphaCode"],
        "FacultyId": student_registered_subjects["data"][course]["FacultyIDs"],
        "EnrollmentNo": username,
        "Name": student_info["data"]["Name"]
    }

    response = r.post(
        "http://10.22.0.107:8000/api/student/markAttendance", json=data)
    response = response.json()

    print("\n", response)

    disconnect_cisco_vpn()


if __name__ == "__main__":
    main()
