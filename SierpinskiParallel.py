from mpi4py import MPI
import matplotlib.pyplot as plt
import numpy as np
import time

start_time = 0

def sierpinski_triangle(vertices, depth, triangles):
    if depth == 0:
        triangles.append(vertices)
        return

    v0, v1, v2 = vertices

    midpoints = [((v0[0] + v1[0]) / 2, (v0[1] + v1[1]) / 2),
                 ((v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2),
                 ((v2[0] + v0[0]) / 2, (v2[1] + v0[1]) / 2)]

    sierpinski_triangle((v0, midpoints[0], midpoints[2]), depth - 1, triangles)
    sierpinski_triangle((midpoints[0], v1, midpoints[1]), depth - 1, triangles)
    sierpinski_triangle((midpoints[2], midpoints[1], v2), depth - 1, triangles)

def parallel_sierpinski(comm, rank, size, initial_triangles, recursion_depth):
    triangles = []

    # Divide the initial triangles among processes
    start_index = rank * len(initial_triangles) // size
    end_index = (rank + 1) * len(initial_triangles) // size
    process_triangles = initial_triangles[start_index:end_index]

    # Each process independently computes its part
    for triangle in process_triangles:
        sierpinski_triangle(triangle, recursion_depth, triangles)

    # Gather all triangles from each process to process 0
    all_triangles = comm.gather(triangles, root=0)

    if rank == 0:
        # Flatten the list of lists to get a single list of triangles
        all_triangles = [triangle for sublist in all_triangles for triangle in sublist]
        # Measure Time before plotting 
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution Time: {execution_time} seconds")

        # Plot all collected triangles
        plt.figure(figsize=(6, 6))
        for triangle in all_triangles:
            x, y = zip(*triangle, triangle[0])
            plt.plot(x, y, 'k')

        plt.axis('equal')
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Define the vertices of the initial triangle
    initial_triangles = [((0, 0), (1, 0), (0.5, np.sqrt(3)/2))]

    # Set the depth of recursion
    recursion_depth = 5

    start_time = time.time()
    parallel_sierpinski(comm, rank, size, initial_triangles, recursion_depth)
    
        
