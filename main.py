from PIL import Image
import math

def characterDecide(gsValue):
    if gsValue < 35:
        pixelChar = "#"

    elif gsValue < 45:
        pixelChar = "@"

    elif gsValue < 55:
        pixelChar = "%"

    elif gsValue < 65:
        pixelChar = "&"

    elif gsValue < 80:
        pixelChar = "$"

    elif gsValue < 100:
        pixelChar = "*"

    elif gsValue < 115:
        pixelChar = "+"

    elif gsValue < 125:
        pixelChar = "="

    elif gsValue < 140:
        pixelChar = "~"

    elif gsValue < 155:
        pixelChar = "-"

    elif gsValue < 165:
        pixelChar = ";"

    elif gsValue < 175:
        pixelChar = "!"

    elif gsValue < 185:
        pixelChar = "?"

    elif gsValue < 200:
        pixelChar = ":"

    elif gsValue < 215:
        pixelChar = "."

    elif gsValue < 225:
        pixelChar = ","

    elif gsValue < 235:
        pixelChar = "'"

    elif gsValue < 247:
        pixelChar = "\""

    else:
        pixelChar = " "

    return pixelChar

def stringGenerator(characterArray, height, width):
    string = ""
    for y in range(height):  # Iterate over height first
        for x in range(width):
            string += characterArray[x][y]
        string += "\n"
    return string

def writeToFile(filename, inputString):
    filename = filename.split(".")[0]
    filename = f"assets\ASCI\{filename}-ASCI.txt"
    with open(filename, 'w') as file:
        file.write(inputString)

    print(f"Successfully wrote to {filename}")

filename = input("Enter File name as string Including extensions such as png: ")
pixel_density = int(input("Enter you pixel density for example 4 pixels becomes 1 you input would be 4: "))
contrast = int(input("Enter Contrast: "))

image = Image.open(f"assets\images\{filename}")

width, height = image.size

image = image.resize((width // pixel_density, height // pixel_density))

width, height = image.size

pixels = image.load()

pixelsChar = [[" " for _ in range(height)] for _ in range(width)]

processed_pixels = 0

for y in range(height):
    for x in range(width):
        pixelRGB = pixels[x, y]
        gsValue = math.floor((0.299 * pixelRGB[0]) + (0.587 * pixelRGB[1]) + (0.114 * pixelRGB[2]))
        gsValue = math.floor(((125 - gsValue) * contrast) + 125)
        pixels[x, y] = (gsValue,gsValue,gsValue)
        pixelsChar[x][y] = characterDecide(gsValue) + " "

        processed_pixels += 1
        completion_percent = (processed_pixels / ( height * width)) * 100

        if completion_percent % 1 == 0:
            print(f"{completion_percent}% complete")


# Write to file using the corrected stringGenerator

image.show()
writeToFile(filename, stringGenerator(pixelsChar, height, width))
