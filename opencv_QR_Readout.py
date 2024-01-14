import cv2
import numpy as np
import time

# Function to decode QR codes using OpenCV
def decode_qr_codes(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialize QRCodeDetector
    qr_decoder = cv2.QRCodeDetector()

    # Detect and decode QR codes
    retval, decoded_info, points, straight_qrcode = qr_decoder.detectAndDecodeMulti(gray)

    # List to store the QR code data
    qr_data_list = []

    # Draw rectangles around detected QR codes
    if points is not None and len(points) > 0:
        for i in range(len(points)):
            hull = cv2.convexHull(points[i].astype(np.int32))
            cv2.polylines(image, [hull], True, (0, 255, 0), 2)
            qr_data_list.append(decoded_info[i])

    # Print the array of QR code data after a certain interval (e.g., 1 second)
    if qr_data_list and time.time() % 1 < 0.1:
        print("QR Code Data:", qr_data_list)

    return image

# Main function
def main():
    # Open the video capture device (you can replace 0 with the camera index or video file)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Break the loop if there's an issue reading the frame
        if not ret:
            break

        # Call the decode_qr_codes function to find and draw QR codes
        result_frame = decode_qr_codes(frame)

        # Display the result frame
        cv2.imshow('QR Code Tracking', result_frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Run the main function
if __name__ == "__main__":
    main()
