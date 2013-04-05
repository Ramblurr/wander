from apscheduler.scheduler import Scheduler

sched = Scheduler()

@sched.interval_schedule(seconds=3)

def some_job():
    print "hello there omg!"

def start():
    sched.configure()
    sched.start()
