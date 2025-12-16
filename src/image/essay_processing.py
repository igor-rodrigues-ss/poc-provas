import cv2
import numpy as np

from pdf2image import convert_from_path


def to_png(path: str, output_path: str):
    pages = convert_from_path(path, dpi=300)
    page = pages[0]

    page.save(output_path, "PNG")


def pre_processing(path: str, output_path: str):
    pages = convert_from_path(path, dpi=300)
    page = pages[0]

    img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

    h, w = img.shape[:2]

    top = 130
    bottom = 50
    left = 210
    right = 90

    img = img[top : h - bottom, left : w - right]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))

    detected_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    mask = detected_lines

    clean = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    gray_clean = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY)
    final = cv2.threshold(gray_clean, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.imwrite(output_path, final)