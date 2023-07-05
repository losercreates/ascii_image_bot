import telebot
from PIL import Image, ImageDraw, ImageFont
import math
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
charArray = list(chars)
charLength = len(charArray)
interval = charLength/256

oneCharWidth = 10
oneCharHeight = 18

def getChar(inputInt):
    return charArray[math.floor(inputInt*interval)]

@bot.message_handler(commands=['start'])
def handle_start(message):
    instructions = "Welcome to the ASCII Art Bot! 😄\n\n" \
                   "Send me an image and I will convert it into ASCII art for you!\n\n" \
                   "Please note that the quality and generation timr of the ASCII art " \
                   "depends on the complexity of the image and may vary.\n\n" \
                   "Please use a low resolution image\n\n" \
                   "To get started, simply send me a photo!"

    bot.send_message(message.chat.id, instructions)

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    # Get the photo file ID and download the image
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Load the image using PIL
    image = Image.open(BytesIO(downloaded_file)).convert('RGB')

    # Generate the ASCII image
    width, height = image.size
    scaleFactor = math.ceil(2000 / height) * 0.1
    image = image.resize((int(scaleFactor * width), int(scaleFactor * height * (oneCharWidth / oneCharHeight))), Image.NEAREST)
    width, height = image.size
    pix = image.load()

    output_image = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(0, 0, 0))
    draw = ImageDraw.Draw(output_image)

    for i in range(height):
        for j in range(width):
            r, g, b = pix[j, i]
            h = int(r/3 + g/3 + b/3)
            pix[j, i] = (h, h, h)
            draw.text((j*oneCharWidth, i*oneCharHeight), getChar(h), font=fnt, fill=(r, g, b))

    # Save the ASCII image to a BytesIO object
    ascii_image_buffer = BytesIO()
    output_image.save(ascii_image_buffer, format='PNG')
    ascii_image_buffer.seek(0)

    # Send the ASCII image back to the user
    bot.send_photo(message.chat.id, photo=ascii_image_buffer)

@bot.message_handler(func=lambda message: True)
def handle_invalid_input(message):
    error_message = "Invalid input! Please send me a photo to convert it into ASCII art."

    bot.reply_to(message, error_message)

if __name__ == '__main__':
    fnt = ImageFont.truetype('lucon.ttf', 15)
    bot.polling()
