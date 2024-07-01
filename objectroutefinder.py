import itertools

# Distance matrix based on the given data
distance_matrix = [
    [0, 0.453, 0.541, 0.4, 0.206, 0.403],
    [0.453, 0, 0.522, 0.636, 0.269, 0.269],
    [0.541, 0.522, 0, 0.304, 0.412, 0.255],
    [0.4, 0.636, 0.304, 0, 0.403, 0.403],
    [0.206, 0.269, 0.412, 0.403, 0, 0.212],
    [0.403, 0.269, 0.255, 0.403, 0.212, 0]
]

# Number of objects
num_objects = len(distance_matrix)

# Function to calculate the total distance for a given order of objects
def calculate_total_distance(order, distance_matrix):
    total_distance = 0
    for i in range(len(order) - 1):
        total_distance += distance_matrix[order[i]][order[i + 1]]
    return total_distance

# Generate all permutations of the objects
permutations = list(itertools.permutations(range(num_objects)))

# Find the optimal order with the minimum distance
min_distance = float('inf')
optimal_order = None

for perm in permutations:
    distance = calculate_total_distance(perm, distance_matrix)
    if distance < min_distance:
        min_distance = distance
        optimal_order = perm

# Output the optimal order and the minimum distance
print("Optimal Order of Objects:", optimal_order)
print("Minimum Total Distance:", min_distance)