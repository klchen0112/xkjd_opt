from multiprocessing import Process, Queue

def write_to_queue(queue, data):
    for item in data:
        queue.put(item)

def read_from_queue(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(item)

if __name__ == '__main__':
    # 创建队列并启动读取任务
    q = Queue()
    read_proc = Process(target=read_from_queue, args=(q,))
    read_proc.start()

    # 启动写入任务
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]
    write_procs = []
    for i in range(5):
        write_proc = Process(target=write_to_queue, args=(q, data[i]))
        write_procs.append(write_proc)
        write_proc.start()

    # 等待所有写入任务完成
    for write_proc in write_procs:
        write_proc.join()

    # 发送结束信号给读取任务，并等待读取任务完成
    q.put(None)
    read_proc.join()
