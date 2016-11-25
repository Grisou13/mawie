from multiprocessing import Pool,Process,Queue, Manager, TimeoutError ,JoinableQueue

from app.models.File import File
import os


class Updator():
    def __init__(self):
        self.pool = Pool(processes=2)
        self.numProcess = 2
        self.updateQueueFile()
        self.pool.map(self.task,self.queueFiles)


    def updateQueueFile(self):
        self.queueFiles = JoinableQueue()
        for file in File.query(include_deleted=True):
            self.queueFiles.put(file)

        for i in range(self.numProcess):
            self.queueFiles.put(None)

    def task(self):
        while True:
            file = self.queueFiles.get()
            if not os.path.isfile(file.path):
                print(file.path," n'existe pas")
            else:
                print(file.path," :File exists")
if __name__=='__main__':
    app = Updator()


# class Updator():
#     def __init__(self):
#         self.updateQueue()
#         self.pool()
#     def updateQueue(self):
#         self.manager = Manager()
#         self.queue = Queue()
#         for file in File.query(include_deleted=True):
#             self.queue.put(file)
#
#     def pool(self):
#         queue = Queue()
#         test = Process(self.checkFileExist, args=(queue,))
#         test.start()
#
#     def checkFileExist(self,queue):
#         i = queue.get()
#         print(i)
#
# if __name__ == '__main__':
#     test = Updator()
#
# sentinel = -1
# def test(q):
#     while True:
#         data = q.get()
#         print(data.path)
#         if data is sentinel:
#             break
#
# if __name__=='__main__':
#     q = Queue()
#     for i in File.query():
#         q.put(i)
#
#     with Pool(processes=4) as pool:
#         pool.map(test, ])
#