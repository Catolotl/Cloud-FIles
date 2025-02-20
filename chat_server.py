import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import time
from datetime import datetime

# Store chat rooms with details: messages, active users, and server location
chat_rooms = {}

# A helper function to manage active users for each room
def get_active_users(room_name):
    return len(chat_rooms.get(room_name, {}).get('users', []))

# A helper function to fetch the server location (for simplicity, hardcoded)
def get_server_location(room_name):
    return " North America"  # Hardcoded for now, can be "Europe", "Asia", etc.

MAX_MESSAGES = 100  # Maximum number of messages per room

class ChatServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the chat page if it's the root path
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'r') as file:
                self.wfile.write(file.read().encode())
        
        # Handle request for all chat rooms
        elif self.path == '/rooms':
            self.handle_get_rooms()
        
        # Handle request for messages in a specific room
        elif self.path.startswith('/room/'):
            room_name = self.path.split('/')[2]
            self.handle_get_messages(room_name)
        
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # Handle creating a new room
        if self.path == '/create_room':
            self.handle_create_room()
        
        # Handle sending a message to a specific room
        elif self.path.startswith('/send/'):
            room_name = self.path.split('/')[2]
            self.handle_send_message(room_name)
        
        # Handle adding a user to a room (for tracking active users)
        elif self.path.startswith('/join/'):
            room_name = self.path.split('/')[2]
            self.handle_join_room(room_name)
        
        else:
            self.send_response(404)
            self.end_headers()

    def handle_get_rooms(self):
        """Return a list of all active rooms, including server location and active users."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        rooms = []
        
        for room_name, room_data in chat_rooms.items():
            rooms.append({
                "name": room_name,
                "location": get_server_location(room_name),
                "active_users": get_active_users(room_name)
            })
        
        self.wfile.write(json.dumps({"rooms": rooms}).encode())

    def handle_get_messages(self, room_name):
        """Return the messages in a specific chat room."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if room_name not in chat_rooms:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Room not found")
            return
        
        messages = chat_rooms.get(room_name, {}).get("messages", [])
        self.wfile.write(json.dumps({"messages": messages}).encode())

    def handle_create_room(self):
        """Create a new chat room."""
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        data = json.loads(post_data.decode())
        room_name = data.get("room_name")

        if room_name:
            chat_rooms[room_name] = {
                "messages": [],  # Initialize an empty message list for the new room
                "users": []      # Active users list
            }

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Room created")

    def handle_send_message(self, room_name):
        """Send a message to a specific chat room."""
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        data = json.loads(post_data.decode())

        message = data.get("message")
        username = data.get("username")

        if room_name not in chat_rooms:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Room not found")
            return

        if message and username:
            timestamp = datetime.now().strftime("%H:%M")
            chat_rooms[room_name]["messages"].append(f"{timestamp} {username}: {message}")
            
            # Limit the number of messages in the room to MAX_MESSAGES
            if len(chat_rooms[room_name]["messages"]) > MAX_MESSAGES:
                chat_rooms[room_name]["messages"].pop(0)  # Remove the oldest message

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Message received")

    def handle_join_room(self, room_name):
        """Add the user to the room's active users list."""
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        data = json.loads(post_data.decode())

        username = data.get("username")
        if username and room_name in chat_rooms:
            if username not in chat_rooms[room_name]["users"]:
                chat_rooms[room_name]["users"].append(username)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"User joined room")

# Start the server
def run(server_class=HTTPServer, handler_class=ChatServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    print('Server Side: http://localhost:8000/ Client Side: http://192.168.1.242:8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
