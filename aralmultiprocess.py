import threading
import time

class Process:
    def __init__(self):
        self.process_running = False
        self.thread = None

    def start(self, process_number):
        self.process_running = True
        self.thread = threading.Thread(target=self.run_process, args=(process_number,))
        self.thread.start()

    def stop(self):
        self.process_running = False
        if self.thread is not None:
            self.thread.join()

    def run_process(self, process_number):
        while self.process_running:
            print(f"Process {process_number} is running")
            time.sleep(1)

process1 = Process()
process2 = Process()

while True:

    button = input("Press 1 to run process 1, press 2 to run process 2, press q to quit: ")
    if button == "1":
        process2.stop()
        process1.start(1)
    elif button == "2":
        process1.stop()
        process2.start(2)
    elif button == "q":
        process1.stop()
        process2.stop()
        break