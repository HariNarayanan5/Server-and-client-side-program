import socket
import threading
import tkinter as tk

def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            message_list.insert(tk.END, message)
        except:
            break

def send_message(event=None):
    message = message_entry.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        message_entry.delete(0, tk.END)

def on_closing(event=None):
    message_entry.delete(0, tk.END)
    message_entry.insert(0, "bye")
    send_message()
    root.quit()

def start_client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5050))

    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()

    root.protocol("WM_DELETE_WINDOW", on_closing)

root = tk.Tk()
root.title("Chat Application")

message_list = tk.Listbox(root, height=20, width=50)
message_list.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.bind("<Return>", send_message)
message_entry.pack(padx=10, pady=5)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=5)

start_client()

root.mainloop()
