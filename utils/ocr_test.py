import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def test_ocr(image_path):
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img)
    print("OCR Output:", repr(text))
    cv2.imshow("Test Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

test_ocr(r"C:\Users\hanaa\OneDrive\Desktop\SmartAssistantProject\sample_text_ocr.png")