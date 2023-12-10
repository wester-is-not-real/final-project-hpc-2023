from mpi4py import MPI
import matplotlib.pyplot as plt
import numpy as np
import time

def plot_point(ax, point, color='k', marker='o'):
    ax.plot(point[0], point[1], marker, color=color, markersize=1)

def parallel_chaos_game(vertices, iterations, rank, size):
    # Initialize MPI
    comm = MPI.COMM_WORLD

    # Broadcast the vertices to all processes
    vertices = comm.bcast(vertices, root=0)

    # Select a random starting point within the triangle
    current_point = np.random.rand(2)

    # Calculate the number of iterations for each process
    local_iterations = iterations // size

    # Store local points in a list
    local_points = []

    for _ in range(local_iterations):
        # Randomly choose one of the vertices
        chosen_vertex = vertices[np.random.choice(len(vertices))]
        # Calculate the midpoint between the current point and the chosen vertex
        current_point = (current_point + chosen_vertex) / 2
        # Store the midpoint in the list
        local_points.append(current_point)

    # Gather all local points to the root process
    all_points = comm.gather(local_points, root=0)

    if rank == 0:
        # Flatten the list of points
        points = [point for sublist in all_points for point in sublist]
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
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Define the vertices of the equilateral triangle
    triangle_vertices = np.array([(0, 0), (1, 0), (0.5, np.sqrt(3)/2)])

    # Set the number of iterations
    num_iterations = 10000000

    # Measure execution time
    start_time = time.time()

    # Broadcast the number of iterations to all processes
    num_iterations = comm.bcast(num_iterations, root=0)

    # Parallel Chaos Game plot
    parallel_chaos_game(triangle_vertices, num_iterations, rank, size)
