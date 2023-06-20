import os
import socket
import threading
import asyncio
from motor.motor_tornado import MotorClient
from dotenv import load_dotenv

load_dotenv()
collection = None
connected_clients = set()
change_stream = None

def send_message(message):
    print(f"broadcasting message: {message}")
    for client in connected_clients:
        client.sendall(message.encode())


async def watch(collection):
    global change_stream

    print("watching db")
    async with collection.watch(full_document='updateLookup') as change_stream:
        async for change in change_stream:
            send_message(change["fullDocument"]["msg"])

def handle_connection(connection):
    connected_clients.add(connection)
    while True:
        user_message: str = connection.recv(1024).decode()
        print(user_message)
        # write to mongodb
        collection.insert_one({"msg": user_message})


def main():
    global collection

    mongo_client = MotorClient(os.getenv("MONGO_SERVER_ADDRESS"))
    collection = mongo_client["py-chat"]["chat-logs"]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Server-Socket erstellen
    port = int(os.getenv("SERVER_PORT"))
    s.bind(("0.0.0.0", port)) # Mit Host (IP-Adresse) und Port verbinden
    s.listen() # Zu listenen beginnen
        
    while True:
        print(f"Listening on port {port}")

        connection, addr = s.accept() # Eingehende Verbindung akzeptieren

        thread = threading.Thread(target=handle_connection, args=(connection,)) 
        thread.start()

        threading.Thread(target=asyncio.run, args=(watch(collection),)).start()


if __name__ == "__main__":
    main()