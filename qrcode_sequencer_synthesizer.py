import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time
from synthesizer import Player, Synthesizer, Waveform

def play_sounds(qr_codes):
    # Create a player and synthesizer
    player = Player()
    player.open_stream()
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=0.5, use_osc2=False)

    # Define frequencies for each QR code number
    frequencies = {
        '1': 261.63,  # C4
        '2': 293.66,  # D4
        '3': 329.63,  # E4
        '4': 349.23,  # F4
        '5': 392.00,  # G4
        '6': 440.00,  # A4
    }

    # Play tones based on QR code data
    for qr_code in qr_codes:
        if qr_code in frequencies:
            frequency = frequencies[qr_code]
            wave = synthesizer.generate_constant_wave(frequency, length=0.5)  # Specify the length here
            player.play_wave(wave)

    print("Finished playing sounds")





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
        if data not in qr_data_list:
            # Add the QR code data to the list
            qr_data_list.append(data)

            points = obj.polygon
            if len(points) == 4:
                hull = cv2.convexHull(np.array(points, dtype=np.int32))
                cv2.polylines(image, [hull], True, (0, 255, 0), 2)

    # Sort the QR codes based on the X-coordinate of the bounding box
    decoded_objects.sort(key=lambda obj: obj.rect[0])

    return image


# Main function
def main():
    # Open the video capture device (you can replace 0 with the camera index or video file)
    cap = cv2.VideoCapture(0)

    # List to store QR code data
    qr_data_list = []

    start_time = time.time()

    # Create a list to store the sequence
    sequence = []

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
        if time.time() - start_time > 0.5:
            # Print the QR code data from left to right
            qr_codes_left_to_right = qr_data_list
            print("QR Code Data (Left to Right):", qr_codes_left_to_right)

            # Play sounds based on QR code data
            play_sounds(qr_codes_left_to_right)

            # Add the QR code data to the sequence list
            sequence.append(qr_codes_left_to_right)

            # Reset the start time and clear the QR data list
            start_time = time.time()
            qr_data_list.clear()

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close all windows
    cap.release()
    cv2.destroyAllWindows()

    # Print the entire sequence
    print("Full Sequence:", sequence)

# Run the main function
if __name__ == "__main__":
    main()
