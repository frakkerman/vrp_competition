import numpy as np
import random

# an example file, you can use more submodules like this to keep your code readable, but import them in main.py


def read_instance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines


def parse_instance(instance):
    # Function to extract section data dynamically
    def extract_section_data(start_idx, count):
        section_data = {}
        actual_count = 0
        for i in range(count):
            line = instance[start_idx + i].strip().split()
            if len(line) == 6:
                actual_count += 1
                node_id = int(line[0])
                section_data[node_id] = {
                    'id': int(line[0]),
                    'x_coord': int(line[1]),
                    'y_coord': int(line[2]),
                    'demand': int(line[3]),
                    'time_window_start': int(line[4]),
                    'time_window_end': int(line[5]),
                }
            else:
                print("Warning, mismatch while parsing instance!")
        if actual_count != count:
            print("Warning, mismatch while arsing instance!")
        return section_data, start_idx + count

    # Extracting cardinalities directly from the instance list
    cardinalities = {
        'depots': int(instance[7].strip()),
        'pick_up_locations': int(instance[3].strip()),
        'delivery_locations': int(instance[5].strip()),
    }

    # Starting line index for depots, pickups, and deliveries
    depots_start_line = 17
    pickups_start_line = depots_start_line + cardinalities['depots'] + 1
    deliveries_start_line = pickups_start_line + cardinalities['pick_up_locations'] + 1

    # Parsing data dynamically
    depots, _ = extract_section_data(depots_start_line, cardinalities['depots'])
    pickups, _ = extract_section_data(pickups_start_line, cardinalities['pick_up_locations'])
    deliveries, _ = extract_section_data(deliveries_start_line, cardinalities['delivery_locations'])

    number_of_trucks = int(instance[9].strip())
    vehicle_capacity = int(instance[11].strip())

    # Verifying cardinality
    cardinality_checks = {
        'depots': len(depots) == cardinalities['depots'],
        'pick_up_locations': len(pickups) == cardinalities['pick_up_locations'],
        'delivery_locations': len(deliveries) == cardinalities['delivery_locations'],
    }

    # Return structured data
    return {
        'depots': depots,
        'pick_up_locations': pickups,
        'delivery_locations': deliveries,
        'number_of_trucks': number_of_trucks,
        'vehicle_capacity': vehicle_capacity,
        'cardinality_checks': cardinality_checks,
    }


def check_vehicle_capacity(solution, instance_dict, vehicle_capacity):
    for route in solution['routes']:
        total_demand = 0
        for location_id in route[1:-1]:  # Exclude the depots at the start and end
            if location_id in instance_dict['pick_up_locations']:
                total_demand += instance_dict['pick_up_locations'][location_id]['demand']
            if total_demand > vehicle_capacity:
                return False
    return True


def check_start_end_at_depot(solution, instance_dict):
    # Extract actual depot IDs for comparison
    depot_ids = {depot_detail['id'] for depot_detail in instance_dict['depots'].values()}

    for route in solution['routes']:
        start_depot_id, end_depot_id = route[0], route[-1]

        # Check if the start and end depot IDs are in the set of depot IDs
        if start_depot_id not in depot_ids or end_depot_id not in depot_ids:
            return False
    return True


def check_number_of_trucks(solution, number_of_trucks):
    return len(solution['routes']) <= number_of_trucks


def check_pickup_before_delivery(solution, instance_dict):
    total_customers = len(instance_dict['pick_up_locations'])

    for route in solution['routes']:
        visited_pickups = set()  # Track visited pickups
        for location_id in route:
            # Check if this location is a delivery location
            if location_id in instance_dict['delivery_locations']:
                # Calculate the expected pickup ID for this delivery
                expected_pickup_id = location_id - total_customers
                # Check if the corresponding pickup has been visited
                if expected_pickup_id not in visited_pickups:
                    return False
            elif location_id in instance_dict['pick_up_locations']:
                # Mark this pickup as visited
                visited_pickups.add(location_id)
    return True


def check_solution_feasibility(solution, instance_dict):
    vehicle_capacity = instance_dict.get('vehicle_capacity', 0)  # Default to 0 if not found
    number_of_trucks = instance_dict.get('number_of_trucks', 0)  # Default to 0 if not found

    if not check_vehicle_capacity(solution, instance_dict, vehicle_capacity):
        print("Warning: Vehicle capacity exceeded.")
    if not check_start_end_at_depot(solution, instance_dict):
        print("Warning: Route does not start and end at a depot.")
    if not check_number_of_trucks(solution, number_of_trucks):
        print("Warning: Number of trucks exceeded.")
    if not check_pickup_before_delivery(solution, instance_dict):
        print("Warning: Delivery location visited before corresponding pickup location.")


def generate_random_routes_from_instance(parsed_data, depot_id, min_size=1, max_size=5):
    # Extract IDs of all pickup and delivery locations
    pickup_ids = list(parsed_data['pick_up_locations'].keys())
    delivery_ids = list(parsed_data['delivery_locations'].keys())

    # Combine pickup and delivery IDs into a single list
    indices = pickup_ids + delivery_ids

    # Shuffle the indices to randomize the routes
    random.shuffle(indices)

    routes = []
    while indices:
        # Ensure the size is within the remaining indices and account for the depot
        size = random.randint(min_size, min(max_size, len(indices)))

        # Create a route starting and ending at the depot
        route = [depot_id] + indices[:size] + [depot_id]
        routes.append(route)

        # Update the remaining indices
        indices = indices[size:]

    return routes
