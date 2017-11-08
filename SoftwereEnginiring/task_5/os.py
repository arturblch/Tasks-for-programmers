from process import Process_Control_Block as PCB

class OS:
    def __init__(self):
        self.max_PID = 20
        self.process_list = dict()

    def create_process(self, name, prior, cpu_burst):
        process = PCB(name, prior, cpu_burst)
        for pid in range(self.max_PID):
            if pid not in self.process_list.keys():
                self.process_list.update((pid , process))

    def Tick(self):
        pass



Linux = OS()

Linux.create_process('main', 0, 10000)