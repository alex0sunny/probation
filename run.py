import asyncio

from core.core import main

loop = asyncio.get_event_loop()

loop.run_until_complete(main(loop))
loop.close()
