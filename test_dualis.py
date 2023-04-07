import unittest
from unittest.mock import patch
from datetime import datetime

from dualis import Dualis

def parse_date(date: str) -> datetime.date:
    """Parses a date string (ex. 25.01.2000) to a datetime.date object."""
    return datetime.strptime(date, '%d.%m.%Y')


class DualisTest(unittest.TestCase):
    def setUp(self):
        self.dualis = Dualis()
    
    def test_get_timetable_week_returns_empty_list(self):
        self.dualis.arguments = "email", "pass"
        mock_response = '<html><body></body></html>'
        expected_data = []
      
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = mock_response
            timetable = self.dualis.getTimeTableWeek(parse_date('01.01.2011'))
            
            self.assertEqual(timetable, expected_data)
            mock_get.assert_called_once()
    