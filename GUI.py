from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTextBrowser,
    QLabel,
    QFileDialog,
    QErrorMessage,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap
import sys
from app import get_citizen
import matplotlib.pyplot as plt
import cv2
import os
import shutil
import datetime
import time

from deepface import DeepFace
from capture import camera


class Home(QMainWindow):
    def __init__(self) -> None:
        """
        init the main window for the gui

        """
        self.citizen = None
        self.front_path = ""
        self.back_path = ""
        self.image_path = ""
        super(Home, self).__init__()
        uic.loadUi("./GUI.ui", self)

        self.upload_front = self.findChild(QPushButton, "upload_front")

        self.upload_back = self.findChild(QPushButton, "upload_back")
        self.upload_image = self.findChild(QPushButton, "upload_image")
        self.submit_button = self.findChild(QPushButton, "submit_button")
        self.clear_button = self.findChild(QPushButton, "clear_button")
        self.save_button = self.findChild(QPushButton, "save_button")

        self.name_field = self.findChild(QTextBrowser, "name_field")
        self.address_field = self.findChild(QTextBrowser, "address_field")
        self.city_field = self.findChild(QTextBrowser, "city_field")
        self.id_field = self.findChild(QTextBrowser, "id_field")
        self.status_field = self.findChild(QTextBrowser, "status_field")
        self.religion_field = self.findChild(QTextBrowser, "religion_field")
        self.gender_field = self.findChild(QTextBrowser, "gender_field")
        self.job_field = self.findChild(QTextBrowser, "job_field")

        self.upload_front.clicked.connect(self.upload)
        self.upload_back.clicked.connect(self.upload)
        self.upload_image.clicked.connect(self.capture)

        self.submit_button.clicked.connect(self.submit)
        self.clear_button.clicked.connect(self.clear)
        self.save_button.clicked.connect(self.save)

        self.front_label = self.findChild(QLabel, "front_label")
        self.back_label = self.findChild(QLabel, "back_label")

        self.result_label = self.findChild(QLabel, "result_label")
        self.result_image = self.findChild(QLabel, "result_image")

        self.show()

    def upload(self):
        button = self.sender()
        button_name = button.text()
        path = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "C:\\Users\PC\Desktop\Dataset",
            "Image files (*.jpg *.gif *.png *.jpeg)",
        )
        if button_name == "صورة البطاقة الامامية":
            self.front_path = path
            self.front_label.setText(os.path.basename(self.front_path[0]))
        elif button_name == "صورة البطاقة الخلفية":
            self.back_path = path
            self.back_label.setText(os.path.basename(self.back_path[0]))

    def submit(self):
        if self.front_path == "" or self.front_path[0] == "":
            self.errorMessage("Error", "Please enter the front image")
            return
        if self.back_path == "" or self.back_path[0] == "":
            self.errorMessage("Error", "Please enter the back image")
            return

        if self.image_path == "":
            self.errorMessage("Error", "Please enter the image")
            return

        paths = [self.front_path, self.back_path]
        self.citizen = get_citizen(paths)

        self.name_field.clear()
        self.name_field.append(self.citizen.full_name)

        self.address_field.clear()
        self.address_field.append(self.citizen.address)

        self.city_field.clear()
        self.city_field.append(self.citizen.city)

        self.id_field.clear()
        self.id_field.append(
            "  \t\t                     " + str(self.citizen.id)
        )

        self.status_field.clear()
        self.status_field.append(self.citizen.marital_state)

        self.religion_field.clear()
        self.religion_field.append(self.citizen.relegion)

        self.gender_field.clear()
        self.gender_field.append(self.citizen.gender)

        self.job_field.clear()
        self.job_field.append(self.citizen.job_title + " " + self.citizen.job)

        fig = plt.figure(figsize=(10, 7))

        rows = 1
        columns = 2

        Image1 = self.citizen.img

        Image2 = cv2.cvtColor(
            cv2.imread(str(self.image_path)), cv2.COLOR_BGR2RGB
        )

        fig.add_subplot(rows, columns, 1)

        plt.imshow(Image1, cmap="gray")
        plt.axis("off")
        id_path = f"citizens\{self.citizen.id}\{self.citizen.id}.jpg"

        fig.add_subplot(rows, columns, 2)

        plt.imshow(Image2)
        plt.axis("off")
        matched = False
        try:
            dist = DeepFace.verify(id_path, self.image_path)["distance"]

            if dist <= 0.3:
                matched = True
            else:
                matched = False
        except:
            pass
        if matched:
            matched = "Matched"
            self.result_label.setText("")
            self.result_label.setText("متطابق")
            self.result_label.setStyleSheet(
                "background-color: lightgreen;text-align:center"
            )

        elif not (matched):
            matched = "Not matched"
            self.result_label.setText("")
            self.result_label.setText("غير متطابق")
            self.result_label.setStyleSheet(
                "background-color: red;text-align:center"
            )

        plt.savefig("result.jpg")

        img_path = "result.jpg"
        pmap = QPixmap(img_path)

        self.result_image.setPixmap(pmap)

        self.image_path = ""

        original_path = r"C:\Users\PC\Desktop\id-reader\capture.png"

        timestamp = int(time.time())

        dt_object = datetime.datetime.fromtimestamp(timestamp)

        filename = dt_object.strftime("%Y-%m-%d_%H-%M-%S")

        if not os.path.exists(
            f"C:\\Users\PC\Desktop\id-reader\citizens\{self.citizen.id}\Logs"
        ):
            os.mkdir(
                f"C:\\Users\PC\Desktop\id-reader\citizens\{self.citizen.id}\Logs"
            )
        new_path = f"C:\\Users\PC\Desktop\id-reader\citizens\{self.citizen.id}\Logs\{filename}.png"
        shutil.copy2(original_path, new_path)

    def errorMessage(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def infoMessage(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def clear(self):
        self.name_field.clear()
        self.address_field.clear()
        self.city_field.clear()
        self.id_field.clear()
        self.status_field.clear()
        self.religion_field.clear()
        self.gender_field.clear()
        self.job_field.clear()
        self.front_label.setText("")
        self.back_label.setText("")
        self.back_path = ""
        self.front_path = ""
        self.image_path = ""
        self.result_label.setText("")
        self.result_label.setStyleSheet("background-color: transparent")
        self.result_image.setPixmap(QPixmap())
        self.citizen = None

    def save(self):
        if self.citizen == None:
            self.errorMessage("Error", "Please submit first")
            return
        self.citizen.full_name = str(self.name_field.toPlainText())
        self.citizen.address = str(self.address_field.toPlainText())
        self.citizen.city = str(self.city_field.toPlainText())
        self.citizen.full_job = str(self.job_field.toPlainText())
        self.citizen.gender = str(self.gender_field.toPlainText())
        self.citizen.marital_state = str(self.status_field.toPlainText())
        self.citizen.relegion = str(self.religion_field.toPlainText())
        self.citizen.file_output()

        self.infoMessage("Done", "Saved successfuly")

    def capture(self):
        captured = camera()
        if captured:
            self.image_path = "capture.png"


def main():
    app = QApplication(sys.argv)
    window = Home()
    app.exec_()


if __name__ == "__main__":
    main()
