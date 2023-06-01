import cv2
import numpy as np

def get_line_segments(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to obtain binary image
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    line_segments = []

    # Iterate over the contours and approximate each contour with a line
    for contour in contours:
        # Approximate the contour as a line segment
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Extract the coordinates of the line segment
        segment = [tuple(point[0]) for point in approx]
        line_segments.append(segment)

    return line_segments

# Example usage
image_path = "output.png"
segments = get_line_segments(image_path)

# Print the coordinates of each line segment
for segment in segments:
    print(segment)
