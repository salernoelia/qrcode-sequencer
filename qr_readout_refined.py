import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time

import warnings

# Suppress ZBar warnings
warnings.filterwarnings("ignore")





# Function to decode barcodes and QR codes
def decode_barcodes(image, qr_data_list):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use pyzbar to decode barcodes and QR codes
    decoded_objects = decode(gray)

    # Loop over the decoded objects and draw rectangles around them
    for obj in decoded_objects:
        # Extract the barcode or QR code data
        data = obj.data.decode('utf-8')

        # Check if the QR code data is not already in the list
        if data not in [x[0] for x in qr_data_list]:
            # Add the QR code data to the list
            qr_data_list.append((data, obj.polygon[0][0] if obj.polygon else 0))

            points = obj.polygon
            if len(points) == 4:
                hull = cv2.convexHull(np.array(points, dtype=np.int32))
                cv2.polylines(image, [hull], True, (0, 255, 0), 2)

    return image

# Main function
def main():
    # Open the video capture device (you can replace 0 with the camera index or video file)
    cap = cv2.VideoCapture(0)

    # List to store QR code data
    qr_data_list = []

    start_time = time.time()

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Break the loop if there's an issue reading the frame
        if not ret:
            break

        try:
            # Call the decode_barcodes function to find and draw QR codes
            result_frame = decode_barcodes(frame, qr_data_list)

            # Display the result frame
            cv2.imshow('Barcode and QR Code Tracking', result_frame)

        except Exception as e:
            print("Error:", str(e))

        # Check if 0.5 seconds have passed
        if time.time() - start_time > 4:
            
            # if qr_data_list is None:
            if not qr_data_list:
                qr_data_list = []

            # Sort the QR codes by their x-coordinate (from left to right)
            qr_data_list.sort(key=lambda x: x[1])

            # Print the QR code data from left to right
            qr_codes_left_to_right = [data for data, _ in qr_data_list]
            print("QR Code Data (Left to Right):", qr_codes_left_to_right)

            # Reset the start time and clear the QR data list
            start_time = time.time()
            qr_data_list.clear()

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Run the main function
if __name__ == "__main__":
    main()
