# PURPOSE OF THIS CODE
# PROJECT
# DATE
# NAME

import matplotlib.pyplot as plt

# oz_bluescreen and meadow are a RGB images, so image and background are 3D arrays
# and have 3 values at every pixel location
# the slice is to remove an unnecessary alpha channel, if present
image = plt.imread("D:/SSP/homework two/oz_bluescreen.png")[:, :, :3]
background = plt.imread("D:/SSP/homework two/meadow.png")[:, :, :3]


# YOUR CODE HERE TO MODIFY image TO PUT THE WIZARD AND HIS BALLOON IN THE MEADOW
for row in range(len(image)):
  for column in range(len(image[row])):
    if image[row][column][2] > (image[row][column][0] + image[row][column][1]):
      image[row][column] = background[row][column]

# save the modified image to a new file called oz_meadow.png
plt.imsave("oz_meadow.png", image)