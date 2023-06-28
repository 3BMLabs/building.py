from PIL import Image

def remove_white_background(input_path, output_path):
    image = Image.open(input_path)
    image = image.convert("RGBA")

    new_image = Image.new("RGBA", image.size, (0, 0, 0, 0))

    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))

            if pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200:
                new_image.putpixel((x, y), (0, 0, 0, 0))
            else:
                new_image.putpixel((x, y), pixel)

    new_image = new_image.convert("RGB")
    new_image.save(output_path, "PNG")

    # Open the saved image and convert it back to RGBA
    saved_image = Image.open(output_path)
    saved_image = saved_image.convert("RGBA")

    # Iterate over the image pixels and set any pixel with alpha > 0 to have a max width of 1
    for x in range(saved_image.width):
        for y in range(saved_image.height):
            pixel = saved_image.getpixel((x, y))

            if pixel[3] > 0:
                saved_image.putpixel((x, y), (pixel[0], pixel[1], pixel[2], 255))

    saved_image.save(output_path, "PNG")

input_path = "input.jpg"
output_path = "output2.png"
remove_white_background(input_path, output_path)
