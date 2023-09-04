import cv2


def camera():
    captured = False
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.namedWindow("capture")

    while True:
        ret, frame = cam.read()

        if not ret:
            break
        cv2.imshow("capture", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            break
        elif k % 256 == 32:
            img_name = "capture.png"
            cv2.imwrite(img_name, frame)

            captured = True
            break

    cam.release()
    cv2.destroyAllWindows()
    return captured
