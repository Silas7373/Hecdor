import threading
import socket
import os
from dotenv import load_dotenv
load_dotenv()

def on_connect(websocket):
    print("Connection established")

def on_disconnect(websocket):
    print("Connection closed")

def on_receive(message):
    print(f"Received message: '{message.decode()}'")

def receive_messages(websocket):
    try:
        while True:
            message = websocket.recv(1024)
            if not message:
                websocket.close()
                exit()
            on_receive(message)
    except:
        websocket.close()

def send_messages(websocket):
    while True:
        message = input()
        if message == "exit" or message == "":
            websocket.close()
            return
        
        websocket.sendall(message.encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ws:
        ws.connect((input("Server IP: "), int(os.getenv("SERVER_PORT"))))

        print("connected")
        
        on_connect(ws)
        
        thread = threading.Thread(target=receive_messages, args=(ws,))
        thread.start()

        send_messages(ws)

if __name__ == "__main__":
    main()