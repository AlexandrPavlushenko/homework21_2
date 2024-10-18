from http.server import BaseHTTPRequestHandler, HTTPServer
from config import file_path


hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """
    def do_GET(self):
        """ Метод для обработки входящих GET-запросов
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(file_path, encoding='utf-8') as f:
            content = f.read()
        self.wfile.write(bytes(content, "utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        print(post_data)

        response = f"Received POST data: {post_data.decode('utf-8')}"
        print(response)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")