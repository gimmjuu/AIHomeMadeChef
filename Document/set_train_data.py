"""
Date : 23/08/25
Author : JooHyein
Details : 라벨링 파일 변환 및 파일 경로 변경
"""
import os
import shutil
from pathlib import Path


def copy_to_images():
    for (root_, directories_, files_) in os.walk(r'D:\음식 이미지 및 영양정보 텍스트\Validation'):
        for dir_ in directories_:
            if "[원천]" in dir_:
                base_path = Path(fr'D:\음식 이미지 및 영양정보 텍스트\Validation\{dir_}')
                for entry in base_path.iterdir():
                    if entry.is_dir():
                        # print(entry.name)
                        files_ = os.listdir(entry)
                        for file in files_:
                            print(fr'{entry}\{file}')
                            shutil.copy(fr'{entry}\{file}',
                                        fr'D:\yolov8_train\images\{file}')


def move_to_labels():
    for (root_, directories_, files_) in os.walk(r'D:\yolov8_train\source\txt'):
        for dir_ in directories_:
            files_ = os.listdir(fr'D:\yolov8_train\source\txt\{dir_}')
            for file in files_:
                shutil.move(fr'D:\yolov8_train\source\txt\{dir_}\{file}', fr'D:\yolov8_train\labels\{file}')


def get_pascal_class():
    class_key = os.listdir(r'D:\yolov8_train\labels')
    # class_value = [x for x in range(1, len(class_key) + 1)]
    class_value = [x + 237 for x in range(1, len(class_key) + 1)]
    print(class_value)
    for i, nm in zip(class_value, class_key):
        print(f"{i}: {nm}")


class ConvertTxtValue:
    def __init__(self):
        self.PASCAL_CLASS = dict()

    def set_pascal_class(self):
        class_key = os.listdir(r'D:\yolov8_train\labels')
        # class_value = [x for x in range(1, len(class_key) + 1)]
        class_value = [x+237 for x in range(1, len(class_key) + 1)]
        self.PASCAL_CLASS = dict(zip(class_key, class_value))

    def convert_txt(self):
        for (root_, directories_, files_) in os.walk(r'D:\yolov8_train\labels'):
            for dir_ in directories_:
                class_value = self.PASCAL_CLASS[dir_]
                print(dir_, class_value)

                if class_value < 2:
                    continue

                files_ = os.listdir(fr'D:\yolov8_train\labels\{dir_}')

                for file_name in files_:
                    if '.txt' in file_name:
                        new_contents = ''

                        with open(fr'D:\yolov8_train\labels\{dir_}\{file_name}', 'r') as f:
                            lines = f.readlines()

                            for i, l in enumerate(lines):
                                if l[:4] == "1 0.":
                                    l = f"{class_value}{l[1:]}"

                                new_contents += l

                        with open(fr'D:\yolov8_train\labels\{file_name}', 'w') as f:
                            f.write(new_contents)


if __name__ == '__main__':
    # --- class list 만들기
    # get_pascal_class()
    # --- .txt 파일 800000개에 대한 class 수정
    test = ConvertTxtValue()
    # test.set_pascal_class()
    # test.convert_txt()
    # --- 라벨링 파일 위치 이동
    # move_to_labels()
    # --- 이미지 파일 복사
    # copy_to_images()
