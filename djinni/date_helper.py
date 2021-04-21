import datetime
import calendar


def date_str_2_datetime(date: str):
    today =  datetime.date.today()
    str_to_date = {"сегодня": today, "вчера": today - datetime.timedelta(days=1),
                    "today": today, "yesterday": today - datetime.timedelta(days=1)}
    if (date in str_to_date):
        return str_to_date[date]

    month_num = month_str_2_num(date.split()[1])
    day = int(date.split()[0])
    return datetime.date(today.year, month_num, day)

def month_str_2_num(month: str):
    months_ru = ("","января","февраля","марта","апреля","мая","июня",
                "июля","августа","сентября","октября","ноября","декабря")
    
    if(month in months_ru):
        return months_ru.index(month)
    return list(calendar.month_abbr).index(month[:3].title())
    
def how_many_days_ago(date):
    delta =  datetime.date.today() - date
    return delta.days
