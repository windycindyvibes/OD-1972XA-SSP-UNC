# PURPOSE OF THIS CODE
# PROJECT
# DATE
# NAME

import math

def convertAngle(degrees, minutes, seconds, radians, normalize):
    # handle a negative angle
    minutes = math.copysign(minutes, degrees)
    seconds = math.copysign(seconds, degrees)

    # perform angle conversion
    x = degrees + minutes/60 + seconds/3600

    # return result
    if radians:
        x = x/180*math.pi
        if normalize:
            x = x%(2*math.pi)
    else:
        if normalize:
            x = x%(360)
    return x
    # YOUR CODE HERE



# test cases for part a
#print(convertAngle(90, 6, 36)) # should print 90.11
#print(convertAngle(-90, 6, 36)) # should print -90.11
#print(convertAngle(-0.0, 30, 45)) # should print -0.5125

# test cases for part b (uncomment these, comment out previous tests)
#print(convertAngle(90, 6, 36, True)) # should print 1.57271618897
#print(convertAngle(-90, 6, 36, True)) # should print -1.57271618897
#print(convertAngle(90, 6, 36, False)) # should print 90.11
#print(convertAngle(-90, 6, 36, False)) # should print -90.11

# these are the test cases you will demonstrate when getting this homework checked off
# test cases for part c (uncomment these, comment out previous tests)
print(convertAngle(90, 6, 36, False, False)) # should print 90.11
print(convertAngle(90, 6, 36, True, False)) # should print 1.57271618897
print(convertAngle(90, 6, 36, False, True)) # should print 90.11
print(convertAngle(90, 6, 36, True, True)) # should print 1.57271618897
print(convertAngle(-90, 6, 36, False, False)) # should print -90.11
print(convertAngle(-90, 6, 36, True, False)) # should print -1.57271618897
print(convertAngle(-90, 6, 36, False, True)) # should print 269.89
print(convertAngle(-90, 6, 36, True, True)) # should print 4.71046911821
print(convertAngle(540, 0, 0, False, True)) # should print 180.0
print(convertAngle(-0.0, 30, 45, False, False)) # should print -0.5125
