"""Task-01: TCP echo server, one client at a time."""
import argparse
import socket

MAX_LINE = 65536


def serve_client(conn, peer):
    print(f'Client đã kết nối: {peer[0]}:{peer[1]}', flush=True)
    conn.settimeout(300)
    with conn.makefile('rb') as reader:
        while True:
            data = reader.readline(MAX_LINE + 1)
            if not data:
                print('Client đã ngắt kết nối.', flush=True)
                return
            if len(data) > MAX_LINE or not data.endswith(b'\n'):
                raise ValueError('Thông điệp quá dài hoặc bị ngắt giữa chừng.')
            text = data[:-1].decode('utf-8')
            print(f'Đã nhận: {text}', flush=True)
            conn.sendall(data)
            print('Đã gửi phản hồi.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=50000)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error('Cổng phải từ 1 đến 65535.')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((args.host, args.port))
        server.listen(1)
        print(f'Đang chờ kết nối tại {args.host}:{args.port}...', flush=True)
        while True:
            conn, peer = server.accept()
            with conn:
                try:
                    serve_client(conn, peer)
                except (OSError, ValueError, UnicodeError) as exc:
                    print(f'Lỗi phiên kết nối: {exc}', flush=True)
            print('Đang chờ client tiếp theo...', flush=True)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nĐã dừng server.')
    except OSError as exc:
        raise SystemExit(f'Không khởi động được server. Kiểm tra IP/cổng: {exc}')
