import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime

import subprocess

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json



def GetCoin(coinid):
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
  parameters = {
      'id':coinid

  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '8c96ea5b-b76a-4e79-a5ee-4706f58be1f6',
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    return(data)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

def GetPrice(coinid, coindata):
  coinprice = coindata['data'][coinid]['quote']['USD']['price']
  return(str(float('%.4g' % coinprice)))




# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)


    coindata = GetCoin('1, 1027, 2130')
    draw.text((x, top), "BTC: "+GetPrice('1', coindata),  font=font, fill=255)
    draw.text((x, top+8), "ETH: "+GetPrice('1027', coindata), font=font, fill=255)
    draw.text((x, top+16), "ENJ: "+GetPrice('2130', coindata), font=font, fill=255)
    draw.text((x, top+24), "-- "+str(datetime.now().strftime('%H:%M:%S')), font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(600)