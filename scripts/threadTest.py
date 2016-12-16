import threading
from queue import Queue

import time


class BG(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.q = queue
    def run(self):
        while not self.q.empty():
            obj = self.q.get(True,0)
            print("got object in thread ["+str(threading.current_thread())+"]")
            print(obj)
            print("##########")
            self.q.put("from thread ["+str(threading.current_thread())+"]")
            time.sleep(1)
if __name__ == '__main__':
    q = Queue(-1)
    q.put_nowait("1")
    q.put_nowait("2")
    t = BG(q)
    t2 = BG(q)
    q.put_nowait("3")
    t.start()
    q.put_nowait("4")
    t2.start()
    q.put_nowait("5")
    q.join()
    print(q.qsize())
    print("finished")