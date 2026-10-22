"""Task-01: interactive UTF-8 TCP echo client."""
import argparse
import socket

MAX_LINE = 65536


def echo(sock, reader, text):
    data = (text + '\n').encode('utf-8')
    if len(data) > MAX_LINE:
        raise ValueError('Chuỗi quá dài: tối đa 65535 byte UTF-8.')
    sock.sendall(data)
    result = reader.readline(MAX_LINE + 1)
    if not result:
        raise EOFError('Server đã đóng kết nối.')
    if result != data:
        raise ValueError('Phản hồi không khớp hoặc bị thiếu.')
    return result[:-1].decode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host')
    parser.add_argument('--port', type=int)
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()
    host = args.host or input('IP server [127.0.0.1]: ').strip() or '127.0.0.1'
    port = args.port
    if port is None:
        try:
            port = int(input('Cổng server [50000]: ').strip() or '50000')
        except ValueError:
            parser.error('Cổng phải là số nguyên.')
    if not 1 <= port <= 65535:
        parser.error('Cổng phải từ 1 đến 65535.')
    with socket.create_connection((host, port), timeout=5) as sock:
        print(f'Kết nối đến {host}:{port} thành công.', flush=True)
        with sock.makefile('rb') as reader:
            if args.test:
                for i in range(1, 11):
                    text = f'Tin nhắn {i}: Xin chào, mạng máy tính!'
                    print(f'PASS {i}/10: {echo(sock, reader, text)}', flush=True)
                print('Kết quả: 10/10 chuỗi UTF-8 đúng.')
            else:
                print('Nhập chuỗi để gửi; gõ /quit để ngắt kết nối.')
                while True:
                    text = input('Nhập nội dung: ')
                    if text == '/quit':
                        break
                    if len((text + '\n').encode('utf-8')) > MAX_LINE:
                        print('Chuỗi quá dài, hãy nhập lại.')
                        continue
                    print('Server trả về:', echo(sock, reader, text), flush=True)
    print('Đã ngắt kết nối.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nĐã kết thúc client.')
    except EOFError as exc:
        print(f'\nĐã kết thúc client. {exc}')
        if str(exc):
            raise SystemExit(1)
    except (OSError, ValueError, UnicodeError) as exc:
        raise SystemExit(f'Lỗi kết nối/truyền nhận. Kiểm tra IP, cổng và server: {exc}')
