import threading
import time

def print_numbers(x):
    for i in range(5):
        time.sleep(1)
        print(f"Thread {x}: {i}")

# 创建两个线程
thread1 = threading.Thread(target=print_numbers, args=('A'))
thread2 = threading.Thread(target=print_numbers, args=('B'))

# 启动线程
thread1.start()
thread2.start()

# 等待两个线程完成
thread1.join()
thread2.join()

print("Both threads have finished.")