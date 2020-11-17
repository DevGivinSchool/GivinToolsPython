import multiprocessing
from multiprocessing import Pool, Queue
from os import getpid
import time
import argparse
import logging


class Executor:
    MAX_WORKERS = multiprocessing.cpu_count()

    def __init__(self, logger):
        """
        Initiates a queue, a pool and a temporary buffer, used only
        when the queue is full.
        """
        self.q = Queue()
        self.pool = Pool(processes=self.MAX_WORKERS, initializer=self.execute, )
        self.temp_buffer = []
        self.logger = logger

    def add_task(self, task):
        """
        If queue is full, put the message in a temporary buffer.
        If the queue is not full, adding the message to the queue.
        If the buffer is not empty and that the message queue is not full,
        putting back messages from the buffer to the queue.
        """
        self.logger.debug('add task')
        if self.q.full():
            self.logger.debug(f'task {task.uuid} append to buffer')
            self.temp_buffer.append(task)
        else:
            self.logger.debug(f'task {task.uuid} append to queue')
            self.q.put(task)
            if len(self.temp_buffer) > 0:
                self.logger.debug(f'task {task.uuid} putting back from the buffer to the queue')
                self.add_task(self.temp_buffer.pop())

    def parse_args(self, args):
        function_map = {'help': self.help,
                        'hello': self.hello}
        parser = argparse.ArgumentParser()

        parser.add_argument('command', choices=function_map.keys())

        args = parser.parse_args([args])

        func = function_map[args.command]
        func()

    def do_work(self, task):
        self.logger.debug('do_work')
        task.display_task()
        self.parse_args(task.subject)

    def execute(self):
        """
        Waits indefinitely for an item to be written in the queue.
        Finishes when the parents process terminates.
        """
        print("Process {0} started".format(getpid()))
        # print(type(self.logger))
        # print(self.logger)
        print(self.__dir__())
        self.logger.debug(f'Process {getpid()} started')
        while True:
            # If queue is not empty, pop the next element and do the work.
            # If queue is empty, wait indefinitely until an element get in the queue.
            task = self.q.get(block=True, timeout=None)
            print("{0} retrieved: {1}".format(getpid(), task))
            self.logger.debug("{0} retrieved: {1}".format(getpid(), task))
            # simulate some random length operations
            self.do_work(task)
            self.logger.debug(f'executer sleep 60 sec ...................')
            time.sleep(60)

    def help(self):
        self.logger.debug(f'function help')

    def hello(self):
        self.logger.debug(f'function hello')
