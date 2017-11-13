"""
Implementation of the Round Robin scheduler
"""
from simso.core import Scheduler, Timer
from simso.schedulers import scheduler


@scheduler("simso.schedulers.RR")
class RR(Scheduler):
    """Round Robin scheduler"""

    def init(self):
        self.ready_list = []
        self.delay = 2
        self.timer = Timer(self.sim, RR.end_event,
                           (self, self.processors[0]), self.delay,
                           cpu=self.processors[0], in_ms=True)
        self.interupt = False

    def on_activate(self, job):
        self.ready_list.append(job)
        job.cpu.resched()

    def on_terminated(self, job):
        if job in self.ready_list:
            self.ready_list.remove(job)
        self.timer.stop()
        job.cpu.resched()

    def end_event(self, cpu):
        self.interupt = True
        self.timer.stop()
        cpu.resched()

    def schedule(self, cpu):
        if self.ready_list:
            job = self.ready_list[0]
            if not cpu.running or self.interupt:
                self.interupt = False
                self.timer.start()
                self.ready_list.remove(job)
                if cpu.running:
                    self.ready_list.append(cpu.running)
                return (job, cpu)
        else:
            return None
