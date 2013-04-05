from apscheduler.scheduler import Scheduler
import logging

from wander.app import app
logging.basicConfig()

class WanderJob(object):
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.name = self.__class__.__name__

    def log(self, msg):
        if self.verbose:
            print("%s: %s" %(self.name, msg))

    def start(self):
        self.log("++Starting++")
        self._run()
        self.log("--Finished--")

    def _run():
        pass

sched = Scheduler()


def job_cartosync():
    job = CartoSyncJob(verbose = True)
    job.start()

@sched.interval_schedule(seconds=5)
def job_spotfetch():
    json = app.config['SPOT_DATA']
    archive = "sqlite:///:memory:"
    job = SpotFetchJob(json_file = json, archive_db = archive, verbose = True)
    job.start()


def start():
    sched.configure()
    sched.start()


from wander.worker.spotfetch import SpotFetchJob
from wander.worker.cartosync import CartoSyncJob


