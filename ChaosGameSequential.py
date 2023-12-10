import matplotlib.pyplot as plt
import numpy as np
import time

start_time = 0

def plot_point(ax, point, color='k', marker='o'):
    ax.plot(point[0], point[1], marker, color=color, markersize=1)

def chaos_game(vertices, iterations):
    # Select a random starting point within the triangle
    current_point = np.random.rand(2)

    # Store points in a list
    points = []

    for _ in range(iterations):
        # Randomly choose one of the vertices
        chosen_vertex = vertices[np.random.choice(len(vertices))]
        # Calculate the midpoint between the current point and the chosen vertex
        current_point = (current_point + chosen_vertex) / 2
        # Store the midpoint in the list
        points.append(current_point)

    # Convert the list of points to a NumPy array for efficient plotting
    points = np.array(points)


    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")

    plt.figure(figsize=(6, 6))
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    # Plot all the points at once
    ax.plot(points[:, 0], points[:, 1], 'ko', markersize=1)

    # Plot the vertices of the triangle
    for vertex in vertices:
        plot_point(ax, vertex, color='r', marker='o')

    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # Define the vertices of the equilateral triangle
    triangle_vertices = np.array([(0, 0), (1, 0), (0.5, np.sqrt(3)/2)])

    # Set the number of iterations
    num_iterations = 10000000

    # Measure execution time
    start_time = time.time()

    # Generate the Chaos Game plot
    chaos_game(triangle_vertices, num_iterations)

