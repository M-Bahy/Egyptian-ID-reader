import matplotlib.pyplot as plt
import cv2
import os


class Citizen:
    def __init__(
        self,
        fname,
        lname,
        add,
        city,
        img,
        id,
        job_title,
        job,
        gender,
        relegion,
        marital_state,
    ) -> None:
        self.first_name = fname
        self.last_name = lname
        self.address = add
        self.city = city
        self.img = img
        self.id = id
        self.job_title = job_title
        self.job = job
        self.gender = gender
        self.relegion = relegion
        self.marital_state = marital_state
        self.full_name = self.first_name + " " + self.last_name
        self.full_job = self.job_title + " " + self.job

    def __str__(self):
        data = ""
        data += f"ألاسم : {self.full_name}\nالعنوان : {self.address}\nالمدينة : {self.city}"
        data += f"\nالرقم القومي : {self.id}"
        data += f"\nالوظيفة : {self.full_job}"
        data += f"\nالنوع : {self.gender}"
        data += f"\nالديانة : {self.relegion}"
        data += f"\nالحالة الاجتماعية : {self.marital_state}"
        return data

    def file_output(self):
        name = self.first_name + " " + self.last_name
        if not os.path.exists("citizens"):
            os.mkdir("citizens")
        if not os.path.exists(f"citizens/{self.id}"):
            os.mkdir(f"citizens/{self.id}")
        with open(f"citizens/{self.id}/info.txt", "w", encoding="utf-8") as f:
            f.write(self.__str__())
            f.close()

    def show_image(self):
        plt.imshow(self.img, cmap="gray")
        plt.show()

    def save_image(self):
        name = self.first_name + " " + self.last_name
        if not os.path.exists("citizens"):
            os.mkdir("citizens")
        if not os.path.exists(f"citizens/{self.id}"):
            os.mkdir(f"citizens/{self.id}")
        name_utf8 = name.encode("utf-8")
        cv2.imwrite(f"citizens/{self.id}/{self.id}.jpg", self.img)
