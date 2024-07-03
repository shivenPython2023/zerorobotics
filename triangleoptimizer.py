import heapq
import math
import numpy as np

# Game constants
OBJECTS = [
    {"id": 0, "x": 0.2, "y": 0.2, "width": 0.15, "height": 0.15, "mass": 1, "value": 50},
    {"id": 1, "x": 0.25, "y": -0.25, "width": 0.15, "height": 0.15, "mass": 1, "value": 50},
    {"id": 2, "x": -0.25, "y": -0.1, "width": 0.15, "height": 0.15, "mass": 1, "value": 50},
    {"id": 3, "x": -0.2, "y": 0.2, "width": 0.05, "height": 0.05, "mass": 0.5, "value": 30},
    {"id": 4, "x": 0.15, "y": 0.0, "width": 0.05, "height": 0.05, "mass": 0.5, "value": 30},
    {"id": 5, "x": 0.0, "y": -0.15, "width": 0.05, "height": 0.05, "mass": 0.5, "value": 30}
]

STARTING_POSITIONS = [(0.5, 0.5), (0.5, -0.5), (-0.5, 0.5), (-0.5, -0.5)]

ROBOT_SPEED = 0.25 # meters per 20 seconds

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def time_to_move(x1, y1, x2, y2):
    return int(distance(x1, y1, x2, y2) / ROBOT_SPEED * 9)

def check_collision(x1, y1, x2, y2, obj):
    # Check if the robot will collide with the object or its boundaries
    if (x1 - obj["width"] / 2 <= x2 <= x1 + obj["width"] / 2 and
        y1 - obj["height"] / 2 <= y2 <= y1 + obj["height"] / 2):
        return True
    return False

def calculate_ideal_drop_off_position(obj_being_held_id, next_obj_id):
    obj_being_held = OBJECTS[obj_being_held_id]
    next_obj = OBJECTS[next_obj_id]

    # Get the coordinates of the next object
    next_obj_x = next_obj["x"]
    next_obj_y = next_obj["y"]
    next_obj_cords= (next_obj_x,next_obj_y)

    # Calculate the ideal drop-off position using the old function
    ideal_drop_off_x, ideal_drop_off_y = calculate_ideal_drop_off_position_old(next_obj_cords)
    
    # Calculate the movement path
    movement_path = [(obj_being_held["x"] + t * (ideal_drop_off_x - obj_being_held["x"]), 
                      obj_being_held["y"] + t * (ideal_drop_off_y - obj_being_held["y"])) 
                     for t in np.arange(0, 1, 0.01)]
    
    # Check for collisions with the next object
    while comp_check_collision(obj_being_held, next_obj, movement_path):
        # Calculate the direction to move away from the next object
        dx = ideal_drop_off_x - obj_being_held["x"]
        dy = ideal_drop_off_y - obj_being_held["y"]
        direction = "none"  # default direction
        if dx > 0 and dy > 0:
            direction = "left"
        elif dx > 0 and dy < 0:
            direction = "up"
        elif dx < 0 and dy > 0:
            direction = "down"
        elif dx < 0 and dy < 0:
            direction = "right"

        # Move away from the next object in the calculated direction
        if direction == "left":
            ideal_drop_off_x -= 0.01
        elif direction == "right":
            ideal_drop_off_x += 0.01
        elif direction == "up":
            ideal_drop_off_y += 0.01
        elif direction == "down":
            ideal_drop_off_y -= 0.01
        else:
            # If direction is "none", move in a default direction (e.g., up)
            ideal_drop_off_y += 0.01

        # Recalculate the movement path
        movement_path = [(obj_being_held["x"] + t * (ideal_drop_off_x - obj_being_held["x"]), 
                          obj_being_held["y"] + t * (ideal_drop_off_y - obj_being_held["y"])) 
                         for t in np.arange(0, 1, 0.01)]

    return ideal_drop_off_x, ideal_drop_off_y
def calculate_ideal_drop_off_position_old_old(current_position):
    # Determine the quadrant
    if current_position[0] >= 0 and current_position[1] >= 0:
        quadrant = 1
    elif current_position[0] < 0 and current_position[1] >= 0:
        quadrant = 2
    elif current_position[0] < 0 and current_position[1] < 0:
        quadrant = 3
    else:
        quadrant = 4

    # Calculate the ideal drop-off position based on the quadrant
    if quadrant == 1:
        distances = [
            (distance(current_position[0], current_position[1], 0.4, current_position[1]), 0.4, current_position[1]),
            (distance(current_position[0], current_position[1], current_position[0], 0.4), current_position[0], 0.4)
        ]
    elif quadrant == 2:
        distances = [
            (distance(current_position[0], current_position[1], -0.4, current_position[1]), -0.4, current_position[1]),
            (distance(current_position[0], current_position[1], current_position[0], 0.4), current_position[0], 0.4)
        ]
    elif quadrant == 3:
        distances = [
            (distance(current_position[0], current_position[1], -0.4, current_position[1]), -0.4, current_position[1]),
            (distance(current_position[0], current_position[1], current_position[0], -0.4), current_position[0], -0.4)
        ]
    else:
        distances = [
            (distance(current_position[0], current_position[1], 0.4, current_position[1]), 0.4, current_position[1]),
            (distance(current_position[0], current_position[1], current_position[0], -0.4), current_position[0], -0.4)
        ]

    # Return the ideal drop-off position
    _, x, y = min(distances, key=lambda x: x[0])
    return x, y
def calculate_ideal_drop_off_position_old(current_position):
    # Determine the quadrant
    if current_position[0] >= 0 and current_position[1] >= 0:
        quadrant = 1
    elif current_position[0] < 0 and current_position[1] >= 0:
        quadrant = 2
    elif current_position[0] < 0 and current_position[1] < 0:
        quadrant = 3
    else:
        quadrant = 4

    # Calculate the ideal drop-off position based on the quadrant
    if quadrant == 1:
        distances = [
            (distance(current_position[0], current_position[1], 0.4, current_position[1]), (0.4, current_position[1])),
            (distance(current_position[0], current_position[1], current_position[0], 0.4), (current_position[0], 0.4))
        ]
    elif quadrant == 2:
        distances = [
            (distance(current_position[0], current_position[1], -0.4, current_position[1]), (-0.4, current_position[1])),
            (distance(current_position[0], current_position[1], current_position[0], 0.4), (current_position[0], 0.4))
        ]
    elif quadrant == 3:
        distances = [
            (distance(current_position[0], current_position[1], -0.4, current_position[1]), (-0.4, current_position[1])),
            (distance(current_position[0], current_position[1], current_position[0], -0.4), (current_position[0], -0.4))
        ]
    else:
        distances = [
            (distance(current_position[0], current_position[1], 0.4, current_position[1]), (0.4, current_position[1])),
            (distance(current_position[0], current_position[1], current_position[0], -0.4), (current_position[0], -0.4))
        ]

    # Return the ideal drop-off position
    return min(distances, key=lambda x: x[0])[1]

def calculate_time_and_battery_consumption(starting_position, object_id):
    # Calculate time and battery consumption for moving to the object
    obj = OBJECTS[object_id]  # object_id is already an integer
    time_consumption = time_to_move(starting_position[0], starting_position[1], obj["x"], obj["y"])
    battery_consumption = time_consumption / 9 * obj["mass"]
    return time_consumption, battery_consumption

def calculate_image_quality(object_id):
    # Calculate image quality for the object
    obj = OBJECTS[object_id]
    return obj["value"]

def calculate_distance(obj, current_position):
    return ((obj["x"] - current_position[0]) ** 2 + (obj["y"] - current_position[1]) ** 2) ** 0.5

def prioritize_objects():
    return [(0, 0), (1, 4), (2, 1), (3, 5), (4, 2), (5, 3)]

def comp_check_collision(obj_being_held, obj_to_check, movement_path):
    # Calculate the bounding box of the object being held
    obj_being_held_width = obj_being_held["width"]
    obj_being_held_height = obj_being_held["height"]
    obj_being_held_x_min = -obj_being_held_width / 2
    obj_being_held_x_max = obj_being_held_width / 2
    obj_being_held_y_min = -obj_being_held_height / 2
    obj_being_held_y_max = obj_being_held_height / 2

    # Calculate the bounding box of the object to check
    obj_to_check_width = obj_to_check["width"]
    obj_to_check_height = obj_to_check["height"]
    obj_to_check_x = obj_to_check["x"]
    obj_to_check_y = obj_to_check["y"]
    obj_to_check_x_min = obj_to_check_x - obj_to_check_width / 2
    obj_to_check_x_max = obj_to_check_x + obj_to_check_width / 2
    obj_to_check_y_min = obj_to_check_y - obj_to_check_height / 2
    obj_to_check_y_max = obj_to_check_y + obj_to_check_height / 2

    # Check for collisions along the movement path
    for segment_x, segment_y in movement_path:
        if (obj_being_held_x_min + segment_x <= obj_to_check_x_max and
            obj_being_held_x_max + segment_x >= obj_to_check_x_min and
            obj_being_held_y_min + segment_y <= obj_to_check_y_max and
            obj_being_held_y_max + segment_y >= obj_to_check_y_min):
            return True  # collision detected
    print('got e')
    return False  # no collision detected


def greedy_search(starting_position):
    time = 0
    battery = 100
    image_quality = 0
    num_boxes_picked_up = 0
    object_order = []
    movement_path_list = [starting_position] 

    # Create a priority queue to store objects to visit
    priority_queue = prioritize_objects() 

    current_position = starting_position

    while priority_queue:
        _, object_id = heapq.heappop(priority_queue)
        obj = OBJECTS[object_id]

        # Check if the robot will collide with the object or its boundaries

        if check_collision(current_position[0], current_position[1], obj["x"], obj["y"], obj):
            continue

        # Calculate time and battery consumption for moving to the object
        time_consumption_to_object, battery_consumption_to_object = calculate_time_and_battery_consumption(current_position, object_id)

        # Check if the robot has enough battery to move to the object and collect it
        if battery - battery_consumption_to_object < 0:
            break

        # Calculate the value of collecting the box
        value = calculate_image_quality(object_id)

        if object_id == 0:
            next_obj=4
        elif object_id == 4:
            next_obj=1
        elif object_id == 1:
            next_obj = 5
        elif object_id ==5:
            next_obj = 2
        elif object_id ==2:
            next_obj = 3
        
        # Calculate the ideal drop-off position
        if object_id is not 3:
            ideal_drop_off_x, ideal_drop_off_y = calculate_ideal_drop_off_position(object_id, next_obj)
        else:
            ideal_drop_off_x, ideal_drop_off_y = calculate_ideal_drop_off_position_old_old((obj["x"],obj["y"]))

        # Calculate the total time and battery consumption for collecting the object and dropping it off
        time_consumption_to_drop_off = time_to_move(obj["x"], obj["y"], (ideal_drop_off_x, ideal_drop_off_y)[0], (ideal_drop_off_x, ideal_drop_off_y)[1])
        battery_consumption_to_drop_off = time_consumption_to_drop_off / 20
        total_time_consumption = time_consumption_to_object + time_consumption_to_drop_off
        total_battery_consumption = battery_consumption_to_object + battery_consumption_to_drop_off

        # Update time, battery, and image quality
        time += total_time_consumption
        battery -= total_battery_consumption
        round_battery= round(battery,1)
        image_quality += value
        num_boxes_picked_up += 1

        # Update current position
        current_position = (ideal_drop_off_x, ideal_drop_off_y)
        movement_path_list.append((obj["x"], obj["y"]))
        movement_path_list.append(current_position)

        # Add object to the order
        object_order.append(object_id)
        print(object_id)

    return object_order, time, round_battery, image_quality, num_boxes_picked_up, movement_path_list


def main():
    starting_position = (0.5, 0.5)
    object_order, time, round_battery, image_quality, num_boxes_picked_up, movement_path_list= greedy_search(starting_position)
    print("Object Order:", object_order)
    print("Time:", time)
    print("Battery:", round_battery)
    print("Image Quality:", image_quality)
    print("Number of Boxes Picked Up:", num_boxes_picked_up)
    print("Score:", 0.8*(180-time) + round_battery + 1.2*image_quality)
    print("Movement Path:")
    
    for i, pos in enumerate(movement_path_list):
        if i == 0:
            print(f"Start at {pos}")
        else:
            print(f"Move to {pos}")

if __name__ == "__main__":
    main()
