import os
import telebot
import uuid

from PyQt5.QtGui import QPixmap


class TelegramBot:
    def __init__(self, lbl_imgview):
        self.bot_token = "6563537418:AAF6LaEx7-VxN8GVWMIMKTC4wIg4nFPv6DQ"
        self.bot = telebot.TeleBot(self.bot_token)
        self.custom_folder_path = r"C:\Users\KDT113\Desktop\AIHomeMadeChef\Font"
        self.bot.message_handler(content_types=["photo"])(self.handle_image)
        self.file_name = ''
        self.lbl_img = lbl_imgview

    def generate_unique_filename(self):
        unique_string = str(uuid.uuid4().hex)
        return os.path.join(self.custom_folder_path, f"image_{unique_string}.jpg")

    def handle_image(self, message):
        image_filename = self.generate_unique_filename()
        file_info = self.bot.get_file(message.photo[-1].file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)
        with open(image_filename, "wb") as new_file:
            new_file.write(downloaded_file)
        self.bot.send_message(message.chat.id, "이미지 저장이 완료되었습니다.")
        self.file_name = image_filename
        self.lbl_img.setPixmap(QPixmap(self.file_name))

    def start_polling(self):
        while True:
            try:
                self.bot.polling()
            except Exception as e:
                print("Polling Error:", e)
