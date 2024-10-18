from http.server import BaseHTTPRequestHandler, HTTPServer
from config import file_path
import os

hostName = "localhost"  # Address for network access
serverPort = 8080  # Port for network access


class MyServer(BaseHTTPRequestHandler):
    """Class for handling incoming client requests."""

    def do_GET(self):
        """Method to handle incoming GET requests."""
        self.send_response(200)

        if self.path == "/":
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
            self.wfile.write(bytes(content, "utf-8"))
        else:
            # Serve static files
            self.handle_static_files()

    def handle_static_files(self):
        """Serve static files (like CSS, JS)."""
        static_dir = os.path.join(os.getcwd())
        file_path = os.path.join(static_dir, self.path[1:])

        if os.path.isfile(file_path):
            self.send_header("Content-type", self.guess_type(file_path))
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())

    def guess_type(self, file_path):
        """Guess the content type based on file extension."""
        if file_path.endswith('.css'):
            return 'text/css'
        elif file_path.endswith('.js'):
            return 'application/javascript'

    def do_POST(self):
        """Method for handling POST requests."""
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        print(post_data)

        response = f"Received POST data: {post_data.decode('utf-8')}"
        print(response)


if __name__ == "__main__":
    # Initialize web server
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started at http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")