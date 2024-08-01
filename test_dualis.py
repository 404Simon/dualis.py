import unittest
from unittest.mock import patch
from datetime import datetime

from dualis import Dualis
from models import Appointment

def parse_date(date: str) -> datetime.date:
    """Parses a date string (ex. 25.01.2000) to a datetime.date object."""
    return datetime.strptime(date, '%d.%m.%Y')

def parse_time(time: str) -> datetime.time:
    """Parses a time string (ex. 12:00) to a datetime.time object."""
    return datetime.strptime(time, '%H:%M').time()


class DualisTest(unittest.TestCase):
    def setUp(self):
        self.dualis = Dualis()



    def test_get_timetable_week_requests_correct_url(self):
        arguments = "email", "pass"
        self.dualis.arguments = arguments
        date = parse_date('01.01.2011')
        expected_url = f"https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=SCHEDULER&ARGUMENTS={arguments},-N000030,-A{date.strftime('%d/%m/%Y')},-A,-N1,-N0,-N0"
        with patch('requests.Session.get') as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.text = ""
            self.dualis.get_time_table_week(date)

        mock_request.assert_called_once_with(expected_url)
        

    
    def test_get_timetable_week_returns_empty_list(self):
        self.dualis.arguments = "email", "pass"
        with open('test_html/timetable_week_empty.html', 'r') as f:
            mock_response = f.read()
        expected_data = []
      
        with patch('requests.Session.get') as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.text = mock_response
            timetable = self.dualis.get_time_table_week(parse_date('01.01.2011'))
            
            self.assertEqual(timetable, expected_data)
            mock_request.assert_called_once()
    


    def test_get_timetable_week_room_in_arrow_parses_appointment_correctly(self):
        self.dualis.arguments = "email", "pass"
        mock_response = """
            <td class="appointment" style="background-color: #ffff00" rowspan="8" abbr="Freitag Spalte 1">
                <span style="font: 9px Arial" class="timePeriod">
                    08:00 - 10:00
                    <a class="arrow" style="font-size: inherit" href="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-asdefasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfsadfsadfasdfasdfasdfasdfasdfasdfsadfsadfsadfasdfsadfsadfdsafasdfsadfsadfsadfsadfasdfasdfasdfasdfsadfasdfsadfasdfsadfsadfasdfasdfasdf">
                    DFR-088
                    </a>
                </span>
                <br />
                <a href="/scripts/mgrqispi.dll?APPNAME=CampusNet&amp;PRGNAME=COURSEPREP&amp;ARGUMENTS=-N187187187187187,-N187187,-N0,-N345476786797656,-JDKCD,-N234658476593446" class="link" title="ExampleSubject DFR-TNIP2055">
                    ExampleSubject1
                </a>
            </td>
        """
        expected_data = [Appointment(parse_date('31.12.2010'), parse_time('08:00'), parse_time('10:00'), 'ExampleSubject DFR-TNIP2055', 'DFR-088', None)]
      
        with patch('requests.Session.get') as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.text = mock_response
            timetable = self.dualis.get_time_table_week(parse_date('01.01.2011'))
            
            self.assertEqual(timetable, expected_data)
            mock_request.assert_called_once()



    def test_get_timetable_week_room_in_timePeriod_parses_appointment_correctly(self):
        self.dualis.arguments = "email", "pass"
        mock_response = """
            <td class="appointment" style="background-color: #ffff00" rowspan="14" abbr="Dienstag Spalte 1">
                <span style="font: 9px Arial" class="timePeriod">
                    09:00 - 12:30 ROM-187
                </span>
                <br />
                <a href="/scripts/mgrqispi.dll?APPNAME=CampusNet&amp;PRGNAME=COURSEPREP&amp;ARGUMENTS=-N187187187187187,-N187187,-N0,-N290374280238947,-JDKCD,-N290374280238947" class="link" title="Workhard Subject DFR-TNIP2055">
                    Another Example Subject
                </a>
            </td>
        """
        expected_data = [Appointment(parse_date('28.12.2010'), parse_time('09:00'), parse_time('12:30'), 'Workhard Subject DFR-TNIP2055', 'ROM-187', None)]

        with patch('requests.Session.get') as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.text = mock_response
            timetable = self.dualis.get_time_table_week(parse_date('01.01.2011'))
            
            self.assertEqual(timetable, expected_data)
            mock_request.assert_called_once()



    def test_get_timetable_week_mixed_returns_correct_list(self):
        arguments = "email", "pass"
        self.dualis.arguments = arguments
        with open('test_html/timetable_week_mixed.html', 'r') as f:
            mock_response = f.read()
        example1 = Appointment(parse_date('12.08.1988'), parse_time('08:00'), parse_time('10:00'), 'ExampleSubject DFR-TNIP2055', 'DFR-088', None)
        example2 = Appointment(parse_date('08.08.1988'), parse_time('08:15'), parse_time('12:30'), 'Example Subject 2 DFR-TNIP2055', 'DFR-088', None)
        example3 = Appointment(parse_date('09.08.1988'), parse_time('09:00'), parse_time('12:30'), 'Workhard Subject DFR-TNIP2055', 'ROM-187', None)
        example4 = Appointment(parse_date('12.08.1988'), parse_time('10:15'), parse_time('12:30'), 'Subject42 Gr.C  DFR-TNIP2055', 'HOR-131', None)
        example5 = Appointment(parse_date('09.08.1988'), parse_time('13:00'), parse_time('16:30'), 'Interesting Subject  DFR-TNIP2055', 'MPQ-187', None)
        example6 = Appointment(parse_date('10.08.1988'), parse_time('13:00'), parse_time('16:30'), 'very Complex Subject  DFR-TNIP2055', 'MPQ-187', None)
        expected = [example1, example2, example3, example4, example5, example6]

        with patch('requests.Session.get') as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.text = mock_response
            date = parse_date('08.08.1988')
            timetable = self.dualis.get_time_table_week(date)
            
            mock_request.assert_called_once()
            assert timetable == expected



    def test_get_timetable_week_status_404_raises_exception(self):
        self.dualis.arguments = "email", "pass"
        with patch('requests.Session.get') as mock_request:
            mock_request.return_value.status_code = 404
            with self.assertRaises(Exception):
                self.dualis.get_time_table_week(parse_date('01.01.2011'))
            mock_request.assert_called_once()


if __name__ == '__main__':
    unittest.main()

