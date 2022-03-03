from datetime import date


_format = {
    "ymd": "{d.year}-{d.month}-{d.day}",
    "mdy":"{d.month}/{d.day}/{d.year}",
    "dmy":"{d.day}/{d.month}/{d.year}"
}

class DateNew:
    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, format_spec):

        if format_spec == "":
            format_spec = "ymd"
        fmt = _format[format_spec]
        return fmt.format(d=self)



if __name__ == '__main__':
    # date = DateNew(2021,8,13)
    # print(format(date,"mdy"))

    d = date(2012,12,21)
    print(d)
    print(format(d,"%A,%B %d,%Y"))#格式化代码的解析工作完全由类自己决定
