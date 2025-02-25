# The Steps I planed before typing codes.
# Opens Camera
# Displays Video
# Captures Frames by keyboard
# Decodes QR Codes
# Prints Results

# OpenCV is used for image and video processing.
import cv2
# This library is used for reading QR codes.
import pyzbar.pyzbar as pyzbar
# import time, but I've not used it,just for a test.

# This function handles capturing video, extracting frames, and decoding QR codes.
def capture_and_decode_qr():

    # creates a video capture object.
    # The argument 0 typically selects the default camera which is my laptop webcam.
    cap = cv2.VideoCapture(0)

    # This checks if the camera opened successfully.
    # If not, it prints an error message and exits the function.
    if not cap.isOpened():
        print("Webcam Error.")
        return

    # Flag to indicate if capturing is active
    # A boolean variable that keeps track of whether I've started the frame capture.
    capturing = False

    # List to store the captured frames
    extracted_frames = []

    # This loop continuously reads frames from the camera.
    while True:

        # Reads a frame from the camera.
        # ret is a boolean indicating whether the frame was read successfully.
        # frame is the actual image data as a NumPy array.
        ret, frame = cap.read()

        # block handles the case where a frame could not be read.
        if not ret:
            print("Read Frame Error.")
            break

        # Display the frame with instructions
        if not capturing:
            # displays the current frame from the camera and adds text instructions
            # The instructions change depending on the capturing state.
            cv2.putText(frame, "Press 's' to start capturing, 'q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Press 'e' to extract frame, 'q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # cv2.imshow displays the frame in a window.
        cv2.imshow("Camera Feed", frame)

        # Key Press Handling
        key = cv2.waitKey(1)  # Wait for 1ms for key press

        if key == ord('s'):  # Start capturing
            capturing = True
            print("Capturing started.")
        elif key == ord('e') and capturing:  # Extract frame
            extracted_frames.append(frame.copy()) # copy the frame
            print(f"Frame extracted. Total frames: {len(extracted_frames)}")
        elif key == ord('q'):  # Quit
            break


    # Cleanup : Releases the camera resource and closes the OpenCV windows.
    cap.release()
    cv2.destroyAllWindows()

    # QR Code Processing
    # Process extracted frames for QR codes
    for i, frame in enumerate(extracted_frames): # iterates
        decoded_data = decode_qr_from_image(frame) # to decode any QR codes in each frame
        if decoded_data:
            print(f"QR code data in frame {i+1}: {decoded_data}")
        else:
            print(f"No QR code found in frame {i+1}")

# this function takes an image, converts it to grayscale, uses pyzbar to find QR codes, extracts the data from those QR codes
# Decodes QR codes from a given image.
def decode_qr_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for better QR detection
    barcodes = pyzbar.decode(gray)

    decoded_data = []
    for barcode in barcodes:
        data = barcode.data.decode("utf-8")  # Decode from bytes to string
        decoded_data.append(data)
    return decoded_data

# This ensures that the capture_and_decode_qr() function is called only when the script is run directly.
if __name__ == "__main__":
    capture_and_decode_qr()