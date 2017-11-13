"""
Implementation of the First-Come, First-Served scheduler
"""
from simso.core import Scheduler
from simso.schedulers import scheduler


@scheduler("simso.schedulers.FCFS")
class FCFS(Scheduler):
    """First-Come, First-Served scheduler"""

    def init(self):
        self.ready_list = []

    def on_activate(self, job):
        self.ready_list.append(job)
        job.cpu.resched()

    def on_terminated(self, job):
        if job in self.ready_list:
            self.ready_list.remove(job)
        job.cpu.resched()

    def schedule(self, cpu):
        if self.ready_list:
            job = self.ready_list[0]
            if not cpu.running:
                self.ready_list.remove(job)
                return (job, cpu)
        else:
            return None
