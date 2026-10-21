from PIL import Image
import numpy as np
import copy
import sys

class image():
    def __init__(self, ref, rx = 0, ry = 0):
        if ref == None:
            self.resolution = [rx, ry]
            self.pixels = []
            for i2 in range(ry):
                self.pixels.append([])
                for i3 in range(rx):
                    self.pixels[-1].append([])
                    for i in range(3):
                        self.pixels[-1][-1].append(255)
        else:
            # Initialize the image based on parameters
            img = Image.open(ref)
            width, height = img.size
            self.resolution = [width, height]
            ref = np.asarray(img)
            self.resolution = [ref.shape[1], ref.shape[0]]
            self.pixels = ref.tolist()
    
    def save_image(self, name):
        '''
        Saves the result, always uses 3 channels.

        If there are fewer than 3 channels, it adds new empty ones until there are 3.

        If there are more than 3 channels, it removes the 4th one and those after.
        '''
        to_save = copy.deepcopy(self.pixels)
        # Add extra channels to make the image "saveable"
        channel_length = len(self.pixels[0][0])
        if channel_length < 3:
            for i in range(3 - channel_length):
                for y in range(self.resolution[1]):
                    for x in range(self.resolution[0]):
                        to_save[y][x].append(0)
        # Reduce to 3 channels to make the image "saveable"
        for y in range(self.resolution[1]):
            for x in range(self.resolution[0]):
                to_save[y][x] = to_save[y][x][:3]
        # Save the image
        array_np = np.array(to_save, dtype=np.uint8)
        Image.fromarray(array_np).save(name + ".png")

def breakDown(img1, img2):
    # Get the colours in the image
    colours = {}
    for y in range(img1.resolution[1]):
        for x in range(img1.resolution[0]):
            colours[str(img2.pixels[y][x][0]) + "," + str(img2.pixels[y][x][1]) + "," + str(img2.pixels[y][x][2])] = img2.pixels[y][x]
    # Indexing
    colourIndex = {}
    colourCount = 0
    colourPoints = []
    for i in colours:
        colourIndex[i] = colourCount
        colourCount += 1
        colourPoints.append([])
    # Split points
    for y in range(img1.resolution[1]):
        for x in range(img1.resolution[0]):
            txt = str(img2.pixels[y][x][0]) + "," + str(img2.pixels[y][x][1]) + "," + str(img2.pixels[y][x][2])
            colourPoints[colourIndex[txt]].append([x, y])
    # Image split
    for i in range(colourCount):
        newImg = image(None, img1.resolution[0], img1.resolution[1])
        for p in colourPoints[i]:
            newImg.pixels[p[1]][p[0]] = img1.pixels[p[1]][p[0]]
        newImg.save_image("result_" + str(i))

def run(img1, img2):
    newImg1 = image(img1)
    newImg2 = image(img2)
    if newImg1.resolution[0] == newImg2.resolution[0] and newImg1.resolution[1] == newImg2.resolution[1]:
        breakDown(newImg1, newImg2)
    else:
        raise IndexError("The resolutions aren't the same! (" + str(newImg1.resolution) + "/" + str(newImg2.resolution) + ")")