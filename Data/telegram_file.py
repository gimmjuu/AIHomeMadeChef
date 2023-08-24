import os

import telebot
import uuid

# 텔레그램 봇 토큰
bot_token = "6563537418:AAF6LaEx7-VxN8GVWMIMKTC4wIg4nFPv6DQ"
bot = telebot.TeleBot(bot_token)
custom_folder_path = "./img_file"

def generate_unique_filename():
    # 랜덤 문자열 생성
    unique_string = str(uuid.uuid4().hex)
    image_filename = os.path.join(custom_folder_path,f"image_{unique_string}.jpg")
    return image_filename

def handle_image(message):
    # 유니크한 이미지 파일 이름 생성
    image_filename = generate_unique_filename()

    # 이미지 저장
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(image_filename, "wb") as new_file:
        new_file.write(downloaded_file)

    # 이미지 저장 후 메시지 전송
    bot.send_message(message.chat.id, "이미지 저장이 완료되었습니다.")

@bot.message_handler(content_types=["photo"])
def on_image(message):
    handle_image(message)

bot.polling()