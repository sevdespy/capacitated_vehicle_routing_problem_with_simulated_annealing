import random #to generate random numbers and make random selections
import math #for mathematical functions and constants

distance_matrix = [
     [0, 448611, 591924, 3863, 483555, 269697, 493869, 410305, 877571],
     [450053, 0, 483966, 154226, 697236, 700143, 924315, 731766, 1228502],
     [58949, 480755, 0, 34477, 460973, 562904, 900641, 1098323, 1595059],
     [38726, 155622, 34934, 0, 549806, 494314, 815754, 77319, 1269923],
     [484764, 698296, 460301, 550466, 0, 315262, 617247, 900634, 1247748],
     [270057, 708694, 566826, 494365, 312669, 0, 343838, 589118, 93306],
     [494349, 932986, 904386, 817784, 618029, 342106, 0, 724025, 836274],
     [403507, 730996, 1102078, 772338, 901058, 59016, 724548, 0, 632475],
     [871633, 1228601, 1599683, 1269943, 1248796, 937898, 836796, 632603, 0]
] #distance between cities

vehicles = [50, 25, 25] #vehicle capacities
demands = [0, 15, 13, 8, 12, 7, 11, 9, 10] #demands of cities

def simulated_annealing(distance_matrix, vehicles, demands, num_iterations=10000, alpha=0.99, initial_temperature=100): #to define the SA function

    def total_distance(route, distance_matrix): #takes the parameters of a route and distance_matrix and to calculate the total distance of the given route
        distance = 0 # to calculate the total distance of the given route
        for i in range(len(route) - 1): # to loop every element in the route list except the last element
            distance += distance_matrix[route[i]][route[i + 1]] #to calculate distance from current city to next city in loop
        return distance #to return the total distance

    def swap_two_nodes(route): #to create a new route by taking a route parameter and randomly swapping two cities on the route
        new_route = route[:] #to create a new route without changing the original route
        i, j = random.sample(range(1, len(route) - 1), 2) #to randomly assign and randomly select two different indexes in the route
        new_route[i], new_route[j] = new_route[j], new_route[i] #to relocate
        return new_route #to generate new solutions

    def generate_initial_solution(distance_matrix, vehicles, demands): #to generate a random solution initially by assigning cities to random vehicles
        cities = list(range(1, len(distance_matrix))) #to create a city list
        random.shuffle(cities) #to mix the cities so that the initial solution is random
        routes = [] #to include the route of each vehicle in the solution
        vehicle_idx = 0 #to represent the index of the current vehicle in the vehicles list
        remaining_capacity = vehicles[vehicle_idx] #to keep track of how much load a vehicle can carry and when it will be full
        current_route = [0] #to represent the current vehicle's route and 0 depots i.e. starting city

        for city in cities: #to start a loop to check the requests on each city in the cities list
            demand = demands[city] #to be used to compare the city's demand with the remaining capacity of the current vehicle
            if remaining_capacity - demand >= 0: #to check if the remaining capacity of the existing vehicle can meet the city's demand
                current_route.append(city) #if the vehicle can meet the city's demand, to add the city to the existing route
                remaining_capacity -= demand #to subtract the city's demand from the remaining capacity of the current vehicle
            else:
                current_route.append(0) #ends the current route and to return the route to the repository
                routes.append(current_route) #to add the current route to the list of routes
                vehicle_idx += 1 #to switch to the next vehicle
                if vehicle_idx < len(vehicles): #if there are more available tools to run the code in this block
                    remaining_capacity = vehicles[vehicle_idx] #to update the current vehicle's capacity
                else:
                    break
                current_route = [0] #to start a new route and set the warehouse as the starting city
                current_route.append(city) #to add the current city to the new route
                remaining_capacity -= demand #to subtract the city's demand from the remaining capacity of the current vehicle

        if current_route: #to run the codes in this block if the last created route is not empty
            current_route.append(0) #to finish the last route and return the route to the repository
            routes.append(current_route) #to add the last route to the list of routes
            
        return routes #to return the starting routes

    def calculate_total_distance(routes, distance_matrix): #to calculate the total distance of all routes
        return sum(total_distance(route, distance_matrix) for route in routes)

    routes = generate_initial_solution(distance_matrix, vehicles, demands) #to create the starting routes using the given
    temperature = initial_temperature #to set the starting temperature

    for _ in range(num_iterations): #to perform the specified number of iterations
        new_routes = [swap_two_nodes(route) for route in routes] #to create new routes by randomly swapping two nodes on existing routes
        current_distance = calculate_total_distance(routes, distance_matrix) #to calculate the total distance of available routes
        new_distance = calculate_total_distance(new_routes, distance_matrix) #to calculate the total distance of new routes created
        if new_distance < current_distance: #to check if the total distance of new routes is less than the total distance of existing routes
            routes = new_routes #to consider the new routes as existing routes if the total distance of the new routes is lower
        else:
            probability = math.exp(-(new_distance - current_distance) / temperature) #to calculate the probability that new routes will be accepted
            if random.random() < probability: #to decide whether to accept new routes by comparing a random number with the probability of being accepted
                routes = new_routes #to update existing routes if new routes are accepted
        temperature *= alpha #to control the rate of temperature drop

    return routes, calculate_total_distance(routes, distance_matrix) #to return the best found routes and the total distance of those routes

routes, total_distance = simulated_annealing(distance_matrix, vehicles, demands) #to calculate the best routes and the total distance using the function

print("Optimal routes:")
for i, route in enumerate(routes, 1): #to get the index of each route and the route using the list of routes in a loop by starting the indexes at 1
    print(f"Vehicle {i}: {' -> '.join(map(str, route))}") #to convert all elements to string and print the route of each vehicle by separating all cities with ->

print(f"\nTotal distance: {total_distance}")
