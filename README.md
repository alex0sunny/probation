# probation

Probation task on asyncio and aiohttp.

Enpoints:

http://localhost:8080/

http://localhost:8080/enqueue

Python developer test task
==============

Create github repository with aiohttp application on Python 3.6. run.py should be at the root. The backend should calculate the arithmetic sequence (sum of members). Simultaneously with the launch of the application, a web server should be launched with two endpoints:
1. Enqueue task. Parameters:
- count - number of elements (int)
- delta - arithmetic progression common difference (float)
- start - initial term
- interval - interval between iterations in seconds (float)

2. Get the sorted list of tasks and their statuses. Result fields for every task:
- Number in queue
- Status: in process/in queue
- count
- delta
- start
- interval
- currently calculated value
- calculation start date

--------

### Requirements:
- Remove completed tasks
- Store data in memory
- Application starts as a single process
- Current value calculation should depend exclusively on interval and on common difference and should not take into account number of iterations nor time elapsed from the start of the task.
- Task is enquued and, if possible, processed immediately.
- One worker executes only one task
- It should be possible to set the maximum number of parallel execution workers
