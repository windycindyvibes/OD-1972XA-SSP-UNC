import math

def get_magnitude(vec):
    magnitude = 0.0
    for x in vec:
        magnitude += x**2
    magnitude = math.sqrt(magnitude)
    return magnitude

def dot_product(vec1, vec2):
    product = 0
    for i in range(0, len(vec1)):
        product += vec1[i] * vec2[i]
    return product

def cross_product(vec1, vec2):
    ans = [0,0,0]
    ans[0] = vec1[1] * vec2[2] - vec1[2] * vec2[1]
    ans[1] = vec1[2] * vec2[0] - vec1[0] * vec2[2]
    ans[2] = vec1[0] * vec2[1] - vec1[1] * vec2[0]
    return ans

print(get_magnitude([]))
print(get_magnitude([3]))
print(get_magnitude([1,-1]))
print(get_magnitude([1,1,1,1]))

print(dot_product([], []))
print(dot_product([2,5,6], [3,7,8]))
print(dot_product([1,-1,0], [-1,-1,5]))
print(dot_product([1,0,1,0], [2,2,0,2]))

print(cross_product([1,0,0], [0,1,0]))
print(cross_product([1,0,0], [0,0,1]))
print(cross_product([2,5,6], [3,7,8]))
