def get_angular_momentum_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

        position = lines[1].strip().split()
        position = [6.6846E-09*float(value) for value in position]

        velocity = lines[3].strip().split()
        velocity = [6.6846E-09*5022642.89055*float(value) for value in velocity]
    
    angular_momentum = [0., 0., 0.]
    angular_momentum[0] = round(position[1]*velocity[2] - position[2]*velocity[1], 6) 
    angular_momentum[1] = round(position[2]*velocity[0] - position[0]*velocity[2], 6)
    angular_momentum[2] = round(position[0]*velocity[1] - position[1]*velocity[0], 6)

    return angular_momentum