from apscheduler.scheduler import Scheduler

from wander.app import app

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

@sched.interval_schedule(seconds=3)
def some_job():
    print "hello there omg!"

def job_cartosync():
    import cartosync.CartoSyncJob
    job = cartosync.CartoSyncJob(verbose = True)
    job.start()

def job_spotfetch():
    import spotfetch.SpotFetchJob
    json = app.config['SPOT_DATA']
    archive = "sqlite:///:memory"
    job = spotfetch.SpotFetchJob(json_file = json, archive_db = archive, verbose = True)
    job.start()


def start():
    sched.configure()
    sched.start()


