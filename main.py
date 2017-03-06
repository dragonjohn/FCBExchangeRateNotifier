import ConfigParser
import requests
import re

# FCB exchange rate page
res = requests.get("https://ibank.firstbank.com.tw/NetBank/7/0201.html?sh=none");

#print(res.text)


#find spot and cash rate
target_flag = False
exchange_rate_set = []
for row in res.iter_lines():
    if "U.S. Dollar(USD)" in row:
        target_flag = True
    if "Japanese Yen (JPY)" in row:
        target_flag = True
    if target_flag:
        row = row.strip()
        if re.findall(r"\d+\.\d+",row):
            #print row
            exchange_rate_set.append(float(row))
            target_flag = False
#print(exchange_rate_set)

for idx, rate in enumerate(exchange_rate_set):
    if idx%2 == 0:
        print rate
        # if rate < USD_target, send email notification

Config = ConfigParser.ConfigParser()
Config.read("fcber.ini")
print (Config.sections())

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("Skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = none
    return dict1