import calendar
from django.utils import timezone


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat")
        self.months = (
            "January",
            "Feburary",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "Setember",
            "October",
            "November",
            "December",
        )

    def get_month(self):
        return self.months[self.month - 1]

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []

        for week in weeks:
            for day, _ in week:
                now = timezone.now()
                today = now.day
                past = False
                month = now.month
                if self.month == month and today >= day:
                    past = True
                new_day = Day(day, past, self.month, self.year)
                days.append(new_day)

        return days


class Day:
    def __init__(self, number, past, month, year):
        self.number = number
        self.past = past  # boolean
        self.month = month
        self.year = year

    def __str__(self):
        return str(self.number)
