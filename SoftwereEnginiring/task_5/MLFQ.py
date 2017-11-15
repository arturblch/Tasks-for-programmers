"""
Implementation of the Multilevel Feedback Queue scheduler
"""
from simso.core import Scheduler, Timer
from simso.schedulers import scheduler

QUANTUM = 8
BOOST_DELAY = 200
NUM_QUEUE = 4

@scheduler(
    "simso.schedulers.MLFQ",
    required_task_fields=[{
        'name': 'priority',
        'type': 'int',
        'default': '0'
    }])
class MLFQ(Scheduler):
    """Multilevel Feedback Queue scheduler"""

    def init(self):

        self.ready_lists = [[] for _ in range(NUM_QUEUE)]
        self.job_timer = None
        self.boost_timer = Timer(
            self.sim,
            MLFQ.boost_event, (self, self.processors[0]),
            BOOST_DELAY,
            one_shot=False,
            cpu=self.processors[0],
            in_ms=True)
        self.interupt = False

    def on_activate(self, job):
        self.ready_lists[0].append(job)
        job.cpu.resched()

    def on_terminated(self, job):
        prior = job.data["priority"]
        if job in self.ready_lists[prior]:
            self.ready_lists[prior].remove(job)
        if prior < NUM_QUEUE - 1:
            self.timer.stop()
        job.cpu.resched()

    def boost_event(self, cpu):
        for q in range(1, NUM_QUEUE):
            for j in self.ready_lists[q]:
                j.data["priority"] = 0
            self.ready_lists[0].extend(self.ready_lists[q])
        cpu.running.data["priority"] = 0
        cpu.resched()

    def end_event(self, cpu):
        self.interupt = True
        self.timer.stop()
        prior = cpu.running.data["priority"]
        cpu.running.data["priority"] = prior + 1 if prior < NUM_QUEUE - 1 else NUM_QUEUE - 1
        cpu.resched()

    def getTimer(self, prior):
        if prior < NUM_QUEUE-1:
            return Timer(
                self.sim,
                MLFQ.boost_event, (self, self.processors[0]),
                QUANTUM*(2**prior),
                cpu=self.processors[0],
                in_ms=True)
        else:
            None

    def schedule(self, cpu):
        if self.interupt or any(self.ready_lists):
            job = None
            if any(self.ready_lists):
                for r in range(NUM_QUEUE):
                    if self.ready_lists[r]:
                        job = self.ready_lists[r][0]
                        break
            else:
                job = cpu.running

            prior = job.data["priority"]

            if (not cpu.running or
                    prior < cpu.running.data["priority"] or
                    self.interupt):
                self.timer = self.getTimer(prior)
                self.timer.start()
                if job in self.ready_lists[prior]:
                    self.ready_lists[prior].remove(job)
                if cpu.running:
                    self.ready_lists[cpu.running.data["priority"]].append(
                        cpu.running)
                return (job, cpu)
        else:
            return None
