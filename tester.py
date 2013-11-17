from tasks import DS
from decimal import Decimal

t = DS("192.168.1.27", False)

t.Login("admin", "p0nyl0ver")

tasks = t.GetTaskList()

for task in tasks:
    print "%.2f" % (float(float(task.SizeUploaded) / float(task.Size)) * 100)

t.Logout()