"""
Implementation of the Multilevel Feedback Queue scheduler
"""
from simso.core import Scheduler, Timer
from simso.schedulers import scheduler

@scheduler(
    "simso.schedulers.MLFQ")
class MLFQ(Scheduler):
    """Multilevel Feedback Queue scheduler"""
    QUANTUM = 8
    BOOST_DELAY = 200
    NUM_QUEUE = 4

    def init(self):

        self.ready_lists = [[] for _ in range(self.NUM_QUEUE)]
        self.job_timer = None
        self.timers = [self.create_timer(i) for i in range(self.NUM_QUEUE - 1)]
        self.prior_table = {}
        self.boost_timer = Timer(
            self.sim,
            MLFQ.boost_event, (self, self.processors[0]),
            self.BOOST_DELAY,
            one_shot=False,
            cpu=self.processors[0],
            in_ms=True)
        self.boost_timer.start()
        self.interupt = False

    def on_activate(self, job):
        self.ready_lists[0].append(job)
        self.prior_table.update({job: 0})
        job.cpu.resched()

    def on_terminated(self, job):
        prior = self.prior_table[job]
        if job in self.ready_lists[prior]:
            self.ready_lists[prior].remove(job)
        if self.job_timer:
            self.job_timer.stop()
        self.prior_table.pop(job, None)
        job.cpu.resched()

    def boost_event(self, cpu):
        for q in range(1, self.NUM_QUEUE):
            for j in self.ready_lists[q]:
                self.prior_table[j] = 0
            self.ready_lists[0].extend(self.ready_lists[q]) # Add all in first queue
            del self.ready_lists[q][:]                      # Cleare all from old queue
        if cpu.running:
            self.prior_table[cpu.running] = 0
            self.interupt = True
            cpu.resched()

    def end_event(self, cpu):
        if cpu.running:
            self.interupt = True
            if self.job_timer:
                self.job_timer.stop()
            prior = self.prior_table[cpu.running]
            self.prior_table[cpu.running] = prior + 1 if prior < self.NUM_QUEUE - 1 else self.NUM_QUEUE - 1
            cpu.resched()

    def create_timer(self, i):
        return Timer(
                self.sim,
                MLFQ.end_event, (self, self.processors[0]),
                self.QUANTUM*(2**i),
                cpu=self.processors[0],
                in_ms=True)

    def set_timer(self, prior):
        if self.job_timer:
            self.job_timer.stop()

        if prior < self.NUM_QUEUE-1:
            self.job_timer = self.timers[prior]
            self.job_timer.start()


    def schedule(self, cpu):
        if any(self.ready_lists):
            for r in range(self.NUM_QUEUE):
                if self.ready_lists[r]:
                    job = self.ready_lists[r][0]
                    break

            j_prior = self.prior_table[job]

            if (not cpu.running or
                    j_prior < self.prior_table[cpu.running] or
                    self.interupt and j_prior <= self.prior_table[cpu.running]):
                self.set_timer(j_prior)
                if self.interupt:
                    self.interupt = False
                if job in self.ready_lists[j_prior]:
                    self.ready_lists[j_prior].remove(job)
                if cpu.running:
                    self.ready_lists[self.prior_table[cpu.running]].append(
                        cpu.running)
                return (job, cpu)

        elif self.interupt:
                self.interupt = False
                self.set_timer(self.prior_table[cpu.running])
                return None
        else:
            return None
