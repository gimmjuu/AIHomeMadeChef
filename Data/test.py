import json
import os


def main():
    front_path, file_list = get_file_path()
    for file in file_list:
        convert_to_coco(file, front_path[:-1])


def get_file_path():
    file_list = os.listdir(r"data/orgin")
    return r"C:\Users\kdt111\Desktop\project_YOLOv8\data\orgin\\", file_list


def convert_to_coco(file_name, origin_path):
    bbox = None
    file_path = origin_path + file_name
    new_folder_path = r"C:\Users\kdt111\Desktop\project_YOLOv8\data\labels\train\\"
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        bbox = data['annotations'][0]['bbox']
        img_width = data['images'][0]['width']
        img_height = data['images'][0]['height']
    try:

        x_center = bbox[0] + (bbox[2] / 2)
        y_center = bbox[1] + (bbox[3] / 2)
    except:
        return

    x_center_normalized = f"{(x_center / img_width):.6f}"
    y_center_normalized = f"{(y_center / img_height):.6f}"
    width_normalized = f"{(bbox[2] / img_width):.6f}"
    height_normalized = f"{(bbox[3] / img_height):.6f}"

    normalized_bbox = [x_center_normalized, y_center_normalized, width_normalized, height_normalized]

    new_file_path = new_folder_path[:-1] + file_name[:-4] + "txt"
    result = f"0 {' '.join(normalized_bbox)}"
    with open(new_file_path, "w", encoding="utf-8") as file_:
        file_.write(f"{result}")

    # print(0, end=" ")
    # print(*normalized_bbox)
def convert_to_coco_v2(file_name, origin_path):
    bbox = None
    file_path = origin_path + file_name
    new_folder_path = r"C:\Users\kdt111\Desktop\project_YOLOv8\data\labels\train\\"
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        drug_num = data['images'][0]['drug_N'][3:]
        print(f"{drug_num} | {file_path}")

        bbox = data['annotations'][0]['bbox']
        img_width = data['images'][0]['width']
        img_height = data['images'][0]['height']
    try:

        x_center = bbox[0] + (bbox[2] / 2)
        y_center = bbox[1] + (bbox[3] / 2)
    except:
        return

    x_center_normalized = f"{(x_center / img_width):.6f}"
    y_center_normalized = f"{(y_center / img_height):.6f}"
    width_normalized = f"{(bbox[2] / img_width):.6f}"
    height_normalized = f"{(bbox[3] / img_height):.6f}"

    normalized_bbox = [x_center_normalized, y_center_normalized, width_normalized, height_normalized]

    new_file_path = new_folder_path[:-1] + file_name[:-4] + "txt"
    result = f"{drug_num} {' '.join(normalized_bbox)}"
    with open(new_file_path, "w", encoding="utf-8") as file_:
        file_.write(f"{result}")
    return drug_num

if __name__ == '__main__':
    main()