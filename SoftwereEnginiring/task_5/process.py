# Этот клас будет отвечать за создание процессов


class Process_Control_Block:
    def create_process(self, name, prior, cpu_burst):
        self.status = "Create"
        self.pc = 0   # Program counter
        self.reg = {  # Registers
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "E": 0,
            "H": 0,
            "L": 0
        }

        self.prior = prior   # Priority
        self.address = None  # Memory

        self.cpu_burst = cpu_burst

    def finish_process(self):
        self.life_time = 3
        self.status = "Done"

    def prepare_process(self):
        self.status = "Ready"

    def pause_process(self):
        self.status = "Ready"

    def run_process(self):
        self.status = "Run"
