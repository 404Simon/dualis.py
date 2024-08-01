from datetime import datetime
import dualis

def parse_date(date: str) -> datetime.date:
    """Parses a date string (ex. 25.01.2000) to a datetime.date object."""
    return datetime.strptime(date, '%d.%m.%Y')



## Examples ##

test = dualis.Dualis("email", "pass")

print(test.get_exam_results())
print(test.get_new_messages())
print(test.get_performance())
print(test.get_time_table_day())
print(test.get_time_table_week(parse_date('05.05.2055')))
print(test.get_exam_results())

