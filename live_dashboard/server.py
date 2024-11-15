import asyncio
import json
import websockets
import random
import time

connected_clients=set()
page_views=0

async def send_data(websocket):
    global page_views
    page_views+=1;
    start_time=time.time()
    while True:
        session_time= (time.time()-start_time)/60
        data = {
                "active_users": len(connected_clients),
                "page_views": page_views,
                "session_time": session_time
            }
        await websocket.send(json.dumps(data))
        await asyncio.sleep(2)

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        await send_data(websocket)
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler,"localhost",3000):
        print('Server running of ws://localhost:3000')
        await asyncio.Future()

asyncio.run(main())
