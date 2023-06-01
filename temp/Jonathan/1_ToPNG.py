from PIL import Image

def remove_white_background(input_path, output_path):
    # Open the image
    image = Image.open(input_path)

    # Convert the image to RGBA
    image = image.convert("RGBA")

    # Create a blank image with a transparent background
    new_image = Image.new("RGBA", image.size, (0, 0, 0, 0))

    # Iterate over each pixel in the image
    for x in range(image.width):
        for y in range(image.height):
            # Get the pixel value at the current position
            pixel = image.getpixel((x, y))

            # Check if the pixel is mostly white
            if pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200:
                # Set the pixel in the new image as transparent
                new_image.putpixel((x, y), (0, 0, 0, 0))
            else:
                # Set the pixel in the new image as the original pixel
                new_image.putpixel((x, y), pixel)

    # Save the image as a PNG file
    new_image.save(output_path, "PNG")

# Example usage
input_path = "input.jpg"
output_path = "output.png"
remove_white_background(input_path, output_path)
