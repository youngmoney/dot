import datetime

class Due:
    Never = 0xDEADBEAF

    @staticmethod
    def str2due(s):
        s = s.lower()

        human = {"today":0, "tomorrow":1, "soon":3}
        days = None
        if s in human:
            days = human[s]
        elif s in DueWeekly.Days:
            days = DueWeekly.days_until_weekday(DueWeekly.Days.index(s))
        # elif s in DueWeekly.Short:
        #     days = DueWeekly.days_until_weekday(DueWeekly.Short.index(s))
        if not days is None:
            return DueDate.days2due(days)

        # Otherwise Normal
        try:
            return DueWeekly.str2due(s)
        except:
            try:
                return DueDate.str2due(s)
            except:
                return Due()


    def __init__(self):
        pass

    def has_passed(self):
        return False

    def days_until(self):
        return Due.Never

    def __repr__(self):
        return ""

class DueDate(Due):
    @staticmethod
    def str2due(s):
        m, d, y = s.split("/")
        m = int(m)
        d = int(d)
        y = int(y)
        return DueDate(d, m, y)

    @staticmethod
    def days2due(d):
        return DueDate.date2due(datetime.date.today()+datetime.timedelta(d))

    @staticmethod
    def date2due(date):
        return DueDate(date.day, date.month, date.year)

    def __init__(self, day, month, year):
        self.month = month
        self.day = day
        self.year = year

    def date(self):
        return datetime.date(self.year, self.month, self.day)

    def is_late(self):
        return self.days_until() < 0

    def is_today(self):
        return self.days_until() == 0

    def days_until(self, date = None):
        if date is None:
            date = datetime.date.today()
        delta = datetime.date(self.year, self.month, self.day) - date
        return delta.days

    def __repr__(self):
        return str(self.month)+"/"+str(self.day)+"/"+str(self.year)

class DueWeekly(Due):
    Monday = "monday"
    Tuesday = "tuesday"
    Wednesday = "wednesday"
    Thursday = "thursday"
    Friday = "friday"
    Saturday = "saturday"
    Sunday = "sunday"
    Days = [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
    Short = ["m", "t", "w", "r", "f", "s", "d"]


    @staticmethod
    def str2due(s):
        date_string = ""
        day_string = s.lower()
        if "|" in s:
            date_string, day_string = s.lower().split("|")

        days = [False] * 7
        for c in day_string:
            if c in DueWeekly.Short:
                days[DueWeekly.Short.index(c)] = True
            else:
                raise ValueError

        due = DueDate.str2due(date_string) if date_string != "" else None
        return DueWeekly(days, due)

    def __init__(self, days, due=None):
        self.days = days
        self.due = due
        if due is None: self.reset_due()

    def __repr__(self):
        s = ""
        i = 0
        for day in self.days:
            if day:
                s += DueWeekly.Short[i]
            i += 1

        if len(s) > 0: return str(self.due)+"|"+s.upper()
        return ""

    def getDue(self):
        return self.due

    def get_next(self, date=None):
        if date is None:
            if self.due is None:
                date = datetime.date.today()
            else:
                date = self.due.date() + datetime.timedelta(1)
        if self.days[date.weekday()]:
            return DueDate.date2due(date)
        return self.get_next(date+datetime.timedelta(1))

    @staticmethod
    def days_until_weekday(week, date=None):
        if date is None:
            date = datetime.date.today()
        if date.weekday() == week:
            return 0 #DueDate.date2due(date)
        return DueWeekly.days_until_weekday(week, date+datetime.timedelta(1)) + 1

    def reset_due(self, all=False):
        if all:
            self.due = None
        self.due = self.get_next()

    def next_due(self):
        self.due = self.get_next()

    def is_late(self):
        return self.due.is_late()

    def is_today(self):
        return self.due.is_today()

    def days_until(self):
        return self.due.days_until()

