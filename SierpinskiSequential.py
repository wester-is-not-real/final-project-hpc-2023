import matplotlib.pyplot as plt
import numpy as np
import time

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

if __name__ == "__main__":
    # Define the vertices of the initial triangle
    initial_triangle = [(0, 0), (1, 0), (0.5, np.sqrt(3)/2)]

    # Set the depth of recursion
    recursion_depth = 14

    # Collect triangles during recursion
    triangles = []
    start_time = time.time()
    sierpinski_triangle(tuple(initial_triangle), recursion_depth, triangles)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")
    # Plot all collected triangles
    plt.figure(figsize=(6, 6))
    for triangle in triangles:
        x, y = zip(*triangle, triangle[0])
        plt.plot(x, y, 'k')

    plt.axis('equal')
    plt.axis('off')
    plt.show()

    
