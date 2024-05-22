import socketserver

import http.server


class RequestHandler(
    http.server.SimpleHTTPRequestHandler
):
    def do_any_method(self):
        content_length = int(
            self.headers.get("Content-Length", 0)
        )
        body = self.rfile.read(
            content_length
        ).decode("utf-8")
        print(
            f"Request: {self.command} {self.path}\n"
            f"Headers: {self.headers}\n"
            f"Body: {body}\n"
        )
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self.do_any_method()

    def do_POST(self):
        self.do_any_method()

    def do_PUT(self):
        self.do_any_method()

    def do_DELETE(self):
        self.do_any_method()

    def do_PATCH(self):
        self.do_any_method()

    def do_HEAD(self):
        self.do_any_method()

    def do_OPTIONS(self):
        self.do_any_method()


def run_server():
    PORT = 8080
    Handler = RequestHandler

    with socketserver.TCPServer(
        ("", PORT), Handler
    ) as httpd:
        print(f"Server running on port {PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
