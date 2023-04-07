from datetime import datetime
import dualis

def parse_date(date: str) -> datetime.date:
    """Parses a date string (ex. 25.01.2000) to a datetime.date object."""
    return datetime.strptime(date, '%d.%m.%Y')



## Examples ##

test = dualis.Dualis("email", "pass")

print(test.getExamResults())
print(test.getNewMessages())
print(test.getPerformance())
print(test.getTimeTableDay())
print(test.getTimeTableWeek(parse_date('05.05.2055')))
print(test.getTimeTableMonth())
print(test.getTodayEvents())
print(test.getExamResults())
