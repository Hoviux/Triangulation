import cv2
import numpy as np
import random
import math


def draw_voronoi(img, subdiv):
    (facets, centers) = subdiv.getVoronoiFacetList([])

    for i in range(0, len(facets)):
        ifacet_arr = []
        for f in facets[i]:
            ifacet_arr.append(f)

        ifacet = np.array(ifacet_arr, np.int)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        cv2.fillConvexPoly(img, ifacet, color, 0)
        ifacets = np.array([ifacet])
        cv2.polylines(img, ifacets, True, (0, 0, 0), 1, 0)
        cv2.circle(img, (centers[i][0], centers[i][1]), 10, (0, 0, 0), -1)


def draw_delaunay(img, subdiv, delaunay_color):
    triangleList = subdiv.getTriangleList()
    size = img.shape
    r = (0, 0, size[1], size[0])

    for t in triangleList:

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

# Needed to caculate area of triangle
        #print(str(pt1))
        #print(str(pt2))
        #print(str(pt3))
        #triangle_size(pt1, pt2, pt3)

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
            cv2.line(img, pt1, pt2, delaunay_color, 5)
            cv2.line(img, pt2, pt3, delaunay_color, 5)
            cv2.line(img, pt3, pt1, delaunay_color, 5)

## Shiiiiit wich doesn't works
def triangle_size(pt1, pt2, pt3):
    xp1 = pt1[0]
    xp2 = pt2[0]
    xp3 = pt3[0]
    yp1 = pt1[1]
    yp2 = pt2[1]
    yp3 = pt3[1]

    print('Первая точка : x = ', str(xp1), ' y = ', str(yp1))
    print('Вторая точка : x = ', str(xp2), ' y = ', str(yp2))
    print('Третья точка : x = ', str(xp2), ' y = ', str(yp3))


    pass
##Shiiiit


def draw_point(img, p, color):
    cv2.circle(img, p, 10, color, -1)


def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True


if __name__ == '__main__':

    # Define window names
    win_delaunay = "Delaunay Triangulation"
    win_voronoi = "Voronoi Diagram"

    cv2.namedWindow(win_delaunay, cv2.WINDOW_NORMAL)
    cv2.namedWindow(win_voronoi, cv2.WINDOW_NORMAL)

    # Turn on animation while drawing triangles
    animate = True

    # Define colors for drawing.
    delaunay_color = (255, 0, 255)
    points_color = (255, 0, 0)

    # Read in the image.
    img = cv2.imread("2.jpg", 1)

    # Keep a copy around
    img_orig = img.copy()

    # Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])

    # Create an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect)

    # Create an array of points.
    points = []

    # Read in the points from a text file
    with open("points.txt") as file:
        for line in file:
            x, y = line.split()
            points.append((int(x), int(y)))

    # Insert points into subdiv
    for p in points:
        subdiv.insert(p)

        # Show animation
        if animate:
            img_copy = img_orig.copy()
            # Draw delaunay triangles
            draw_delaunay(img_copy, subdiv, (0, 255, 0))
            cv2.imshow(win_delaunay, img_copy)
            cv2.waitKey(100)

    # Draw delaunay triangles
    draw_delaunay(img, subdiv, (0, 255, 0))

    # Draw points
    for p in points:
        draw_point(img, p, (0, 0, 255))

    # Allocate space for Voronoi Diagram
    img_voronoi = np.zeros(img.shape, dtype=img.dtype)

    # Draw Voronoi diagram
    draw_voronoi(img_voronoi, subdiv)

    # Show results
    cv2.imshow(win_delaunay, img)
    cv2.imshow(win_voronoi, img_voronoi)
    cv2.imwrite('Delanay_triangulation.jpg', img)
    cv2.imwrite('Voronoy_diagram.jpg', img_voronoi)
    cv2.waitKey(0)


