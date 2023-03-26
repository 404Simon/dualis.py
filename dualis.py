import requests
import copy
from bs4 import BeautifulSoup
import re


class Dualis(object):
    """API Wrapper for the Dualis Website"""

    HTTP_METHODS = ['get', 'options', 'head', 'post', 'put', 'patch', 'delete']

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
        if loginRequest.status_code != 200:
            raise Exception("Login failed")
        else:
            print("Login successful")

        self.arguments = loginRequest.headers["REFRESH"].split("ARGUMENTS=")[1].split(",")[0]
        print(self.arguments)

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


    def getTimeTable(self):
        """Get the timetable from a student"""
        a = self.session.get(f"https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=SCHEDULER&ARGUMENTS={self.arguments},-N000028,-A,-A,-N0")  
        if a.status_code != 200:
            raise Exception("Request failed")

        # TODO parse the data more efficiently
        # TODO Selection day,week,month
        
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