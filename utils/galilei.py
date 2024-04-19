import math

import numpy as np


def apply(state, dt):
    borot = state.borot()
    position = borot.position()
    v_l, v_r = borot.speed()
    theta = borot.theta()
    radius = borot.radius()

    return motion_of_robot_rotation(v_l, v_r, radius, theta, position, dt)


# Calculate Omega: the rate of rotation
def rate_of_rotation(v_l, v_r, radius):
    l = get_diameter(radius)
    return (v_r - v_l) / l


def right_velocity(omega, R, radius):
    l = get_diameter(radius)
    return omega * (R + (l / 2))


def left_velocity(omega, R, radius):
    l = get_diameter(radius)
    return omega * (R - (l / 2))


def icc(R, theta, position):
    dx = -R * math.sin(theta)
    dy = R * math.cos(theta)

    return position[0] + dx, position[1] + dy


# Calculate R: signed distance from the ICC to the midpoint between the
# wheels
def signed_distance_from_icc_to_wheel(v_l, v_r, radius):
    return radius * ((v_l + v_r) / (v_r - v_l))


def get_diameter(radius):
    return 2 * radius


def motion_of_robot_rotation(v_l, v_r, radius, theta, position, dt):
    l = get_diameter(radius)

    if v_l == v_r:
        dx = v_l * math.cos(theta) * dt
        dy = v_l * math.sin(theta) * dt
        new_position = (position[0] + dx, position[1] + dy)
        new_theta = theta
    elif v_l == -v_r:
        omega = (v_r - v_l) / l
        new_position = position
        new_theta = theta + omega * dt
    else:
        R = signed_distance_from_icc_to_wheel(v_l, v_r, radius)
        omega = rate_of_rotation(v_l, v_r, radius)
        icc_position = icc(R, theta, position)

        rotation_by_wdt_about_z_axis_matrix = np.array([
            [math.cos(omega * dt), -math.sin(omega * dt), 0],
            [math.sin(omega * dt), math.cos(omega * dt), 0],
            [0, 0, 1]
        ])

        translate_icc_to_origin_matrix = np.array([
            position[0] - icc_position[0],
            position[1] - icc_position[1],
            theta
        ])

        translate_icc_to_origin_location_matrix = np.array([
            icc_position[0],
            icc_position[1],
            omega * dt
        ])

        x_prime, y_prime, theta_prime = (rotation_by_wdt_about_z_axis_matrix.dot(translate_icc_to_origin_matrix)
                                         + translate_icc_to_origin_location_matrix)
        new_position = (x_prime, y_prime)
        new_theta = theta_prime

    return new_position[0], new_position[1], new_theta
