import cv2

name = input(" Enter your name: ").strip().lower()
filename = f"photoss/{name}.jpg"

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    cv2.imshow("Captured Image", frame)
    cv2.imwrite(filename, frame)
    print(f" Saved as {filename}")
else:
    print(" Failed to capture image")

cv2.waitKey(2000)
cap.release()
cv2.destroyAllWindows()
