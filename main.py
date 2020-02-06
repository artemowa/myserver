import socket
import os

from mainpackage.urls import URLS
from settingspackage import settings


def parse_request(request):
    parsed = request.split(' ')
    return (parsed[0], parsed[1])


def generate_headers(method, url):
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)
    elif 'static' in url:
        if os.path.isfile(os.path.join(settings.BASE_DIR, url[1:])):
            return ('HTTP/1.1 200 OK\n\n', 200)
        else:
            return ('HTTP/1.1 404 Not found\n\n', 404)
    elif url not in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)
    else:
        return ('HTTP/1.1 200 OK\n\n', 200)


def generate_content(url, code):
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    elif code == 404:
        return '<h1>404</h1><p>Not found</p>'
    elif 'static' in url:
        with open(os.path.join(settings.BASE_DIR, url[1:])) as staticfile:
            return staticfile.read()
    else:
        return URLS[url].get_response()

def generate_response(request):
    method, url = parse_request(request.decode('utf-8'))
    header, code = generate_headers(method, url)
    content = generate_content(url, code)
    return (header + content).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8000))
    server_socket.listen()
    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)

        print(request.decode('utf-8'))

        response = generate_response(request)
        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run()
