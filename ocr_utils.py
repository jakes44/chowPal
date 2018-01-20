import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'tesseract'

def img2str(img):
    return pytesseract.image_to_string(img)

def img2boxes(img):
    return pytesseract.image_to_boxes(img)

