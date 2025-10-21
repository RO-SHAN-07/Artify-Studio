import cv2
from PIL import Image
import turtle

import os
import sys

def convert_to_jpg(image_path):
    """
    Converts an image to JPG format if it's not already.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The path to the JPG image, or None if conversion fails.
    """
    try:
        img = Image.open(image_path)
        if img.format.lower() in ['jpg', 'jpeg']:
            print("Image is already in JPG format.")
            return image_path

        print(f"Converting image from {img.format} to JPG...")
        base, _ = os.path.splitext(image_path)
        jpg_path = base + ".jpg"

        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        img.save(jpg_path, 'jpeg')
        print(f"Image saved as {jpg_path}")
        return jpg_path

    except (IOError, OSError) as e:
        print(f"Error processing image: {e}")
        return None

def process_image(image_path):
    """
    Processes the image to create a black and white sketch.

    Args:
        image_path (str): The path to the JPG image.
    """
    try:
        print("Processing image...")
        img = cv2.imread(image_path)

        img = cv2.resize(img, (300, 300))

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray_img, 100, 200)

        bw_image_path = "bw_image.jpg"
        cv2.imwrite(bw_image_path, edges)
        print(f"Processed image saved as {bw_image_path}")

        cv2.imshow("Original Image", img)
        cv2.imshow("Processed Image", edges)

        print("Press any key to close the image previews...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return bw_image_path

    except Exception as e:
        print(f"An error occurred during image processing: {e}")
        return None

def draw_with_turtle(image_path):
    """
    Renders the processed image using Turtle Graphics.

    Args:
        image_path (str): The path to the processed black and white image.
    """
    try:
        print("Rendering with Turtle Graphics...")
        img = Image.open(image_path).convert('L')
        width, height = img.size

        screen = turtle.Screen()
        screen.setup(width + 20, height + 20)
        screen.setworldcoordinates(0, height, width, 0)
        screen.title("Turtle Drawing")
        turtle.tracer(0, 0)

        pen = turtle.Turtle()
        pen.speed(0)
        pen.penup()
        pen.hideturtle()
        pen.color("black")

        print("Drawing started...")
        for y in range(height):
            for x in range(width):
                brightness = img.getpixel((x, y))
                if brightness == 255:
                    pen.goto(x, y)
                    pen.dot(2)
            if y % 10 == 0:
                screen.update()

        screen.update()
        print("Turtle drawing complete. Click on the window to exit.")
        screen.exitonclick()

    except Exception as e:
        print(f"An error occurred during Turtle Graphics rendering: {e}")
        try:
            turtle.bye()
        except turtle.Terminator:
            pass

def main():
    """
    Main function to run the image to sketch and draw application.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_image>")
        return

    image_path = sys.argv[1]
    print(f"Loading image from: {image_path}")

    jpg_image_path = convert_to_jpg(image_path)

    if jpg_image_path:
        print(f"Image ready for processing: {jpg_image_path}")
        processed_image_path = process_image(jpg_image_path)
        if processed_image_path:
            draw_with_turtle(processed_image_path)
    else:
        print("Could not process the image.")

if __name__ == "__main__":
    main()
