import json

from apscheduler.schedulers.blocking import BlockingScheduler
from pip._vendor import requests


class Bean:
    hour = 0
    minute = 0
    content = ""

    def __init__(self, hour, minute, content):
        self.hour = hour
        self.minute = minute
        self.content = content


class Clock:
    def remind(content):
        url = "https://oapi.dingtalk.com/robot/send?access_token=69d725b52e355ad81d221aebb0a39fc5290bf4c0b52362b8e08271b87656d436"
        headers = {'Content-Type': 'application/json'}
        data = {'msgtype': 'text',
                'text': {
                    'content': content
                },
                "at": {
                    "atMobiles": [18744022755],
                    "isAtAll": False
                }
                }
        print(data)
        res = requests.post(url=url, headers=headers, data=json.dumps(data))
        return res

    scheduler = BlockingScheduler()
    data_list = [Bean(hour=12, minute=0, content="鹤仔仔该吃饭了"),
                 Bean(hour=14, minute=0, content='懒熊熊想兔蛮蛮了'),
                 Bean(hour=15, minute=0, content='小鹤仔该喝水了'),
                 Bean(hour=16, minute=0, content='小鹤仔该活动活动了'),
                 Bean(hour=17, minute=0, content='小鹤仔该上厕所了'),
                 Bean(hour=18, minute=0, content='鹤仔仔该休息休息了'),
                 Bean(hour=19, minute=20, content='鹤仔仔该吃晚饭了'),
                 Bean(hour=20, minute=30, content='鹤仔仔该下班了'),
                 ]
    for bean in data_list:
        scheduler.add_job(remind, "cron", day_of_week="1-5", hour=bean.hour, minute=bean.minute,
                          args=[bean.content])
    print("start clock")
    scheduler.start()


if __name__ == '__main__':
    Clock = Clock()
