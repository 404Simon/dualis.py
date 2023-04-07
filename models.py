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