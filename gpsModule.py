import http.server
import socketserver
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', socket_timeout=None))
competitorsChannel = connection.channel()
trackChannel = connection.channel()

class RequestHandler(http.server.BaseHTTPRequestHandler):
    """
    A request handler class that forwards incoming POST requests to RabbitMQ, depending on their ID.
    """

    def do_POST(self):
        """
        Handles incoming POST requests.

        Reads the request body, and forwards it to RabbitMQ, depending on its ID.
        Sends a response back to the client.
        """

        # Read the request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Forward the request body to RabbitMQ
        data = post_data.decode('utf-8')
        id = str(eval(data)['id'])
        if id.isnumeric() and int(id) > 9999:
            trackChannel.queue_declare(queue='TRACK')
            trackChannel.basic_publish(exchange='', routing_key='TRACK', body=data)
        else:
            competitorsChannel.queue_declare(queue='GPS')
            competitorsChannel.basic_publish(exchange='', routing_key='GPS', body=data)

        # Send a response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"{failed: False, success: True}")

# Create a socket server that listens on port 8000
with socketserver.TCPServer(("", 8000), RequestHandler) as httpd:
    """
    A TCP server that listens on port 8000, and handles incoming requests.

    This script starts a TCP server that listens on port 8000, and handles incoming HTTP POST requests.
    Forwards incoming POST requests to RabbitMQ, depending on their ID.
    """

    print("Server listening on port 8000...")
    httpd.serve_forever()
