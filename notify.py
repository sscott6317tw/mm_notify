from asyncio import IncompleteReadError
from asyncio import run as async_run
from time import mktime, strptime, time
import os
from argparse import ArgumentParser
from datetime import datetime, timedelta

from aiohttp import ClientSession, request
from aiowebsocket.converses import AioWebSocket
from orjson import OPT_INDENT_2, dumps, loads
from loguru import logger
from line_bot import send_message_to_channel
from telegram_bot import send_message_to_user
import configparser

class MMBot:

    def __init__(self, team_name, method="function") -> None:
        self.config = configparser.ConfigParser() 
        self.config.read("config\config.ini")
        self.server_url = "pmo-mattermost.qyrc452.com"
        self.eng_name = user
        self.username = self.config['mm_info'][f'{user}_username']
        self.password = self.config['mm_info'][f'{user}_password']
        self.token = None
        self.headers = None
        self.team_name = team_name
        self.channel_announce = "bot_channel"
        self.channel_warning = "bot_warring"
        self.channel_msg_only = "msg_announce"
        if method == "function":
            self.token = async_run(self.login_get_token())
        elif method == "api":
            self.token = None
        self.emoji_list = None

    def get_new_key_user(self):
        self.config = configparser.ConfigParser() 
        self.config.read("config\config.ini")
        key_user = self.config['mm_info'][f'{user}_keypoint_user'].split(",")
        return key_user

    async def login_get_token(self, bot=False):
        if bot:
            data = {"device_id": "", "login_id": self.bot_username, "password": self.bot_password, "token": None}
        else:
            data = {"device_id": "", "login_id": self.username, "password": self.password, "token": None}
        async with request("POST", f"https://{self.server_url}/api/v4/users/login", json=data) as resp:
            response = await resp.text()
        if resp.status == 200:
            token = resp.headers["token"]
        else:
            await self.post_message("Error", None, f"```\n{response}\n```")
        return token

    async def connect_to_mattermost(self):
        wss = "wss://pmo-mattermost.qyrc452.com/api/v4/websocket"
        disable_channel = {"bot_warring"}
        async with AioWebSocket(wss) as aws:
            converse = aws.manipulator
            auth_data = {
                "seq": 1,
                "action": "authentication_challenge",
                "data": {"token": await self.login_get_token()},
            }
            await converse.send(dumps(auth_data))
            type_count = 0
            try:
                while 1:
                    key_user = self.get_new_key_user()
                    if r := await converse.receive():
                        r: dict = loads(r)
                        if r.get("event") == "channel_viewed":
                            continue
                        msg_channel = r.get("channel_name")
                        if msg_channel in disable_channel:
                            continue
                        elif r.get("event") and r.get("event") == 'posted':
                            if r['data']['channel_type'] == 'D':
                                if str(self.eng_name).lower() in str(r['data']['sender_name']).lower():
                                    continue
                                msg = (f"{r['data']['sender_name']}私訊你了!!!\n訊息內容：{loads(r['data']['post'])['message']}")
                                telegram_post_msg(self.eng_name, msg)
                            else:
                                if str(self.eng_name).lower() in str(r['data']['sender_name']).lower() or "qa-pepe" in str(r['data']['sender_name']):
                                    continue
                                elif str(self.eng_name).lower() in str(loads(r['data']['post'])['message']).lower():
                                    msg = (
                                        f"{r['data']['sender_name']}在群組{r['data']['channel_display_name']}密你了!!!\n訊息內容：{loads(r['data']['post'])['message']}"
                                    )
                                    telegram_post_msg(self.eng_name, msg)
                                elif any(str(user).lower() in str(r['data']['sender_name']) for user in key_user):
                                    msg = (
                                        f"{r['data']['sender_name']}在群組{r['data']['channel_display_name']}發話了!!!\n訊息內容：{loads(r['data']['post'])['message']}"
                                    )
                                    telegram_post_msg(self.eng_name, msg)
                                elif "all" in str(loads(r['data']['post'])['message']):
                                    msg = (
                                        f"注意注意!!{r['data']['sender_name']}在群組{r['data']['channel_display_name']}標記全部人\n訊息內容：{loads(r['data']['post'])['message']}"
                                    )
                                    telegram_post_msg(self.eng_name, msg)
                        elif r.get("event") and r.get("event") == 'status_change' : #防止離線方式
                            await self.send_private_message("我離線囉~~~:pedroraccoon: ")
                            msg = (
                                "你離線啦!!!!!!!幫你傳個訊息給別人 Hee Ha~~~~~~~"
                            )
                            telegram_post_msg(self.eng_name, msg)       
                        logger.info(dumps(r, option=OPT_INDENT_2).decode("utf-8-sig"))
                    check_endtime(end_time)                 
            except IncompleteReadError as e:
                print(e, "IncompleteReadError")

    async def send_private_message(self, message):
        mm_bot = MMBot("qa-ornd", "api")
        mm_bot.token = await mm_bot.login_get_token()
        url = f"https://{self.server_url}/api/v4"
        headers = self.headers = {"Authorization": f"Bearer {mm_bot.token}"}
        #Kevin err4uojxsj8mmysd1yt1mjhcpr
        #Joey pzzxp9nni3nctrkdmm131me41h
        #離線群組 1easc8g5sjfoicij81f4kdtw3r
        send_msg = {
            "ralf": "1easc8g5sjfoicij81f4kdtw3r", #後面是要送的人
            "joey": "1easc8g5sjfoicij81f4kdtw3r"
            }
        async with ClientSession(headers=headers) as session:
            content = {"channel_id": "1easc8g5sjfoicij81f4kdtw3r", "message": message}
            async with session.post(f"{url}/posts", json=content) as resp:
                msg_id = await resp.json()
        return message

def check_endtime(time_string):
    if time_string != "0":
        time_stamp = int(mktime(strptime(time_string, "%Y-%m-%d %H:%M")))  # 轉成時間戳
        now = int(time())
        if now >= time_stamp:
            logger.success("預計結束時間到期")
            os._exit(0)

def telegram_post_msg(user_name, msg):
    send_message_to_user(user_name, msg)

def linebot_post_msg(user_name, msg):
    send_message_to_channel(user_name, msg)

def parse_args():
    parser = ArgumentParser(prog="notify.py")
    parser.add_argument("-u", "--user", type=str)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.user:
        user = args.user
    else:
        user = "joey"
    new_time = datetime.now() + timedelta(minutes=5)
    end_time = new_time.strftime("%Y-%m-%d %H:%M")
    method = MMBot("qa-ornd", method="websocket")
    while True:
        async_run(method.connect_to_mattermost())
