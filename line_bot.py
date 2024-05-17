import aiohttp
import asyncio
import requests

def send_message_to_channel(user_name, msg):
    user_id_dict = {
        "ralf" : "U28e3c407e9681001f0ef8ce0774b44b1",
        "joey" : ""
    }
    headers = {
        "Authorization": "Bearer hiTkVFocsLiKYcWxs27wgYtLWuJe4/MLvWXkIeRen9V5l/gZnt2QPt1AQX0U+nlcIZHvTMC6w8IkrtWRreounwPlhCHB2EOPPKuTuyzcYmfgS3hcu2pFqZtGuP1Q9/M6m/cAsML8lcH6VbHeVrso9AdB04t89/1O/w1cDnyilFU="
    }
    # url = "https://api.line.me/v2/bot/group/Cd8acd7e3027d7888bc6750248047d8a2/members/ids"
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, headers=headers) as response:
    #         if response.status == 200:
    #             print("Message sent successfully.")
    # user_id = "Uf34024d50c8a0bd1683bc5b6894a7abd"
    # channel_id = "Cd8acd7e3027d7888bc6750248047d8a2"
    # msg = f"<@{user_id}> {msg}"
    url = "https://api.line.me/v2/bot/message/push"
    payload = {
        "to": user_id_dict[user_name],
        "messages": [{"type": "text", "text": msg}],
    }

    response = requests.post(url, headers=headers, json=payload)



# if __name__ == "__main__":
#     asyncio.run(send_message_to_channel("ralf","Hello, world!"))