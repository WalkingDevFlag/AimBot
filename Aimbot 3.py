import numpy as np
import cv2
import time
import pyautogui
import mss

# Get the screen resolution
screen_width, screen_height = pyautogui.size()

# Calculate the coordinates for the 200x200 region in the center of the screen
box_width = 200
box_height = 200
x1 = (screen_width - box_width) // 2  # left
y1 = (screen_height - box_height) // 2  # top
x2 = x1 + box_width  # right
y2 = y1 + box_height  # bottom

# Create a monitor dictionary for the region of interest
monitor = {"top": y1, "left": x1, "width": box_width, "height": box_height}

with mss.mss() as sct:
    while True:
        # Capture the 200x200 region in the center of the screen
        screen = np.array(sct.grab(monitor))
        
        # Display the captured region
        cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        
        # Exit loop if 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
