import random
from math import sqrt


# a helper module, you can use more submodules like this to keep your code readable, but do import them in main.py


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
        # Adjusted to handle new format
        for visit in route[1:-1]:  # Exclude the depots at the start and end
            location_id = visit['node_id']
            if location_id in instance_dict['pick_up_locations']:
                total_demand += instance_dict['pick_up_locations'][location_id]['demand']
            elif location_id in instance_dict['delivery_locations']:
                total_demand += instance_dict['delivery_locations'][location_id]['demand']
            if total_demand > vehicle_capacity:
                return False
    return True


def check_start_end_at_depot(solution, instance_dict):
    # Extract actual depot IDs for comparison
    depot_ids = {depot_detail['id'] for depot_detail in instance_dict['depots'].values()}

    for route in solution['routes']:
        # Adjusted to handle new format
        start_depot_id, end_depot_id = route[0]['node_id'], route[-1]['node_id']

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
        completed_deliveries = set()  # Track completed deliveries

        for visit in route:
            location_id = visit['node_id']

            # Check if this location is a delivery location
            if location_id in instance_dict['delivery_locations']:
                expected_pickup_id = location_id - total_customers
                # Check if the corresponding pickup has been visited and is not yet delivered
                if expected_pickup_id not in visited_pickups or expected_pickup_id in completed_deliveries:
                    return False
                else:
                    # Mark the delivery as completed
                    completed_deliveries.add(expected_pickup_id)

            elif location_id in instance_dict['pick_up_locations']:
                # Mark this pickup as visited
                visited_pickups.add(location_id)

        # After processing a route, ensure all visited pickups have been delivered
        if not all(pickup in completed_deliveries for pickup in visited_pickups):
            return False

    return True
    
def check_no_duplicate_visits(solution):
    visited_nodes = set()  # Track visited nodes across all routes

    for route in solution['routes']:
        for visit in route[1:-1]:  # Exclude the depots at the start and end
            node_id = visit['node_id']
            # Check if this node has already been visited in any route
            if node_id in visited_nodes:
                return False  # Node visited more than once, fail the check
            else:
                visited_nodes.add(node_id)
    return True  # All nodes visited at most once across all routes, pass the check


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
    return


def calculate_euclidean_distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def total_profit_with_penalties(solution, instance):
    """"
    NOTE: we should change the profit calculation such that:
    -Costs are higher, and it becomes interesting to not serve customers
    -Penalties are higher such that it becomes interesting to optimize the time windows
    -The waiting time at the depot is not included in the waiting time, to start later delivery
    -Make clear that waiting time is in minutes and is a decision variable
    """
    total_distance = 0
    total_penalty = 0  # Initialize total penalty for time window violations
    total_revenue = 0  # Initialize total revenue from sales
    total_waiting_time_hours = 0  # Initialize total waiting time
    truck_cost_per_hour = 20
    truck_speed = 25  # distance units per hour
    penalty_per_hour = 6  # Euro per hour early or late
    revenue_per_demand_unit = 50  # Euro per unit of demand

    # Combine pickup and delivery locations for easy access
    node_data = {**instance['depots'], **instance['pick_up_locations'], **instance['delivery_locations']}

    for route in solution['routes']:
        current_time = 0  # Start of the day for each route
        for i in range(len(route) - 1):
            node_current = route[i]
            node_next = route[i + 1]

            node_id_current = node_current['node_id']
            node_id_next = node_next['node_id']
            waiting_time_hours = node_current['waiting_time'] / 60.0  # Convert waiting time to hours
            total_waiting_time_hours += waiting_time_hours  # Accumulate total waiting time

            x1, y1 = node_data[node_id_current]['x_coord'], node_data[node_id_current]['y_coord']
            x2, y2 = node_data[node_id_next]['x_coord'], node_data[node_id_next]['y_coord']
            travel_time_hours = calculate_euclidean_distance(x1, y1, x2, y2) / truck_speed

            current_time += travel_time_hours + waiting_time_hours
            service_start_time = current_time

            if service_start_time < node_data[node_id_next]['time_window_start']:
                total_penalty += (node_data[node_id_next]['time_window_start'] - service_start_time) * penalty_per_hour
            elif service_start_time > node_data[node_id_next]['time_window_end']:
                total_penalty += (service_start_time - node_data[node_id_next]['time_window_end']) * penalty_per_hour

            # If the current node is a pickup location, calculate revenue
            if node_id_current in instance['pick_up_locations']:
                demand = node_data[node_id_current]['demand']
                total_revenue += demand * revenue_per_demand_unit

            total_distance += travel_time_hours * truck_speed

    total_time_hours = (total_distance / truck_speed) + total_waiting_time_hours
    total_cost = (total_time_hours * truck_cost_per_hour) + total_penalty

    return total_revenue-total_cost  # return profit


def generate_random_routes_from_instance(parsed_data, depot_id, min_size=1, max_size=5, max_waiting_time=10):
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

        # Initialize the route with the depot as the starting point
        route = [{"node_id": depot_id, "waiting_time": 0}]

        # Add nodes to the route with random waiting times
        for node_id in indices[:size]:
            waiting_time = 0
            route.append({"node_id": node_id, "waiting_time": waiting_time})

        # Add the depot as the ending point of the route
        route.append({"node_id": depot_id, "waiting_time": 0})

        routes.append(route)

        # Update the remaining indices
        indices = indices[size:]

    return routes
