
## How It Works
- **Client (`client.py`):** Responsible for creating the user interface where users can interact and send data to the server. It also handles receiving responses from the server.
- **Server (`server.py`):** Receives requests from the client, processes these requests (e.g., database operations, computations), and sends back the responses.

### Setup
1. **Server Setup:** Run `server.py` on the server machine. Ensure it is properly configured to accept incoming network connections.
2. **Client Setup:** Run `client.py` on one or more client machines. Configure each client to connect to the server's IP address and port.

## Running the Application
- Start the server first by executing `python server.py`.
- Then, on the client machine, run `python client.py`.
