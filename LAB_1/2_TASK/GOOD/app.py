from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            response = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>ОК</title>
            </head>
            <body>
                <p>Сервер работает</p>
            </body>
            </html>
            """
            self.wfile.write(response.encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

def main():
    port = 8000
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"Сервер запущен на http://localhost:{port}")    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
        server.shutdown()

if __name__ == '__main__':
    main()