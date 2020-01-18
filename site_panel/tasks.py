from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from main.models import MyUser
from seen.models import Counter_Seen, Last_Seen
from site_panel.models import *

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval",seconds=2)
def delete_last_seen():
	server_datetime = datetime.now()
	server_time = datetime.now().time().strftime('%H:%M')
	time = datetime.strptime('00:00', '%H:%M')
	time = time.time().strftime('%H:%M')
	try:
		counters_seen = Counter_Seen.objects.filter(updated__lt=server_datetime)
		if counters_seen.count():
			if counters_seen.first().updated.date() < server_datetime.date():
				if server_time == time:
					for counter in counters_seen:
						print(counter.updated)
						last_counter = Last_Seen.objects.create(name=counter.name, user_id=counter.user_id,
																counter=counter.counter, path=counter.path,
																date=datetime.now().date())
						counter.counter = 0
						counter.delete()
	except:
		print('amir')


register_events(scheduler)

