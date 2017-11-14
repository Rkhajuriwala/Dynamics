from math import sin as s
from math import cos as c
import math
import numpy as np
from Main import Robot




l = [1, 1, 1]
r = [0.5, 0.5, 0.5] # r0 r1 r2
m = [1, 1, 1]
I = [[1, 1, 1], [1, 1, 1], [1, 1, 1]] # Ix Iy Iz


def make_mass_matrix(robot):

    """

    :param theta_1: angle for joint 1
    :param theta_1: angle for joint 2
    :param theta_1: angle for joint 3
    :return: mass matrix
    """

    I,m,l,r = robot.uppack()
    theta_1 = robot.q[0]
    theta_2 = robot.q[1]
    theta_3 = robot.q[2]

    M_11 = I[1][1] * s(theta_2) ** 2 + I[2][1] * s(theta_2 + theta_3) ** 2 + \
           I[0][2] + I[1][2] * c(theta_2) ** 2 + \
           I[1][2] * c(theta_2 + theta_3) ** 2
    M_12 = 0

    M_13 = 0
    M_21 = 0
    M_22 = I[1][0] + I[2][0] + m[2] * l[0] ** 2 + \
           m[1] * r[0] ** 2 + m[1] ** 2 + \
           2 * m[2] * l[0] * r[1] * c(theta_3)

    M_23 = I[2][0] + m[2] * r[1] ** 2 + \
           m[2] * l[0] * r[1] * c(theta_3)


    M_31 = 0
    M_32 = I[2][0] + m[2] * r[1] ** 2 + \
           m[2] * l[1] * r[1] * c(theta_3)
    M_33 = I[2][0] + m[2] * r[1] ** 2



    M = np.matrix([ [ M_11, M_12, M_13],
                    [ M_21, M_22, M_23],
                    [ M_31, M_32, M_33] ] )
    return  M


def make_gravity_matrix(robot):
    """

    :param theta_1: angle for joint 1
    :param theta_1: angle for joint 2
    :param theta_1: angle for joint 3
    :return: gravity matix
    """
    I, m, l, r = robot.uppack()
    theta_1 = robot.q[0]
    theta_2 = robot.q[1]

    gravity = 9.81

    G_1 = 0


    G_2 = -(m[1] * r[0] + m[2] * l[0]) * gravity * c(theta_2) \
          - m[2] * r[1] * c(theta_2 + theta_3)

    G_3 = -m[2] * gravity * r[1] * c(theta_2 + theta_3)

    G = np.matrix([ [ G_1 ], [ G_2 ], [ G_3 ] ])


    return G


def make_coriolis_matrix(robot):
    """

    :param theta_1: angle for joint 1
    :param theta_1: angle for joint 2
    :param theta_1: angle for joint 3
    :return: coriolis matrix
    """

    I, m, l, r = robot.uppack()
    theta_1 = robot.q[0]
    theta_2 = robot.q[1]
    theta_3 = robot.q[2]

    theta_23 = theta_2 + theta_3
    C =  np.zeros(shape=(3,3))

    gamma_001 = 0.5*( I[1][2] - I[2][2] - m[1]*r[1]^2)*s(2*theta_2) + 0.5*(  I[2][1] - I[2][2] )*s(2*theta_23) \
                 -m[2]*(l[1]*c(theta_2) + r[2]*c(theta_23))*(l[1]*s(theta_2) + r[2] *s(theta_23))

    gamma_002 = 0.5*(I[2][1] - I[2][2])*c(2*theta_23) -m[2]*r[2]*s(theta_23)*(l[1] *c(theta_2) + r[2]*c(theta_23))

    gamma_010 = 0.5*(I[1][1] - I[1][2] - m[1]*r[1]^2 )*c(2*theta_2) + 0.5*( I[2][1] - I[2][2])*c(2*theta_2) \
                - m[2]*(  l[1]*c(theta_2) + r[2]*c(theta_23) )*( l[1]*s(theta_2) + r[2]*s(theta_23)  )

    gamma_020 = 0.5*( I[2][1] - I[2][2] )*sin(2*theta_23) - m[2]*r[2]*s(theta_23)*( l[1]*c(theta_2) + r[2]*c(theta_23))

    gamma_100 = 0.5*(I[1][2] - I[1][1] + m[1]*r[1]^2)*s(2*theta_2) + 0.5*(I[2][2] - I[2][1])*s(2*theta_23) + \
                m[2]*( l[1]*c(theta_2) + r[2]*c(theta_23) )*(l[1]*s(theta_2) +  r[2]*s(theta_23) )


    gamma_112 = -l[1]*m[2]*r[2]*s(theta_3)

    gamma_121 = gamma_112
    gamma_122 = gamma_112


    gamma_200 = 0.5*(I[2][2] - I[2][1]) + m[1]*r[2]*s(theta_23)*(l[1]*c(theta_2) + r[2]*c(theta_23))
    gamma_211 = l[1]*m[2]*r[2]*s(theta_3)


    C[0,0] = gamma_001 + gamma_002
    C[0, 1] = gamma_010
    C[0, 2] = gamma_020
    C[1,0] = gamma_100
    C[1, 1] = gamma_112
    C[1, 2] = gamma_121 + gamma_122

    C[2,0] = gamma_200
    C[2,1] = gamma_211


    return C


def get_jacobian_matricies(robot):
    """

    :param theta_1: angle for joint 1
    :param theta_1: angle for joint 2
    :param theta_1: angle for joint 3
    :return: cartesian pose of links
    """

    I, m, l, r = robot.uppack()
    theta_1 = robot.q[0]
    theta_2 = robot.q[1]
    theta_3 = robot.q[2]


    J_1 =  np.zeros(shape=(6,3))
    J_1[5,0] = 1


    J_2 = np.matrix(  [ [-r[0] * c(theta_2), 0, 0],
                        [  0,                              0,                0],
                        [0, -r[0], 0],
                        [  0,                             -1,                0],
                        [  -s(theta_2),                    0,                0],
                        [c(theta_2),                       0,                0] ] )

    J_3 = np.matrix( [ [l[1] * c(theta_2) - r[1] * c(theta_2 + theta_3), 0, 0],
                       [0, l[0] * s(theta_1), 0],
                       [0, -l[1] - l[0] * c(theta_3), -r[1]],
                       [ 0,                                          -1,                    -1 ],
                       [-s(theta_2+theta_3),                          0,                     0 ],
                       [c(theta_2+theta_3),                           0,                     0 ] ])

    return (J_1, J_2, J_3)


def fk( robot):
    """

    :param theta_1: angle for joint 1
    :param theta_1: angle for joint 2
    :param theta_1: angle for joint 3
    :return: cartesian pose of links
    """

    I, m, l, r = robot.uppack()
    theta_1 = robot.q[0]
    theta_2 = robot.q[1]
    theta_3 = robot.q[2]

    pose_1 = (0,0,l[0])

    pose_2 = ( l[1]*c(theta_2)*c(theta_1), l[1]*c(theta_2)*c(theta_1), l[0] + l[2]*s(theta_2) )

    pose_3 = (
                 ( l[1]*c(theta_2) + l[2]*c(theta_2 + theta_3) )*c(theta_1), \
                 ( l[1]*c(theta_2) + l[2]*c(theta_2 + theta_3))*s(theta_1), \
                 ( l[0] + l[1]*s(theta_1) + l[2]*s(theta_2+theta_3))
             )


    return ( pose_1, pose_2, pose_3  )

def ik(robot, pose):
    """

    :param x: x position of the EE
    :param y: y position of the EE
    :param z: z position of the EE
    :return: list of the joint angles
    """
    I, m, l, r = robot.uppack()
    x = pose[0]
    y = pose[1]
    z = pose[2]

    theta_1 = math.atan2(y,z)
    theta_3 = -math.acos( (x*x + y*y + (z- l[0])**2 -l[1]*l[1] - l[2]*[2])/ ( 2*l[1]*[2] )   )
    theta_2 = math.atan2( z- l[0] , math.sqrt(x*x, y*y) ) - math.atan2( l[2]*s(theta_3), l[1] + l[2]*c(theta_3) )

    return (theta_1, theta_2, theta_3)


def get_torque(robot):
    """

    :param robot:
    :return:
    """
    M = make_mass_matrix( robot )
    C = make_coriolis_matrix(robot)
    G = make_gravity_matrix(robot)
    q = np.asarray(robot.q).reshap(3,1)
    qd = np.asarray(robot.qd).reshap(3,1)
    qdd = np.asarray(robot.qdd).reshap(3,1)
    load = np.asarray(robot.tau).reshap(3,1)

    return M*qdd + C*qd + G





