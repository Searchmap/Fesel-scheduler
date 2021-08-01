import numpy as np
import pickle

from datetime import *

import json

import cv2

import zmq
import cv2

from os import path
from glob import glob

from collections import Counter

import operator as op
import functools as ft, itertools as it

from os.path import join

from db_config.connection import connect, deconnect

def is_valid(date1, date2):
    return (date1.date() <= date.today() and date2.date() >= date.today())

def is_active(weekdays):
    return (str(date.today().weekday()) in weekdays)

def process_contracts():
    ongoing_contracts = []
    
    db = connect()
    cursor = db.cursor()

    sql = 'SELECT * FROM Contract'
    cursor.execute(sql)

    contracts_list = cursor.fetchall()
    for contract in contracts_list:
        if is_valid(contract[1], contract[2]) and is_active(contract[3].split(',')):
            ongoing_contracts.append(contract[0])

    deconnect(db, cursor)

    return ongoing_contracts

def process_media_table():
    media_files = []
    ongoing_contracts = process_contracts()

    db = connect()
    cursor = db.cursor()

    sql = 'SELECT * FROM Media;'
    cursor.execute(sql)

    list_media = cursor.fetchall()
    for media in list_media:
        if media[5] in ongoing_contracts:
            temp_dict = {}
            name, gender, age, skin = media[1], media[2], media[3], media[4]
            temp_dict['name'] = name
            temp_dict['vector'] = vectorize(merge_media_chars(gender, age, skin))
            media_files.append(temp_dict)

    deconnect(db, cursor)

    return media_files

def compute_score(public_vect, media_vect):
    return np.sum(public_vect * media_vect)

def update_media_list(public_vect, media_files):
    for mf in media_files:
        mf['score'] = compute_score(public_vect, mf['vector'])
    media_files.sort(key=op.itemgetter('score'), reverse=True)

def diaporama(screen_name, filenames, media_path, shared_queue):
    total_v = len(filenames)
    if total_v == 0: exit(1)
    v_index = 0
    readers = [ (cv2.VideoCapture(join(media_path, fname)), fname) for fname in filenames ]
    lenghts = [ int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) for cap, _ in readers ]
    cursors = [0] * len(lenghts)

    keep_showing = True
    while keep_showing:
        if not shared_queue.empty():
            _, filenames = shared_queue.get()
            v_index = 0
            file2index = dict([ (f, i) for i, f in enumerate(filenames)])
            readers = sorted(readers, key=lambda obj: file2index[obj[1]])
            lenghts = [ int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) for cap, _ in readers ]
            cursors = [0] * len(lenghts)
            for cap, _ in readers:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        key_code = cv2.waitKey(25) & 0xFF
        keep_showing = key_code != 27
        if key_code == 32:
            v_index = (v_index + 1) % total_v
        else:
            status, bgr_frame = readers[v_index][0].read()
            cursors[v_index] = cursors[v_index] + 1
            if status:
                bgr_frame = cv2.resize(bgr_frame, (640, 480))
                if cursors[v_index] == lenghts[v_index]:
                    cursors[v_index] = 0
                    readers[v_index][0].set(cv2.CAP_PROP_POS_FRAMES, 0)
                    v_index = (v_index + 1) % total_v
                cv2.imshow(screen_name, bgr_frame)
            else:
                v_index = (v_index + 1) % total_v

    for cap, _ in readers: cap.release()

    cv2.destroyAllWindows()

def create_screen(name, W, H, position=None):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, W, H)
    if position is not None:
        cv2.moveWindow(name, *position)

def values2proportions(dico):
    s = sum(dico.values())
    for key, value in dico.items():
        dico[key] = round((value/s), 2)
    return dico

def merge_media_chars(gender, age, skin):
    merged_chars = {}
    
    l1, l2, l3 = [], [], []
    if gender != '': l1 = gender.split(',')
    if age != '': l2 = age.split(',')
    if skin != '': l2 = skin.split(',')
    l = l1 + l2 + l3

    for elt in l: merged_chars[elt] = 1

    return merged_chars

def merge_metrics(metrics):
    list_metrics = [values2proportions(value) for value in metrics.values()]
    return dict(ft.reduce(op.add, map(Counter, list_metrics)))

def vectorize(merged_metrics):
    dico = {
        'M': 0, 'F': 0,
        'child': 0, 'young': 0, 'young_adult': 0, 'adult': 0, 'middle_aged': 0, 'senior': 0,
        'arab': 0, 'asian': 0, 'black': 0, 'indian': 0, 'white': 0,
    }

    dico.update(merged_metrics)

    return np.array([value for value in dico.values()])

class ZMQServer:
    def __init__(self, pusher_port, source_data):
        self.pusher_port = pusher_port 
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PUSH)
        self.data = pickle.load(open(source_data, 'rb'))
        self.nb_items = len(self.data)
        self.cursor = 0 
    
    def start(self):
        self.socket.bind(f'tcp://*:{self.pusher_port}')

    def send(self):
        if not self.empty():
            response = self.data[self.cursor]
            self.cursor += 1
            self.socket.send_pyobj(response) 
        else:
            raise ValueError('No item ...!')

    def empty(self):
        return self.cursor == self.nb_items
    
    def close(self):
        self.socket.close()
        self.ctx.term()

class ZMQWorker:
    def __init__(self, pusher_port):
        self.pusher_port = pusher_port 
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PULL)
    
    def connect(self):
        self.socket.connect(f'tcp://localhost:{self.pusher_port}')
    
    def receive(self):
        data = self.socket.recv_pyobj(flags=zmq.NOBLOCK)
        return data
    
    def close(self):
        self.socket.close()
        self.ctx.term()
    
    def process_data(self, metrics):
        acc = []
        for key, val in metrics.items():
            cnt = Counter()
            iterable = list(val.values())
            cnt.update( iterable )
            acc.append((key, dict(cnt)))
        return dict(acc)

if __name__ == '__main__':
    print('... [ Testing ] ...')
    public_vect = np.array([0.4, 0.6, 0., 0., 0.8, 0.1, 0.1, 0., 0., 1., 0., 0., 0.])
    
    media_files = process_media_table()

    l = ['1','2','3','5']
    print(is_active(l))
    # print(media_files)


    # print([ mf['name'] for mf in media_files ])
    # print([ mf['name'] for mf in media_files ])

    # update_media_list(public_vect, media_files)