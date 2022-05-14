#!/usr/bin/env python
#  coding=utf-8
#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT license.

from threading import Thread
from queue import Queue
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'

app = Flask(__name__)
CORS(app)


rgi_queue = Queue(maxsize=0)
rgo_queue = Queue(maxsize=0)

global_counter = 0


@app.route('/generate', methods=['GET', 'POST'])
def generate_queue():
    global global_counter, rgi_queue, rgo_queue
    try:
        in_request = request.json
        print(in_request)
    except:
        return "invalid input: "
    global_counter += 1
    rgi_queue.put((global_counter, in_request))
    output = rgo_queue.get()
    rgo_queue.task_done()
    return jsonify(output)


def generate_for_queue(in_queue, out_queue):
    while True:
        _, in_request = in_queue.get()
        context = ' EOS '.join(in_request['msg'])
        knowledge = in_request['knowledge']
        response = generate(context, knowledge)

        res = {}
        res['response'] = response[0]
        out_queue.put(res)
        in_queue.task_done()


if __name__ == "__main__":

    from DialoGLM.server import *
    # replace the path with your trained checkpoint
    args.model_name_or_path = 't5-base'
    main()

    worker = Thread(target=generate_for_queue, args=(rgi_queue, rgo_queue,))
    worker.setDaemon(True)
    worker.start()
    app.run(port=8082)
