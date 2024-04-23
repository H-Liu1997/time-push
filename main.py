import random
from time import time, localtime
import cityinfo
from requests import get, post
from datetime import datetime, date
import sys
import os
import http.client, urllib
import json
from zhdate import ZhDate
import requests
global false, null, true
false = null = true = ''
def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token

def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday

    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_weather(city_id, api_key="ae8ad8e430bc47ca90fa190159454633"):
    url = f'https://devapi.qweather.com/v7/weather/3d?location={city_id}&key={api_key}'
    response = requests.get(url)
    response_json = response.json()

    # 检查API请求是否成功
    if response_json['code'] != "200":
        print("API请求失败，请检查错误码和消息")
        return None

    # 提取需要的天气信息
    # print(response_json)
    weather_info = response_json['daily'][0]  # 仅获取最近一天的数据
    weather = weather_info['textDay']
    temp_max = weather_info['tempMax']
    temp_min = weather_info['tempMin']

    return weather, temp_max, temp_min
        
def lucky_lhy():
    if ( Whether_lucky!=False):
        try:
            url = "https://v2.api-m.com/api/horoscope?type=leo&time=today"
            payload = {}
            headers = {
            'User-Agent': 'xiaoxiaoapi/1.0.0 (https://api-m.com)'
            }
            response = requests.request("GET", url, headers = headers, data = payload)
            # print(response.text)
            response = response.json()
    # print(response)
    # print(response["data"]["index"]["all"], response["data"]["index"]["all"])
            data1 = "幸运指数："+str(response["data"]["index"]["all"]) 
            data2 =  str(response["data"]["shortcomment"])
            # +  "\n今日概述："+str(response["data"]["fortunetext"]["all"])
            return data1, data2
        except:
            return ("星座运势API调取错误，请检查API是否正确申请或是否填写正确")
        
def lucky_hzy():
    if ( Whether_lucky!=False):
        try:
            url = "https://v2.api-m.com/api/horoscope?type=scorpio&time=today"
            payload = {}
            headers = {
            'User-Agent': 'xiaoxiaoapi/1.0.0 (https://api-m.com)'
            }
            response = requests.request("GET", url, headers = headers, data = payload)
            # print(response.text)
            response = response.json()
            data1 = "幸运指数："+str(response["data"]["index"]["all"]) 
            data2 =  str(response["data"]["shortcomment"])
            # +  "\n今日概述："+str(response["data"]["fortunetext"]["all"])
            return data1, data2
        except:
            return ("星座运势API调取错误，请检查API是否正确申请或是否填写正确")

#推送信息
def send_message(
        to_user, access_token, city_name_hzy, weather_hzy, max_temperature_hzy, min_temperature_hzy, 
        city_name_lhy, weather_lhy, max_temperature_lhy, min_temperature_lhy,
        lucky_hzy, lucky_lhy, lucky_hzy2, lucky_lhy2,
        ):
    '''
    {{date.DATA}} 
    o(*////▽////*)q  鱼羊恋爱的第{{love_day.DATA}}天！ 
    予予羊羊：{{city_hzy.DATA}} / {{city_lhy.DATA}} 
    本日天气：{{weather_hzy.DATA}} / {{weather_lhy.DATA}}
    最高气温: {{max_temperature_hzy.DATA}}°C / {{max_temperature_lhy.DATA}}°C
    最低气温: {{min_temperature_hzy.DATA}}°C / {{min_temperature_lhy.DATA}}°C 
    <天蝎座>： {{lucky_hzy.DATA}}
    <天蝎座>： {{lucky_hzy2.DATA}}
    <狮子座>： {{lucky_lhy.DATA}}
    <狮子座>： {{lucky_lhy2.DATA}}
    '''
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "city_hzy": {
                "value": city_name_hzy,
                "color": get_color()
            },
            "weather_hzy": {
                "value": weather_hzy,
                "color": get_color()
            },
            "min_temperature_hzy": {
                "value": min_temperature_hzy,
                "color": get_color()
            },
            "max_temperature_hzy": {
                "value": max_temperature_hzy,
                "color": get_color()
            },
            "city_lhy": {
                "value": city_name_lhy,
                "color": get_color()
            },
            "weather_lhy": {
                "value": weather_lhy,
                "color": get_color()
            },
            "min_temperature_lhy": {
                "value": min_temperature_lhy,
                "color": get_color()
            },
            "max_temperature_lhy": {
                "value": max_temperature_lhy,
                "color": get_color()
            },
            "love_day": {
                "value": love_days,
                "color": get_color()
            },

            "lucky_hzy": {
                "value": lucky_hzy,
                "color": get_color()
            },
            "lucky_lhy": {
                "value": lucky_lhy,
                "color": get_color()
            },
            "lucky_hzy2": {
                "value": lucky_hzy2,
                "color": get_color()
            },
            "lucky_lhy2": {
                "value": lucky_lhy2,
                "color": get_color()
            },
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value, year, today)
        # 将生日数据插入data
        data["data"][key] = {"value": birth_day, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("./config.json", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    tokyo = '139.42,35.41'
    taibei = '121.55,25.09'

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入省份和市获取天气信息
    # province, city = config["province"], config["city"]
    weather_lhy, max_temperature_lhy, min_temperature_lhy = get_weather(tokyo)
    weather_hzy, max_temperature_hzy, min_temperature_hzy = get_weather(taibei)

    # #获取天行API
    # tianxing_API=config["tianxing_API"]
    # #是否开启天气预报API
    # Whether_tip=config["Whether_tip"]
    # #是否启用词霸每日一句
    # Whether_Eng=config["Whether_Eng"]
    #是否启用星座API
    Whether_lucky=config["Whether_lucky"]
    # #是否启用励志古言API
    # Whether_lizhi=config["Whether_lizhi"]
    # #是否启用彩虹屁API
    # Whether_caihongpi=config["Whether_caihongpi"]
    # #是否启用健康小提示API
    # Whether_health=config["Whether_health"]
    # #获取星座
    # astro = config["astro"]
    # # 获取词霸每日金句
    # note_ch, note_en = get_ciba()
    # #彩虹屁
    # pipi = caihongpi()
    # #健康小提示
    # health_tip = health()
    # #下雨概率和建议
    # pop,tips = tip()
    # #励志名言
    # lizhi = lizhi()
    # #星座运势
    lucky_hzy_res, lucky_hzy_res2 = lucky_hzy() 
    lucky_lhy_res, lucky_lhy_res2 = lucky_lhy() 
    
    # 公众号推送消息
    for i, user in enumerate(users):
        send_message(
            user, accessToken, config["city_hzy"], weather_hzy, max_temperature_hzy, min_temperature_hzy, 
            config["city_lhy"], weather_lhy, max_temperature_lhy, min_temperature_lhy, lucky_hzy_res, lucky_lhy_res, lucky_hzy_res2, lucky_lhy_res2,
            )
    import time
    time_duration = 3.5
    time.sleep(time_duration)
