# function to emulate workdays function in excel
# copied bulk of code from a tutorial, not 100% certain how parts of it work yet, but it currently works

import datetime as dt

def workdays(d, end, excluded=(6, 7)):
    days = []
    while d <= end:
        if d.isoweekday() not in excluded:
            days.append(d)
        d += dt.timedelta(days=1)
    return days