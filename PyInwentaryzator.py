#!/usr/bin/env python
from getch import getch
from camera import CameraWrapper
from time import time, sleep
import io


PLACES = u'places'
INVENTORY = u'inventory'
TAGS = u'tags'
DATA_FOLDER = u'./data'
CAMERA =1 
INVENTORY_ID_OFFSET = 0

def db_path(name):
    return u"{}/{}.csv".format(DATA_FOLDER, name)


def open_db(filename):
    path = db_path(filename)
    try:
        return io.open(path, u'a', encoding=u"utf-8")
    except Exception:
        io.open(path, u'w', encoding=u"utf-8").close()
    return io.open(path, u'a', encoding=u"utf-8")


def read_db(filename):
    path = db_path(filename)
    try:
        fh = io.open(path, u'r', encoding=u"utf-8")
        table = map(lambda l: l.split(u','), fh.readlines())
        table = map(lambda row: map(lambda element: element.strip()[1:-1], row), table)
        return filter(lambda row: not(len(row)==0 and len(row[0])==0), table)
    except Exception:
        io.open(path, u'w', encoding=u"utf-8").close()
    return []


def read_list(filename):
    list = read_db(filename)
    if len(list) == 0:
        list_file = open_db(filename)
        list_file.write(u'"None"\n')
        list = [[u"None"]]
    return map(lambda row:row[0], list)

def read_string(prompt):
    return unicode(raw_input(prompt), encoding=u'utf8')

places = read_list(PLACES)

inventory = read_db(INVENTORY)
if len(inventory) == 0:
    last_id = INVENTORY_ID_OFFSET
else:
    last_id = int(inventory[-1][0], 16)

with open_db(INVENTORY) as inventory_table, \
        open_db(PLACES) as places_table, \
        CameraWrapper(CAMERA) as camera:
    sleep(1)
    print(u"\n" * 120)
    while True:
        print(u"\n" * 5)
        print(u"Press [Enter] to take a photo, [p] to add a place[q] to quit")
        user_input = getch()
        #print("{} ; {}".format(user_input, ord(user_input)))
        if user_input in (chr(10), chr(13)):
            item_id = last_id + 1
            print(u"Provide data for item id: '" + format(item_id, '04x') + "'")
            picture = u"{}/{}_0.jpg".format(DATA_FOLDER, format(item_id, u'04x').encode(u'utf8')).encode(u'utf8')
            camera.take_picture(picture)
            name = read_string(u"Item name:")
            print(u"Places:")
            print(u'\n'.join([u"{}: {}".format(offset, places[offset]) for offset in range(len(places))]))
            place = read_string(u"choose storage place:")
            print(u"")
            tags = read_string(u"List of comma-separated tags:")
            try:
                line = u'"' + (u'","'.join([
                    format(item_id, u'04x').encode(u'utf8'),
                    name,
                    places[int(place)],
                    tags,
                    picture])) + u'"\n'
                inventory_table.write(line)
            except Exception as e:
                
                print(e)

            print(u"")
            last_id = item_id
        elif user_input == 'p':
            place = read_string(u"Place name:")
            places.append(place)
            places_table.writelines([u'"{}"\n'.format(place)])
            print(u"")
        elif user_input == 'q':
            exit(0)
        else:
            print(u"Something went wrong, try again.")
            
        inventory_table.flush()
        places_table.flush()
