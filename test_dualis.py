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
    
    def test_get_timetable_week_returns_empty_list(self):
        self.dualis.arguments = "email", "pass"
        with open('test_html/timetable_week_empty.html', 'r') as f:
            mock_response = f.read()
        expected_data = []
      
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = mock_response
            timetable = self.dualis.getTimeTableWeek(parse_date('01.01.2011'))
            
            self.assertEqual(timetable, expected_data)
            mock_get.assert_called_once()

    def test_get_timetable_week_mixed_returns_correct_list(self):
        self.dualis.arguments = "email", "pass"
        with open('test_html/timetable_week_mixed.html', 'r') as f:
            mock_response = f.read()
        example1 = Appointment(parse_date('12.08.1988'), parse_time('08:00'), parse_time('10:00'), 'ExampleSubject DFR-TNIP2055', 'DFR-088', None)
        example2 = Appointment(parse_date('08.08.1988'), parse_time('08:15'), parse_time('12:30'), 'Example Subject 2 DFR-TNIP2055', 'DFR-088', None)
        example3 = Appointment(parse_date('09.08.1988'), parse_time('09:00'), parse_time('12:30'), 'Workhard Subject DFR-TNIP2055', 'ROM-187', None)
        example4 = Appointment(parse_date('12.08.1988'), parse_time('10:15'), parse_time('12:30'), 'Subject42 Gr.C  DFR-TNIP2055', 'HOR-131', None)
        example5 = Appointment(parse_date('09.08.1988'), parse_time('13:00'), parse_time('16:30'), 'Interesting Subject  DFR-TNIP2055', 'MPQ-187', None)
        example6 = Appointment(parse_date('10.08.1988'), parse_time('13:00'), parse_time('16:30'), 'very Complex Subject  DFR-TNIP2055', 'MPQ-187', None)
        expected = [example1, example2, example3, example4, example5, example6]

        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = mock_response
            timetable = self.dualis.getTimeTableWeek(parse_date('08.08.1988'))
            
            assert timetable == expected
            mock_get.assert_called_once()
    