from display import *
from matrix import *


def add_circle( points, cx, cy, cz, r, step ):
    theta = 2*math.pi/step
    theta1 = float(0)
    while theta1 < 10.0:
        cos0 = cx + r*math.cos(theta1)
        sin0 = cy + r*math.sin(theta1)
        theta1 += theta
        cos1 = cx + r*math.cos(theta1)
        sin1 = cy + r*math.sin(theta1)
        add_edge(points, cos0, sin0, cz, cos1, sin1, cz)

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    def cubic(t , c):
        return c[0] * math.pow(t,3) + c[1] * math.pow(t,2) + c[2] * math.pow(t,1) + c[3]

    if curve_type == 'hermite':
        rx0 = x2
        ry0 = y2
        rx1 = x3
        ry1 = y3
        Cx, Cy = make_hermite(x0,y0,x1,y1, rx0, ry0, rx1, ry1)
        dt = float(1/step)
        t = float(0)
        while t < 1.0:
            x = cubic(t, Cx)
            y = cubic(t, Cy)
            t += dt
            x0 = cubic(t, Cx)
            y0 = cubic(t, Cy)
            add_edge(points, x, y, 0,x0, y0 ,0)
    elif curve_type == 'bezier':
        Cx1, Cy1 = make_bezier(x0, y0, x1, y1, x2, y2, x3, y3)
        dt = float(1/step)
        t = float(0)
        while t < 1.0:
            x = cubic(t, Cx1)
            y = cubic(t, Cy1)
            t += dt
            x0 = cubic(t, Cx1)
            y0 = cubic(t, Cy1)
            add_edge(points, x, y, 0,x0, y0 ,0)



def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print ('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )




def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
