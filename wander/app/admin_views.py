from flask import redirect, url_for, request
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin import BaseView, expose
from wander.app import  db, admin
import models

from wander.worker import sched, log_file
from wander.worker import jobs as _jobs

def tail(f, n, offset=None):
    """Reads a n lines from f with an offset of offset lines.  The return
    value is a tuple in the form ``(lines, has_more)`` where `has_more` is
    an indicator that is `True` if there are more lines in the file.
    http://stackoverflow.com/a/692616
    """
    avg_line_length = 74
    to_read = n + (offset or 0)

    while 1:
        try:
            f.seek(-(avg_line_length * to_read), 2)
        except IOError:
            # woops.  apparently file is smaller than what we want
            # to step back, go to the beginning instead
            f.seek(0)
        pos = f.tell()
        lines = f.read().splitlines()
        if len(lines) >= to_read or pos == 0:
            return lines[-to_read:offset and -offset or None], \
                   len(lines) > to_read or pos > 0
        avg_line_length *= 1.3

class Jobs(BaseView):

    def get_jobs(self):
        active_jobs = sched.get_jobs()
        job_names = [ j.name for j in active_jobs ]
        inactive_jobs = [ j['name'] for j in filter(lambda x: x['name'] not in job_names, _jobs)]
        return active_jobs, inactive_jobs

    def _error(self, msg):
        return self.render('admin_error.html', error=msg)#

    @expose('/')
    def index(self):
        active, inactive = self.get_jobs()
        return self.render('admin_jobs.html', jobs=active, inactive=inactive)

    @expose('/stop/<int:job_id>', methods=['POST'])
    def stop(self, job_id):
        active, inactive = self.get_jobs()
        if job_id >= len(active) or job_id < 0:
            return self._error("Invalid job ID")

        job = active[job_id]
        sched.unschedule_job(job)
        return redirect(url_for(".index"))

    @expose('/start/<job_name>', methods=['POST'])
    def start(self, job_name):
        for j in _jobs:
            if j['name'] == job_name:
                sched.add_interval_job(j['func'], **j['interval'])
        return redirect(url_for(".index"))
    @expose('/logs')
    def logs(self):
        n = request.args.get('lines', default=50, type=int)
        with open(log_file, 'r') as f:
            log,hasmore = tail(f, n)
            log = '\n'.join(log)
            return self.render('admin_logs.html', log=log)


class PKView(ModelView):
    column_display_pk = True

class TripView(PKView):
    column_hide_backrefs = False
    column_list = ('id', 'name', 'description', 'user')

admin.add_view(PKView(models.User, db.session))
admin.add_view(TripView(models.Trip, db.session))
admin.add_view(PKView(models.Point, db.session))
admin.add_view(Jobs(name="Jobs"))
