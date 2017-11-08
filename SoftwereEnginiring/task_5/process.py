# Этот клас будет отвечать за создание процессов

class Process_Control_Block:
    def __init__(self, name, prior, cpu_burst):
        self.status = "Create"
        self.pc = 0             # Program counter
        self.prior = prior      # Priority
        self.cpu_burst = cpu_burst

    def finish_process(self):
        self.life_time = 64
        self.status = "Done"

    def prepare_process(self, address):
        self.address = address
        self.status = "Ready"

    def pause_process(self):
        self.status = "Ready"

    def run_process(self):
        self.status = "Run"
