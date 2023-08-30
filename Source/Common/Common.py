import urllib.request

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


def set_pixmap_from_url(t_label: QLabel, t_url: str):
    """QLabel에 Image Url을 setPixmap"""
    # 예시 : urlstring = "https://img.freepik.com/premium-vector/korea-food-menu-set_144089-92.jpg"
    urlstring = t_url
    imgfromurl = urllib.request.urlopen(urlstring).read()
    pixmap = QPixmap()
    pixmap.loadFromData(imgfromurl)
    t_label.setPixmap(pixmap.scaledToWidth(t_label.width()))
