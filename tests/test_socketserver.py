from socketserver import BaseRequestHandler, ThreadingTCPServer


class EchoHandler(BaseRequestHandler):
    def handle(self):
        # data = self.request.recv(1024)
        self.request.sendall("\nabc\n".encode())
        # self.request.sendall("END")


server = ThreadingTCPServer(("0.0.0.0", 2019), EchoHandler)
server.serve_forever()