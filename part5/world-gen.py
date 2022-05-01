import numpy as np
import random

def world_gen(size):
    # size = (100,50)

    # 0 = N, 1 = H, 2 = T, 3 = B
    world = np.zeros(size, dtype=int)
    for row in range(len(world)):
        for col in range(len(world[row])):
            world[row][col] = random.choices([0,1,2,3], weights=[0.5, 0.2, 0.2, 0.1])[0]
    
    return world

def is_valid(world, pos):
    if pos[0] < 0 or pos[1] < 0:
        return False
    
    if pos[0] >= world.shape[0] or pos[1] >= world.shape[1]:
        return False

    if world[pos[0]][pos[1]] == 3:
        return False
    
    return True

def execute_action(world, pos, action):
    temp_pos = pos
    if action == "U":
        temp_pos = (temp_pos[0] - 1, temp_pos[1])
    elif action == "L":
        temp_pos = (temp_pos[0], temp_pos[1] - 1)
    elif action == "D":
        temp_pos = (temp_pos[0] + 1, temp_pos[1])
    elif action == "R":
        temp_pos = (temp_pos[0], temp_pos[1] + 1)
    
    if is_valid(world, temp_pos):
        if random.random() < 0.9:
            pos = temp_pos
    
    return pos

def sensor_reading(world, pos):
    terrain = ["N", "H", "T"]
    reading = terrain[world[pos[0]][pos[1]]]
    
    if random.random() > 0.9:
        terrain.remove(reading)
        reading = random.choices(terrain)[0]
    
    return reading

def write_world(name, world):
    # name = "world.txt"
    terrain = ["N", "H", "T", "B"]
    with open(name, "w") as file:
        for row in range(world.shape[0]):
            for col in range(world.shape[1]):
                file.write(terrain[world[row][col]])
                if col != world.shape[1] - 1:
                    file.write(" ")
            if row != world.shape[0] - 1:
                file.write("\n")


def write_world_data(name, start, positions, actions, readings):
    # name = "world_data.txt"

    with open(name, 'w') as file:
        file.write(str(start[0]) + " " + str(start[1]))

        for element in positions:
            file.write("\n" + str(element[0]) + " " + str(element[1]))
        
        for element in actions:
            file.write("\n" + element)
        
        for element in readings:
            file.write("\n" + element)

def gen_ground_truth(world):
    actions_options = ["U", "L", "D", "R"]
    terrain_options = ["N", "H", "T", "B"]
    actions = []
    positions = []
    readings = []
    while True:
        start_y = random.randint(0, world.shape[0]-1)
        start_x = random.randint(0, world.shape[1]-1)
        if world[start_y][start_x] != 3:
            break
    print(world)

    start = (start_y, start_x)
    pos = (start_y, start_x)

    # print(random.choices(actions_options))
    for i in range(100):
        action = random.choices(actions_options)[0]
        pos = execute_action(world, pos, action)
        actions.append(action)
        positions.append(pos)
        readings.append(sensor_reading(world, pos))
    
    print(start)
    print(actions)
    print(positions)
    print(readings)

    # write_world(world)
    # write_world_data(start, positions, actions, readings)

    return start, positions, actions, readings

def generate():
    for i in range(1, 11):
        world_name = "world" + str(i) + ".txt"
        world = world_gen((100,50))
        write_world(world_name, world)
        for j in range(1, 11):
            world_data_name = "world" + str(i) + "_data" + str(j) + ".txt"
            start, positions, actions, readings = gen_ground_truth(world)
            write_world_data(world_data_name, start, positions, actions, readings)

def main():
    generate()

if __name__ == "__main__":
    main()