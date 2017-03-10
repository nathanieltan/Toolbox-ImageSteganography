"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    redPixels = red_channel.load()

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()


    for x in range(x_size):
        for y in range(y_size):
            pixel = redPixels[x,y]

            binaryString = bin(pixel)

            if binaryString[-1] == '1':
                pixels[x,y] = (255,255,255)
            else:
                pixels[x,y] = (0,0,0)


    decoded_image.save("images/decoded_image.png")

def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    unencoded_image = Image.open(template_image)
    unencodedPixels = unencoded_image.load()

    textImage = write_text(text_to_encode, unencoded_image.size)
    encoded_image = Image.new("RGB", unencoded_image.size)

    textPixels = textImage.load()
    pixels = encoded_image.load()

    redPixels = (unencoded_image.split()[0]).load()
    greenPixels = (unencoded_image.split()[1]).load()
    bluePixels = (unencoded_image.split()[2]).load()

    for x in range(unencoded_image.size[0]):
        for y in range(unencoded_image.size[1]):
            binaryString = bin(redPixels[x,y])
            if textPixels[x,y] == (255,255,255):
                binaryString = binaryString[0:-1]+'1'
            else:
                binaryString = binaryString[0:-1]+'0'
            pixels[x,y] = (int(binaryString,2),greenPixels[x,y],bluePixels[x,y])
    encoded_image.save("images/encoded_image.png")

if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image("wow I like memes, and wow, Sophie Li is like, the best Soft Des ninja ever. I was like, totally not paid off to say that. But like, I could be paid to say that in the future. <3")
