from dataclasses import dataclass
import datetime

@dataclass
class Appointment:
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    subject: str
    room: str
    teacher: str
    def __repr__(self):
        return f'{self.date.strftime("%d.%m.%Y")} ({self.start_time.strftime("%H:%M")} - {self.end_time.strftime("%H:%M")}) - {self.subject} - {self.room} - {self.teacher}'
    