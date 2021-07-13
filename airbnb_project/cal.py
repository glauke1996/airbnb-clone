import calendar


class Calendar:
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.day_names = ("Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun")
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
