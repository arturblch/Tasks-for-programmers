"""
Implementation of the PriD scheduler as introduced by Goossens et al. in
Priority-Driven Scheduling of Periodic Task Systems on Multiprocessors.
"""
from simso.core import Scheduler, Timer
from math import ceil
from simso.schedulers import scheduler


@scheduler(
    "simso.schedulers.RR",
    required_task_fields=[{
        'name': 'priority',
        'type': 'int',
        'default': '0'
    }])
class RR(Scheduler):
    """Round Robin scheduler"""

    def init(self):
        self.timers = {}
        self.ready_list = []
        self.delay = 5
        self.interupt = False

    def on_activate(self, job):
        self.ready_list.append(job)
        if job.task not in self.tasks_list:
            self.tasks_list.append(job.task)
        job.cpu.resched()

    def on_terminated(self, job):
        if job in self.ready_list:
            self.ready_list.remove(job)
        if job  in self.timers:
            self.timers[job].stop()
            del self.timers[job]
        job.cpu.resched()

    def end_event(self, job):
        del self.timers[job]
        self.interupt = True
        self.processors[0].resched()

    def schedule(self, cpu):
        if self.ready_list or cpu.running:
            job = min(self.ready_list, key=lambda x: x.data["priority"])
            if cpu.running and self.interupt:
                    self.ready_list.remove(job)
                    self.ready_list.append(cpu.running)
                    return (job, cpu)

            if (cpu.running is None
                    or cpu.running.data["priority"] > job.data["priority"]):
                if job not in self.timers:
                    timer = Timer(self.sim, RR.end_event,
                                  (self, cpu.running), self.delay,
                                  cpu=cpu, in_ms=True)
                    timer.start()
                    self.timers[job] = timer
                self.ready_list.remove(job)
                if cpu.running:
                    self.ready_list.append(cpu.running)
                return (job, cpu)

        else:
            return None
