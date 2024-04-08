import pyautogui
import time
import cv2
import numpy as np
import mss

# Function to check if a pixel's RGB value matches the target color
def check_color(pixel, target_color):
    return pixel[:3] == target_color

# Function to move the mouse to the position of the color detected
def move_to_color_position(position):
    pyautogui.moveTo(position[0], position[1])

# Main function
def main():
    # Set the target color
    target_color = (0, 0, 255)  # Example: looking for pure blue

    try:
        with mss.mss() as sct:
            while True:
                # Capture the screen
                screenshot = sct.grab(sct.monitors[0])

                # Convert the screenshot to an OpenCV image
                img = np.array(screenshot)

                # Convert BGR to RGB (OpenCV uses BGR by default)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Find the position of the color on the screen
                mask = cv2.inRange(img_rgb, target_color, target_color)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    # Get the position of the color
                    x, y, w, h = cv2.boundingRect(contours[0])
                    position = (x + w // 2, y + h // 2)

                    # Move the mouse to the position of the color
                    move_to_color_position(position)

                # Pause briefly before checking again
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()
