import easyocr
import cv2
import os
from fuzzywuzzy import fuzz
import pytesseract
from citizen import Citizen
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
reader = easyocr.Reader(["ar"])


def ocr(path):
    result = reader.readtext(path)

    final = []

    sorted_result = sorted(result, key=lambda x: x[0][1][0], reverse=True)

    for x in sorted_result:
        final.append(x[1])
    str = ""
    for x in final:
        str += x + " "
    return str


def recognize(front, front_template, back, back_template):
    params = []
    flag = False
    for coordinate in front[:-2]:
        roi_x = coordinate["roi_x"]
        roi_y = coordinate["roi_y"]
        roi_width = coordinate["roi_width"]
        roi_height = coordinate["roi_height"]
        roi = front_template[
            roi_y : roi_y + roi_height, roi_x : roi_x + roi_width
        ]
        output_path = "out1.png"
        cv2.imwrite(output_path, roi)
        params.append(ocr(output_path))

    id_x = front[-2]["roi_x"]
    id_y = front[-2]["roi_y"]
    id_width = front[-2]["roi_width"]
    id_height = front[-2]["roi_height"]
    id = front_template[id_y : id_y + id_height, id_x : id_x + id_width]
    text_id = pytesseract.image_to_string(id, lang="ara", config=".")
    text_id = text_id.replace(" ", "")
    text_id = text_id.replace("\n", "")

    img_x = front[-1]["roi_x"]
    img_y = front[-1]["roi_y"]
    img_width = front[-1]["roi_width"]
    img_height = front[-1]["roi_height"]
    img = front_template[img_y : img_y + img_height, img_x : img_x + img_width]

    counter = 0
    for coordinate in back:
        roi_x = coordinate["roi_x"]
        roi_y = coordinate["roi_y"]
        roi_width = coordinate["roi_width"]
        roi_height = coordinate["roi_height"]

        if len(params) == 6:
            if len(params[5]) == 0:
                flag = True
        if len(params) == 7 and flag:
            roi_x = 480
            roi_y = 150
            roi_width = 200
            roi_height = 90

        roi = back_template[
            roi_y : roi_y + roi_height, roi_x : roi_x + roi_width
        ]
        output_path = "out1.png"
        cv2.imwrite(output_path, roi)

        text = ocr(output_path)

        if counter == 2:
            ratio = fuzz.ratio(str(text), "ذكر")
            if ratio >= 75:
                text = "ذكر"
            else:
                text = "انثى"

        elif counter == 3:
            gender = params[6]
            if gender == "ذكر":
                text = text.lstrip()
                ratio = fuzz.ratio(str(text), "مسلم")

                if ratio >= 50:
                    text = "مسلم"
                else:
                    text = "مسيحي"
            else:
                ratio = fuzz.ratio(str(text), "مسلمة")
                if ratio >= 75:
                    text = "مسلمة"
                else:
                    text = "مسيحية"
        elif counter == 4:
            gender = params[6]

            if gender == "ذكر":
                ratio = fuzz.ratio(str(text), "اعزب")
                if ratio >= 75:
                    text = "اعزب"
                elif fuzz.ratio(str(text), "متزوج") >= 75:
                    text = "متزوج"
                elif fuzz.ratio(str(text), "مطلق") >= 75:
                    text = "مطلق"
                elif fuzz.ratio(str(text), "ارمل") >= 75:
                    text = "ارمل"
            else:
                ratio = fuzz.ratio(str(text), "انسة")
                if ratio >= 75:
                    text = "انسة"
                elif fuzz.ratio(str(text), "متزوجة") >= 75:
                    text = "متزوجة"
                elif fuzz.ratio(str(text), "مطلقة") >= 75:
                    text = "مطلقة"
                elif fuzz.ratio(str(text), "ارملة") >= 75:
                    text = "ارملة"

        params.append(text)
        counter += 1

    citizen = Citizen(
        params[0],
        params[1],
        params[2],
        params[3],
        img,
        text_id,
        params[4],
        params[5],
        params[6],
        params[7],
        params[8],
    )
    return citizen


def test(coordinate, template):
    roi_x = coordinate["roi_x"]
    roi_y = coordinate["roi_y"]
    roi_width = coordinate["roi_width"]
    roi_height = coordinate["roi_height"]
    roi = template[roi_y : roi_y + roi_height, roi_x : roi_x + roi_width]
    output_path = "out1.png"
    cv2.imwrite(output_path, roi)

    answer = ocr(output_path)

    if os.path.exists(output_path):
        os.remove(output_path)
