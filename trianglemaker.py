import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_ideal_drop_off_position(current_position, next_object_position):
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
            (distance(current_position[0], current_position[1], 0.351, current_position[1]), (0.351, current_position[1])),
            (distance(current_position[0], current_position[1], current_position[0], 0.36), (current_position[0], 0.36))
        ]
    elif quadrant == 2:
        distances = [
            (distance(current_position[0], current_position[1], -0.351, current_position[1]), (-0.351, current_position[1])),
            (distance(current_position[0], current_position[1], current_position[0], 0.36), (current_position[0], 0.36))
        ]
    elif quadrant == 3:
        distances = [
            (distance(current_position[0], current_position[1], -0.351, current_position[1]), (-0.351, current_position[1])),
            (distance(current_position[0], current_position[1], current_position[0], -0.351), (current_position[0], -0.351))
        ]
    else:
        distances = [
            (distance(current_position[0], current_position[1], 0.351, current_position[1]), (0.351, current_position[1])),
            (distance(current_position[0], current_position[1], current_position[0], -0.351), (current_position[0], -0.351))
        ]

    # Check if the slope of the line between the origin and the current position is 1 or -1
    slope = current_position[1] / current_position[0] if current_position[0]!= 0 else float('inf')
    if slope == 1 or slope == -1:
        print("in here:")
        # Return the edge that is closest to the next object
        if distance(current_position[0], current_position[1], next_object_position[0], next_object_position[1]) > distance(distances[0][1][0], distances[0][1][1], next_object_position[0], next_object_position[1]):
            return distances[0][1]
        else:
            return distances[1][1]
    else:
        # Return the ideal drop-off position
        return min(distances, key=lambda x: x[0])[1]

def generate_movement_path(current_object, next_object, current_position, value):
    # Calculate the cap of the loop
    dx = next_object[0] - current_position[0]
    dy = next_object[1] - current_position[1]
    if abs(dx) > abs(dy):
        cap = next_object[0]
        changing_value = current_position[0]
        increment = 0.005 if current_position[0] < next_object[0] else -0.005
    else:
        cap = next_object[1]
        changing_value = current_position[1]
        increment = 0.005 if current_position[1] < next_object[1] else -0.005

    # Initialize the best movement path and score
    best_movement_path = []
    best_score = -float('inf')

    ideal_drop_off_position = calculate_ideal_drop_off_position(current_position, next_object)
    
    # Loop until the changing value reaches the cap
    while abs(changing_value - cap) > 0.01:
        # Calculate the ideal drop-off position for the current object


        # Calculate the distances and battery consumption for the two line segments
        distance1 = distance(current_position[0], current_position[1], ideal_drop_off_position[0], ideal_drop_off_position[1])
        distance2 = distance(ideal_drop_off_position[0], ideal_drop_off_position[1], next_object[0], next_object[1])
        battery_consumption = (50 + current_object[2]) * (distance1)
        timeconsumption= 65.85 * (distance1+distance2)

        # Calculate the score for this movement path
        score = value - (timeconsumption*0.8 + battery_consumption)
        print(score)
        if changing_value < -0.1:
            break

        # Update the best movement path and score if necessary
        if score > best_score:
            best_movement_path = [current_position, ideal_drop_off_position, next_object]
            best_score = score

        # Update the changing value
        changing_value += increment

        # Update the current position
        if abs(dx) > abs(dy):
            ideal_drop_off_position = (changing_value, ideal_drop_off_position[1])
        else:
            ideal_drop_off_position = (ideal_drop_off_position[0], changing_value)

    # Return the best movement path
    return best_movement_path

# Example usage
#first number represents the object currently held, the next two represent the x and y of the currently held object
current_object_value = 70
current_object_stats = (0, 0.13, 0.27, 10)
next_object_loc = (-0.13, 0.27)
current_position = (0.13, 0.27)

movement_path = generate_movement_path(current_object_stats, next_object_loc, current_position, current_object_value)
print("Movement Path:", movement_path)
