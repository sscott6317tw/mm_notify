from telegram import Bot
import json

def send_message_to_user(user_name, msg):
    bot_token = '6991544735:AAGtzUc-H3MOwfYxc8aPdPMT2b4vbyrMWTY'
    bot = Bot(token=bot_token)
    with open(r'config/user_id.json', 'r') as file:
        json_data = file.read()

    # 将 JSON 数据转换为字典
    user_id_dict = json.loads(json_data)
    bot.send_message(chat_id=user_id_dict[user_name], text=msg)



# if __name__ == "__main__":
#     asyncio.run(send_message_to_channel("ralf","Hello, world!"))