import time
import Constants
import datetime
from dataclasses import dataclass

checkout_lines_time = []


class checkout_system:
    timestamp = 0


def get_checkout_lines():
    count_checkout_lines = int(input('Total checkout lines :'))
    if Constants.MAX_CHECKOUT_LINES < count_checkout_lines <= 0:
        return Constants.ERROR
    return count_checkout_lines


def get_current_time():
    time_in_seconds = (time.localtime().tm_hour * 60 * 60) + (time.localtime().tm_min * 60) + (
        time.localtime().tm_sec)
    print(time.localtime().tm_hour, ':', time.localtime().tm_min, ':', time.localtime().tm_sec)
    return time_in_seconds


def get_cart_size():
    cart_size = int(input('Enter cart size :'))
    if cart_size == Constants.FULL_ITEM_CART:
        return Constants.FULL_ITEM_CART
    elif cart_size == Constants.MEDIUM_ITEM_CART:
        return Constants.MEDIUM_ITEM_CART
    elif cart_size == Constants.LOW_ITEM_CART:
        return Constants.LOW_ITEM_CART
    else:
        return Constants.ERROR


def initialize_time_array(checkout_lines_count):
    checkout_system.timestamp = get_current_time()
    for i in range(checkout_lines_count):
        checkout_lines_time.append(0)
    return


def minimum_checkout_line(checkout_line_count):
    minimum_capacity = Constants.MAX_CHECKOUT_LINE_CAPACITY
    checkout_line_index = Constants.UNDER_INDEX
    for i in range(checkout_line_count):
        if minimum_capacity > checkout_lines_time[i]:
            minimum_capacity = checkout_lines_time[i]
            checkout_line_index = i
    return checkout_line_index


def allocate_checkout_line(checkout_line_count, cart_size):
    current_time = get_current_time()
    time_diff = current_time - checkout_system.timestamp
    for i in range(checkout_line_count):
        if checkout_lines_time[i] != 0:
            checkout_lines_time[i] -= time_diff
        else:
            checkout_lines_time[i] = 0
    checkout_system.timestamp = current_time
    minimum_line_number = minimum_checkout_line(checkout_line_count)
    if minimum_line_number == -1:
        return Constants.ERROR
    if cart_size == Constants.FULL_ITEM_CART:
        checkout_lines_time[minimum_line_number] += Constants.TIME_NEEDED_FOR_FULL_CART
    elif cart_size == Constants.MEDIUM_ITEM_CART:
        checkout_lines_time[minimum_line_number] += Constants.TIME_NEEDED_FOR_MEDIUM_CART
    elif cart_size == Constants.LOW_ITEM_CART:
        checkout_lines_time[minimum_line_number] += Constants.TIME_NEEDED_FOR_LOW_CART
    return minimum_line_number


def print_checkout_lines(checkout_line_count):
    for i in range(checkout_line_count):
        print(checkout_lines_time[i])


def queue(cart_size):
    checkout_lines_count = Constants.CHECKOUT_LINES
    initialize_time_array(checkout_lines_count)
    if cart_size != -1:
        checkout_line_number = allocate_checkout_line(checkout_lines_count, cart_size)
        #print('Go to line :', checkout_line_number + 1)
        #print_checkout_lines(checkout_lines_count)
        return checkout_line_number


cart_size = 0
queue(cart_size)
