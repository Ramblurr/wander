from apscheduler.scheduler import Scheduler, logger as apslogger
from wander.app import app
import logging as log

log_file = 'worker.log'
log_handler= log.FileHandler(log_file)
apslogger.addHandler(log_handler)

class WanderJob(object):
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.name = self.__class__.__name__
        self.logger = log.getLogger(__name__)
        self.logger.addHandler(log_handler)
        self.logger.setLevel(log.DEBUG)
        #self.logger.basicConfig(filename='%s.log'%(self.name), level =log.DEBUG)

    def info(self, msg):
        self.logger.info("%s: %s" %(self.name, msg))

    def debug(self, msg):
        self.logger.debug("%s: %s" %(self.name, msg))

    def start(self):
        self.info("Running..")
        self._run()
        self.info("Finished")

    def _run():
        pass

sched = Scheduler()

@sched.interval_schedule(seconds=5)
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

jobs = [
    { 'name': 'job_cartosync', 'func': job_cartosync, 'interval': { 'seconds': 5 }},
    { 'name': 'job_spotfetch', 'func': job_spotfetch, 'interval': { 'seconds': 5 }},
]

from wander.worker.spotfetch import SpotFetchJob
from wander.worker.cartosync import CartoSyncJob


