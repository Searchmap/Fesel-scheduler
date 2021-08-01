import numpy as np

import pickle
import click

from time import sleep

import cv2
import zmq

from collections import Counter

import multiprocessing as mp
from libraries.strategies import (
                                    ZMQServer,
                                    ZMQWorker,
                                    create_screen,
                                    vectorize,
                                    diaporama,
                                    update_media_list,
                                    process_media_table,
                                    merge_metrics,
)

def server_loop(pusher_port, source_data, server_status):
    try:
        server = ZMQServer(pusher_port, source_data)
        server.start() 
        server_status.set()
        keep_sending = True 
        while keep_sending and not server.empty():
            server.send()
            sleep(0.5) 
    except KeyboardInterrupt as e:
        pass
    finally:
        server_status.clear() 
        sleep(5) 
        server.close()

def worker_loop(pusher_port, pid, server_status, shared_queue):
    try:
        keep_processing = True 
        print('%03d => wait for the server to be ready' % pid)
        server_status.wait()
        worker = ZMQWorker(pusher_port) 
        worker.connect() 
        print('%03d => connect to server' % pid)
        while keep_processing and server_status.is_set():
            try:
                data_from_server = worker.receive()

                print('worker %03d => receive : %d metrics' % (pid, len(data_from_server)))
                print('------------------------------------')
                metrics = data_from_server.to_dict()
                response = worker.process_data(metrics)
                print(response)
                merged_metrics = merge_metrics(response)
                public_vect = vectorize(merged_metrics)
                # print('associated vector =>', public_vect)
                # print('\n')

                media_files = process_media_table()
                update_media_list(public_vect, media_files)

                filenames = [ mf['name'] for mf in media_files ]

                print('\n')
                print(filenames)
                print('\n')

                shared_queue.put((pid, filenames))

                sleep(15)

            except zmq.ZMQError as e: 
                pass 
    except KeyboardInterrupt as e:
        pass 
    finally:
        print('%03d terminate ...!' % pid)
        worker.close()


def sink_loop(media_path, shared_queue):
    W, H = 640, 480
    s00 = '000'
    
    pid, filenames = shared_queue.get()

    create_screen(s00, W, H, (100, 100))
    diaporama(s00, filenames, media_path, shared_queue)

@click.command()
@click.option('--media_path', help='path to media files')
@click.option('--pusher_port', help='port of server', default=8100)
@click.option('--source_data', help='path to source data')
@click.option('--nb_workers', help='number of workers', default=4, type=int)
def main_loop(media_path, pusher_port, source_data, nb_workers):
    try:
        shared_queue = mp.Queue()
        server_status = mp.Event()
        server_process = mp.Process(target=server_loop, args=[pusher_port, source_data, server_status])
        workers = []
        for idx in range(nb_workers):
            wp = mp.Process(
                target=worker_loop, 
                args=[pusher_port, idx, server_status, shared_queue]
            )
            workers.append(wp)
            workers[-1].start()

        server_process.start()
        sink_process = mp.Process(target=sink_loop, args=[media_path, shared_queue])
        sink_process.start()
    except Exception: 
        pass 

if __name__ == '__main__':
    print(' ... [processing] ... ')
    try:
        main_loop()
    except Exception as e:
        pass