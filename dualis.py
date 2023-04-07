#!/usr/bin/env python # [1]
"""\
Dualis API Wrapper

Usage: import dualis and initialize with dualis.Dualis()
Author: pvhil
"""
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from models import Appointment



WOCHENTAGE = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

class Dualis(object):
    """API Wrapper for the Dualis Website"""

    def __init__(self, username=None, password=None):
        """Constructor
        Arguments:
            username -- username of the Dualis Account
            password -- password of the Dualis Account
        """
        self.session = requests.Session()
        if username and password:
            self.login(username, password)


    def login(self, username, password):
        """Login to Dualis
        Arguments:
            username -- username of the Dualis Account
            password -- password of the Dualis Account
        """
        self.username = username
        self.password = password

        loginRequest = self.session.post("https://dualis.dhbw.de/scripts/mgrqispi.dll", data=
            f"usrname={self.username}&pass={self.password}&APPNAME=CampusNet&PRGNAME=LOGINCHECK&ARGUMENTS=clino%2Cusrname%2Cpass%2Cmenuno%2Cmenu_type%2Cbrowser%2Cplatform&clino=000000000000001&menuno=000324&menu_type=classic&browser=&platform="
        )
        if loginRequest.status_code != 200 or loginRequest.headers["REFRESH"].split("ARGUMENTS=")[1].split(",")[0] == "":
            raise Exception("Login failed")
        else:
            print("Login successful")

        self.arguments = loginRequest.headers["REFRESH"].split("ARGUMENTS=")[1].split(",")[0]

    def getTodayEvents(self):
        """Get all events for today"""
        a = self.session.get("https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=MLSSTART&ARGUMENTS="+self.arguments+",-N000019,-N000000000000000")
        if a.status_code != 200:
            raise Exception("Request failed")
        
        soup = BeautifulSoup(a.text, 'html.parser')
        table = soup.findAll("div", {"class": "tb rw-table"})[0]
        return table
        # I dont have an example for this, so I cant test it or parse it

    def getNewMessages(self):
        """Get all new messages"""
        a = self.session.get("https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=MLSSTART&ARGUMENTS="+self.arguments+",-N000019,-N000000000000000")
        if a.status_code != 200:
            raise Exception("Request failed")
        
        soup = BeautifulSoup(a.text, 'html.parser')
        table = soup.findAll("div", {"class": "tb rw-table"})[1]
        return table
        # I dont have an example for this, so I cant test it or parse it

    def getExamResults(self):
        """Get all exam results"""
        a = self.session.get("https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSERESULTS&ARGUMENTS="+self.arguments+",-N000307,")
        if a.status_code != 200:
            raise Exception("Request failed")

        # TODO Selection of semester
        
        soup = BeautifulSoup(a.text, 'html.parser')
        table = soup.find("table", {"class": "nb list"})
        data = {}
        tbody = table.find('tbody')

        for tr in tbody.find_all('tr'):
            temp = {}
            for td in tr.find_all('td'):
                if not td.get_text().replace("\r", "").replace("\t", "").replace("\n", "").replace(" ", "").replace("\xa0"," ") == "" and not td.get_text().replace("\r", "").replace("\t", "").replace("\n", "").replace(" ", "").replace("\xa0"," ") == " ":
                    temp[len(temp)] = re.sub(" +"," ",td.get_text().replace("\r", "").replace("\t", "").replace("\n", "").replace("\xa0"," "))
            data[len(data)] = temp
        return data


    def getPerformance(self): 
        """Get the performance from a student"""
        a = self.session.get(f"https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=STUDENT_RESULT&ARGUMENTS={self.arguments},-N000310,-N0,-N000000000000000,-N000000000000000,-N000000000000000,-N0,-N000000000000000")
        if a.status_code != 200:
            raise Exception("Request failed")

        # TODO parse the data more efficiently
        # TODO Selection of semester
        
        soup = BeautifulSoup(a.text, 'html.parser')
        table = soup.find("table", {"class": "nb list students_results"})
        data = {}
        tbody = table.find('tbody')
        for tr in tbody.find_all('tr'):
            temp = {}
            for td in tr.find_all('td'):
                if not td.get_text().replace("\r", "").replace("\t", "").replace("\n", "").replace(" ", "").replace("\xa0"," ") == "" and not td.get_text().replace("\r", "").replace("\t", "").replace("\n", "").replace(" ", "").replace("\xa0"," ") == " ":
                    temp[len(temp)] = re.sub(" +"," ",td.get_text().replace("\r", "").replace("\t", "").replace("\n", "").replace("\xa0"," "))
            data[len(data)] = temp
        return data


    def getTimeTableDay(self,date=None):
        """Get the timetable from a student
        Arguments:
            date -- date as a string (DD.MM.YYYY)
        """
        if date==None:
            a = self.session.get(f"https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=SCHEDULER&ARGUMENTS={self.arguments},-N000028,-A,-A,-N0")  
        else:
            a = self.session.get(f"https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=SCHEDULER&ARGUMENTS={self.arguments},-N000028,-A{date},-AN,-A,-N0")
        if a.status_code != 200:
            raise Exception("Request failed")

        # TODO parse the data more efficiently
        # TODO Selection day,week,month
        
        soup = BeautifulSoup(a.text, 'html.parser')
        table = soup.find("div", {"id": "scheduler"}).find("table",{ "class": "nb"})
        data = {}
        #tbody = table.find('tbody')
        for tr in table.find_all('tr'):
            temp = {}
            for th in tr.find_all('th'):
                temp["time"] = re.sub(" +"," ",th.get_text().replace("\r", "").replace("\t", "").replace("\n", "").replace("\xa0"," "))
            for td in tr.find_all('td'):
                temp["data"] = re.sub(" +"," ",td.get_text().replace("\r", "").replace("\t", "").replace("\n", "").replace("\xa0"," "))
            data[len(data)] = temp
        return data

    def getTimeTableWeek(self,date: datetime.date = None) -> list:
        """Get the timetable from a student
        Arguments:
            date -- date as a datetime.date object
        """
        if date is None: date = datetime.date.today()
        a = self.session.get(f"https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=SCHEDULER&ARGUMENTS={self.arguments},-N000030,-A{date.strftime('%d/%m/%Y')},-A,-N1,-N0,-N0")
        
        if a.status_code != 200:
            raise Exception("Request failed")

        # TODO Selection day,week,month ?
        
        soup = BeautifulSoup(a.text, 'html.parser')
        appointments = soup.find_all('td', class_='appointment')
        if not appointments:
            return []

        appointment_list = []
        for appointment in appointments:
            soup = BeautifulSoup(str(appointment), 'html.parser')
            appointment_date = appointment['abbr'].split(' ')[0]
            if appointment_date not in WOCHENTAGE: continue
            appointment_date = date + timedelta(days=WOCHENTAGE.index(appointment_date) - date.weekday())

            subject = soup.find('a', class_='link')['title']
            time_period = soup.find('span', class_='timePeriod')
            time_str = time_period.text.strip()[:13]
            room_element = time_period.find('a', class_='arrow')
            room = time_period.text.replace(time_str, '').strip() if room_element is None else room_element.text.strip()            
            start_time, end_time = [datetime.strptime(t.strip(), '%H:%M').time() for t in time_str.split('-')]
            appointment_list.append(Appointment(appointment_date, start_time, end_time, subject, room, None))
        return appointment_list

    @DeprecationWarning
    def getTimeTableMonth(self,date=None):
        """Deprecated, parsing not tested, wont work"""

        """Get the timetable from a student
        Arguments:
            date -- date as a string (DD/MM/YYYY)
        """
        if date==None:
            a = self.session.get(f"https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=SCHEDULER&ARGUMENTS={self.arguments},-N000030,-A,-A,-N1")  
        else:
            a = self.session.get(f"https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=SCHEDULER&ARGUMENTS={self.arguments},-N000030,-{date},-A,-N1,-N0,-N0")
        if a.status_code != 200:
            raise Exception("Request failed")

        # TODO parse the data more efficiently
        # TODO No Example for testing, parsing will not work. Need help
        
        soup = BeautifulSoup(a.text, 'html.parser')
        table = soup.find("div", {"id": "tb tbMonthContainer"}).find("table",{ "class": "nb"})
        data = {}
        #tbody = table.find('tbody')
        for tr in table.find_all('tr'):
            # skip if tr has tbsubhead as class
            if tr.get("class") == ["tbsubhead"]:
                continue
            if tr.find_all("td")[0].get("class") == ["tbcontrol"]:
                continue
            temp = {}
            for th in tr.find_all('th'):                
                temp[len(temp)] = re.sub(" +"," ",th.get_text().replace("\r", "").replace("\t", "").replace("\n", "").replace("\xa0"," "))
            for td in tr.find_all('td'):
                temp[len(temp)] = re.sub(" +"," ",td.get_text().replace("\r", "").replace("\t", "").replace("\n", "").replace("\xa0"," "))
            data[len(data)] = temp

        return data

