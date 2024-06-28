import heapq
import math

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

ROBOT_SPEED = 0.42  # meters per 20 seconds

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def time_to_move(x1, y1, x2, y2):
    return int(distance(x1, y1, x2, y2) / ROBOT_SPEED * 20)

def check_collision(x1, y1, x2, y2, obj):
    # Check if the robot will collide with the object or its boundaries
    if (x1 - obj["width"] / 2 <= x2 <= x1 + obj["width"] / 2 and
        y1 - obj["height"] / 2 <= y2 <= y1 + obj["height"] / 2):
        return True
    return False

def calculate_time_and_battery_consumption(starting_position, object_id):
    # Calculate time and battery consumption for moving to the object
    obj = OBJECTS[object_id]  # object_id is already an integer
    time_consumption = time_to_move(starting_position[0], starting_position[1], obj["x"], obj["y"])
    battery_consumption = time_consumption / 20 * obj["mass"]
    return time_consumption, battery_consumption

def calculate_image_quality(object_id):
    # Calculate image quality for the object
    obj = OBJECTS[object_id]
    return obj["value"]

def greedy_search(starting_position):
    time = 0
    battery = 100
    image_quality = 0
    num_boxes_picked_up = 0
    object_order = []
    movement_path = [starting_position]
    drop_off_zone = [(0.4, 0.4), (0.4, -0.4), (-0.4, 0.4), (-0.4, -0.4)]  # drop off zone

    # Create a priority queue to store objects to visit
    priority_queue = []
    for obj in OBJECTS:
        heapq.heappush(priority_queue, (-obj["value"], obj["id"]))

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

        # Calculate the total time and battery consumption for collecting the object and dropping it off
        ideal_drop_off_position = min(drop_off_zone, key=lambda x: distance(current_position[0], current_position[1], x[0], x[1]))
        time_consumption_to_drop_off = time_to_move(obj["x"], obj["y"], ideal_drop_off_position[0], ideal_drop_off_position[1])
        battery_consumption_to_drop_off = time_consumption_to_drop_off / 20
        total_time_consumption = time_consumption_to_object + time_consumption_to_drop_off
        total_battery_consumption = battery_consumption_to_object + battery_consumption_to_drop_off

        # Check if collecting the box is worth it
        if value > total_battery_consumption and time + total_time_consumption <= 180:  # 300 is the maximum allowed time
            # Update time, battery, and image quality
            time += total_time_consumption
            battery -= total_battery_consumption
            image_quality += value
            num_boxes_picked_up += 1

            # Update current position
            current_position = ideal_drop_off_position
            movement_path.append((obj["x"], obj["y"]))
            movement_path.append(current_position)

            # Add object to the order
            object_order.append(object_id)
        else:
            break

    return object_order, time, battery, image_quality, num_boxes_picked_up, movement_path

def main():
    starting_position = (0.5, 0.5)
    object_order, time, battery, image_quality, num_boxes_picked_up, movement_path = greedy_search(starting_position)
    print("Object Order:", object_order)
    print("Time:", time)
    print("Battery:", battery)
    print("Image Quality:", image_quality)
    print("Number of Boxes Picked Up:", num_boxes_picked_up)
    print("Movement Path:")
    for i, pos in enumerate(movement_path):
        if i == 0:
            print(f"Start at {pos}")
        else:
            print(f"Move to {pos}")

if __name__ == "__main__":
    main()