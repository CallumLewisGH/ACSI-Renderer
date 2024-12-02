from PIL import Image
import math
import time
import threading
import os

def characterDecide(gsValue):
    if gsValue < 35:
        return "#"
    elif gsValue < 45:
        return "@"
    elif gsValue < 55:
        return "%"
    elif gsValue < 65:
        return "&"
    elif gsValue < 80:
        return "$"
    elif gsValue < 100:
        return "*"
    elif gsValue < 115:
        return "+"
    elif gsValue < 125:
        return "="
    elif gsValue < 140:
        return "~"
    elif gsValue < 155:
        return "-"
    elif gsValue < 165:
        return ";"
    elif gsValue < 175:
        return "!"
    elif gsValue < 185:
        return "?"
    elif gsValue < 200:
        return ":"
    elif gsValue < 215:
        return "."
    elif gsValue < 225:
        return ","
    elif gsValue < 235:
        return "'"
    elif gsValue < 247:
        return "\""
    else:
        return " "

def stringGenerator(characterArray, height, width):
    output = []
    for y in range(height):
        line = "".join(characterArray[x][y] for x in range(width))
        output.append(line)
    return "\n".join(output)

def writeToFile(filename, inputString):
    while True:
        print("\n" * 8)
        print(inputString)
        time.sleep(0.1)
    #output_dir = "assets/ASCI"
    #os.makedirs(output_dir, exist_ok=True)
    #filename = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}-ASCI.txt")
    #with open(filename, 'w') as file:
        #file.write(inputString)
    #print(f"Successfully wrote to {filename}")

def graphicsProcessing(pixels, pixelsChar, width, height, xOffset, yOffset, xEnd, yEnd, contrast):
    for y in range(yOffset, yEnd):
        for x in range(xOffset, xEnd):
            pixelRGB = pixels[x, y]
            gsValue = int((0.299 * pixelRGB[0]) + (0.587 * pixelRGB[1]) + (0.114 * pixelRGB[2]))
            gsValue = max(0, min(255, int(((gsValue - 125) * contrast) + 125)))
            pixelsChar[x][y] = characterDecide(gsValue) + " "

filename = "Donut.jpg"
pixel_density = 64
width = 48
height = 24
contrast = 1
threads = 1

image = Image.open(f"assets/images/{filename}")
image = image.resize((width, height))
width, height = image.size
pixels = image.load()

pixelsChar = [[" " for _ in range(height)] for _ in range(width)]

xDiff = width // threads
yDiff = height // threads

threadList = []

start_time = time.time()

for i in range(threads):
    xOffset = xDiff * i
    xEnd = xOffset + xDiff if i < threads - 1 else width
    thread = threading.Thread(
        target=graphicsProcessing,
        args=(pixels, pixelsChar, width, height, xOffset, 0, xEnd, height, contrast)
    )
    threadList.append(thread)
    thread.start()

for thread in threadList:
    thread.join()

elapsed_time = time.time() - start_time
print(f"{threads} threads - Time Taken: {elapsed_time} seconds")

ascii_art = stringGenerator(pixelsChar, height, width)
writeToFile(filename, ascii_art)
