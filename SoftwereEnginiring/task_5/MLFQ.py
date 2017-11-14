"""
Implementation of the Multilevel Feedback Queue scheduler
"""
from simso.core import Scheduler, Timer
from simso.schedulers import scheduler

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
    """Round Robin scheduler"""

    def init(self):

        self.ready_lists = [[] for _ in range(NUM_QUEUE)]
        self.timer = None
        self.boost_timer = Timer(
            self.sim,
            MLFQ.boost_event, (self, self.processors[0]),
            BOOST_DELAY,
            one_shot=False,
            cpu=self.processors[0],
            in_ms=True)
        self.interupt = False

    def boost_event(self, cpu):
        for r in range(len(self.ready_lists) - 1, 0, -1):
            self.ready_lists[r - 1].extend(self.ready_lists[r])
        
        for j in self.ready_lists[0]:
            j.data["priority"] = 0
        cpu.resched()

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

    def end_event(self, cpu):
        self.interupt = True
        self.timer.stop()
        cpu.resched()

    def schedule(self, cpu):
        if self.ready_lists or self.interupt: 
            if self.interupt:
                self.interupt = False
                prior = cpu.running.data["priority"]
                cpu.running.data["priority"] = prior + 1 if prior < len(
                    self.ready_lists) else NUM_QUEUE - 1 
                self.ready_list[cpu.running.data["priority"]].append(
                                cpu.running)
                self.timer = self.getTimer(cpu.running.data["priority"])
                self.timer.start()

            job = None
            for r in range(len(self.ready_lists)):
                if self.ready_lists[r]:
                    job = self.ready_lists[r][0]
                    break

            if (not cpu.running or
                    job.data["priority"] < cpu.running.data["priority"]):

                self.timer = self.getTimer(job.data["priority"])
                self.timer.start()
                self.ready_lists[r].remove(job)
                if cpu.running:
                    self.ready_list[cpu.running.data["priority"]].append(
                        cpu.running)
                return (job, cpu)

        else:
            return None
