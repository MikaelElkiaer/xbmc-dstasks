from tasks import DS

t = DS("192.168.1.27", False)

t.Login("admin", "p0nyl0ver")

tasks = t.GetTaskList()

for i in tasks:
    print i.Title

t.Logout()

print "hello"