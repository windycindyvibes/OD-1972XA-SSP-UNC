# PURPOSE OF THIS CODE
# PROJECT
# DATE
# NAME 

import matplotlib.pyplot as plt

# beach_portrait_gray.png is an RGB image, so image is a 3D array with 3 values at each pixel location
# the slice is to remove an unnecessary alpha channel, if present
image = plt.imread('D:/SSP/homework two/beach_portrait.png')[:, :, :3]


def blur(old_img, radius):
    # YOUR CODE HERE TO PRODUCE AND RETURN A NEW array THAT IS A BLURRED VERSION OF img
    img = old_img.copy()
    for row in range(radius, len(img)-radius+1):
        for column in range(radius, len(img[row])-radius+1):
            for i in range(0, 3):
                img[row][column][i] = old_img[row-radius:row+radius+1, column-radius:column+radius+1, i].mean()
        
    for row in range(0, radius):
        for column in range(0, radius):
            for i in range(0, 3):
                img[row][column][i] = old_img[0:row+radius+1, 0:column+radius+1][i].mean()
    
    for row in range(len(img)-radius+1, len(img)):
        for column in range(len(img[row])-radius+1, len(img[row])):
            for i in range(0, 3):
                img[row][column][i] = old_img[row-radius:len(img), column-radius:len(img[row])][i].mean()

    for row in range(0, radius):
        for column in range(len(img[row])-radius+1, len(img[row])):
            for i in range(0, 3):
                img[row][column][i] = old_img[0:row+radius+1, column-radius:len(img[row])][i].mean()

    for row in range(len(img)-radius+1, len(img)):
        for column in range(0, radius):
            for i in range(0,3):
                img[row][column][i] = old_img[row-radius:len(img), 0:column+radius+1][i].mean()

    return img
        
plt.imsave("beach_portrait_blur.png", blur(image, 3))