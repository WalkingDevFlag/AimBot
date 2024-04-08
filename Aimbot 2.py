import pyautogui
import time
import cv2
import numpy as np
import mss

# Function to check if a pixel's RGB value matches the target color
def check_color(pixel, target_color):
    return pixel[:3] == target_color

# Function to move the cursor within the box based on the position of the color detected
def move_cursor_in_box(box_center, position):
    x, y = position
    box_x, box_y = box_center
    move_x = x - box_x
    move_y = y - box_y
    pyautogui.move(move_x, move_y)

# Main function
def main():
    # Set the target color
    target_color = (0, 0, 255)  # Example: looking for pure blue

    # Get the center coordinates of the screen
    screen_width, screen_height = pyautogui.size()
    box_center = (screen_width // 2, screen_height // 2)

    # Define the box size
    box_size = 10  # 1cm x 1cm box

    # Define the screen size
    screen_width_display = 600
    screen_height_display = 600

    try:
        with mss.mss() as sct:
            while True:
                # Create a blank image for the screen
                screen_img = np.zeros((screen_height_display, screen_width_display, 3), dtype=np.uint8)

                # Draw the box on the screen
                box_left = screen_width_display // 2 - box_size // 2
                box_top = screen_height_display // 2 - box_size // 2
                box_right = screen_width_display // 2 + box_size // 2
                box_bottom = screen_height_display // 2 + box_size // 2
                cv2.rectangle(screen_img, (box_left, box_top), (box_right, box_bottom), (0, 255, 0), 2)

                # Capture the screen
                screenshot = sct.grab(sct.monitors[0])

                # Convert the screenshot to an OpenCV image
                img = np.array(screenshot)

                # Convert BGR to RGB (OpenCV uses BGR by default)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Crop the image to the box boundaries
                box_img = img_rgb[box_top:box_bottom, box_left:box_right]

                # Find the position of the color in the box
                mask = cv2.inRange(box_img, target_color, target_color)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    # Get the position of the color
                    x, y, w, h = cv2.boundingRect(contours[0])
                    position = (box_left + x + w // 2, box_top + y + h // 2)

                    # Move the cursor within the box based on the detected color
                    move_cursor_in_box(box_center, position)

                # Show the image with the box drawn
                cv2.imshow('Screen with Box', cv2.cvtColor(screen_img, cv2.COLOR_RGB2BGR))
                cv2.waitKey(1)

                # Pause briefly before checking again
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()
