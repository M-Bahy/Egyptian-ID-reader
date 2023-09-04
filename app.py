import cv2
from model import recognize, test
import matplotlib.pyplot as plt
import time


def get_citizen(paths):
    front_template = cv2.imread(paths[0][0], cv2.IMREAD_GRAYSCALE)

    front_template = cv2.bilateralFilter(front_template, 11, 17, 17)

    back_template = cv2.imread(paths[1][0], cv2.IMREAD_GRAYSCALE)
    roi_x = 0
    roi_y = 0
    roi_width = 1000
    roi_height = 630
    front_template = front_template[
        roi_y : roi_y + roi_height, roi_x : roi_x + roi_width
    ]
    back_template = back_template[
        roi_y : roi_y + roi_height, roi_x : roi_x + roi_width
    ]

    back_template = cv2.bilateralFilter(back_template, 11, 17, 17)

    new_front = [
        {"roi_x": 650, "roi_y": 135, "roi_width": 300, "roi_height": 90},
        {"roi_x": 400, "roi_y": 216, "roi_width": 600, "roi_height": 65},
        {"roi_x": 400, "roi_y": 270, "roi_width": 600, "roi_height": 90},
        {"roi_x": 400, "roi_y": 340, "roi_width": 600, "roi_height": 90},
        {"roi_x": 400, "roi_y": 460, "roi_width": 600, "roi_height": 90},
        {"roi_x": 0, "roi_y": 0, "roi_width": 300, "roi_height": 380},
    ]

    new_back = [
        {"roi_x": 400, "roi_y": 65, "roi_width": 400, "roi_height": 90},
        {"roi_x": 250, "roi_y": 115, "roi_width": 550, "roi_height": 70},
        {"roi_x": 625, "roi_y": 180, "roi_width": 200, "roi_height": 50},
        {"roi_x": 480, "roi_y": 180, "roi_width": 200, "roi_height": 60},
        {"roi_x": 280, "roi_y": 150, "roi_width": 200, "roi_height": 90},
    ]

    citizen = recognize(new_front, front_template, new_back, back_template)

    citizen.full_name = citizen.first_name + " " + citizen.last_name

    citizen.file_output()
    citizen.save_image()
    return citizen
