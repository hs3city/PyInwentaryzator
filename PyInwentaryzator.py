#!/usr/bin/env python
from getch import getch
from camera import CameraWrapper
from time import time, sleep

PLACES = 'places'
INVENTORY = 'inventory'
TAGS = 'tags'
DATA_FOLDER = './data'


def db_path(name):
    return "{}/{}.csv".format(DATA_FOLDER, name)


def open_db(filename):
    path = db_path(filename)
    try:
        return open(path, 'a')
    except Exception:
        open(path, 'w').close()
    return open(path, 'a')


def read_db(filename):
    path = db_path(filename)
    try:
        fh = open(path, 'r')
        return map(lambda l: l.split(','), fh.readlines())
    except Exception:
        open(path, 'w').close()
    return []


def read_list(filename):
    list = read_db(filename)
    list = map(lambda row: row[0].strip()[1:-1], list)
    if len(list) == 0:
        list = ["None"]
    return list


places = read_list(PLACES)

with open_db(INVENTORY) as inventory_table, \
        open_db(PLACES) as places_table, \
        CameraWrapper(0) as camera:
    sleep(1)
    print("\n" * 120)
    while True:
        print("Press [Enter] to take a photo, [p] to add a place[q] to quit")
        user_input = getch()
        #print("{} ; {}".format(user_input, ord(user_input)))
        if user_input in (chr(10), chr(13)):
            picture = "{}/{}.jpg".format(DATA_FOLDER, time())
            camera.take_picture(picture)
            name = raw_input("Item name:")
            print("Places:")
            print('\n'.join(["{}: {}".format(offset, places[offset]) for offset in range(len(places))]))
            place = raw_input("choose storage place:")
            print("")
            tags = raw_input("List of comma-separated tags:")
            line = '"' + ('","'.join([name, places[int(place)], tags, picture])) + '"\n'
            inventory_table.write(line)
            print("")
        elif user_input == 'p':
            place = raw_input("Place name:")
            places.append(place)
            places_table.writelines(['"{}"\n'.format(place)])
            print("")
        elif user_input == 'q':
            exit(0)
        else:
            print("Something went wrong, try again.")
            
        inventory_table.flush()
        places_table.flush()
