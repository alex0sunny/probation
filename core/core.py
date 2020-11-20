import asyncio
import datetime
from itertools import count

from aiohttp import web
from aiohttp.web_exceptions import HTTPFound

N_WORKERS = 3

QUEUE = asyncio.Queue()

DB = {}

GENERATOR = count(start=1, step=1)

COUNT   =   'count'
DELTA   =   'delta'
START   =   'start'
INTERVAL=   'interval'
CURRENT =   'current'
STATUS  =   'status'
STARTTIME=  'starttime'


async def worker(name, queue):

    while True:
        task_id = await queue.get()
        item = DB[task_id]
        item[STATUS] = 'processing'
        item[STARTTIME] = datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S.%f')[:-5]

        while item[CURRENT] < item[START] + item[COUNT] * item[DELTA]:
            await asyncio.sleep(item[INTERVAL])
            item[CURRENT] += item[DELTA]

        del DB[task_id]


async def tasks_handle(request):
    return web.json_response(DB)


async def enqueue_handle(request):
    params = request.rel_url.query
    if not params:
        raise HTTPFound('/enqueue?count=10&delta=1&start=0&interval=0.5')
    item = {}
    item.update(params)
    item[COUNT]     = int(item[COUNT])
    item[DELTA]     = float(item[DELTA])
    item[START]     = float(item[START])
    item[INTERVAL]  = float(item[INTERVAL])
    item[CURRENT]   = item[START]
    item[STATUS]    = 'pending'
    task_id = next(GENERATOR)
    DB[task_id] = item
    QUEUE.put_nowait(task_id)
    return web.Response(text="accepted task_id: %d\ntask:%s" % (task_id, item))


async def main(loop):

    app = web.Application()
    app.add_routes([web.get('/', tasks_handle),
                    web.get('/enqueue', enqueue_handle)])
    runner = web.AppRunner(app)

    await runner.setup()
    await web.TCPSite(runner).start()

    [loop.create_task(worker(f'worker-{i}', QUEUE)) for i in range(N_WORKERS)]

    await asyncio.Event().wait()

