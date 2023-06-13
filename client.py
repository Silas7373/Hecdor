import asyncio
import websockets

async def on_connect(websocket):
    print("Connection established")

async def on_disconnect(websocket):
    print("Connection closed")

async def on_receive(message):
    print("Received message:", message)

async def receive_messages(websocket):
    async for msg in websocket:
        print(msg)

async def main():

    async with websockets.connect("ws://10.10.1.218:5000/chat") as websocket:
        
        await on_connect(websocket)
        
        receive_task = asyncio.ensure_future(receive_messages(websocket))
       
        while True:
            user_input = input("Enter a message to send (or 'quit' to exit): ")

            if user_input == "quit":
                break

            await websocket.send(user_input)
            _ = await websocket.recv()

        receive_task.cancel()
        try:
            await receive_task
        except asyncio.CancelledError:
            pass

        await on_disconnect(websocket)


asyncio.get_event_loop().run_until_complete(main())
