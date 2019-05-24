def compare_time(day1, day2):
    '''Comparing 2 days. If day1 is later than day2 then return True else False'''
    day1, day2 = standard(day1), standard(day2)

    day1 = day1.split('/')
    day1.reverse()
    day1 = int(''.join(day1))

    day2 = day2.split('/')
    day2.reverse()
    day2 = int(''.join(day2))

    if day1 > day2:
        return True
    
    else:
        return False

def standard(day):
    day = day.split('/')
    if int(day[1]) < 10 and len(day[1]) == 1:
        day[1] = '0' + day[1]
    
    if int(day[0]) < 10 and len(day[0]) == 1:
        day[0] = '0' + day[0]
    day = '/'.join(day)

    return day

if __name__ == "__main__":
    print(compare_time("25/4/2019", "20/5/2019"))
    day = standard("1/03/2019")
    print(day)
    # day = standard("24/10/2019")
    # print(day)
