import socket
import os
from datetime import datetime

class WebServer:
    """
    WebServer を表すクラス
    """
    def serve(self):
        # サーバーを起動する

        print("=== サーバーを起動します ===")

        try:
            # socketの生成
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # socket をlocalhostの8080ポートに割り当てる
            server_socket.bind(("localhost", 8080))
            server_socket.listen(10)

            # 外部からの接続まし、接続があった場合コネクションを確立する
            print("=== クライアントからの接続を待ちます ===")
            (client_socket, address) = server_socket.accept()
            print("=== クライアントとの接続が完了しました remoto_address: {address} ===")

            # クライアントから送られてきたデータを取得
            request = client_socket.recv(4096)

            # レスポンス内容をファイルに書き出す
            # logs ディレクトリが存在しなければ作成
            log_dir = os.path.join(os.path.dirname(__file__), 'logs')
            os.makedirs(log_dir, exist_ok=True)

            # クライアントから送られてきたデータをファイルに書き出す
            file_path = os.path.join(log_dir, "server_recv.txt")
            with open(file_path, "wb") as f:
                f.write(request)

            # レスポンスボディを作成
            respons_body = "<html><body><h1>Hello Python WEB SERVER</h1></body></html>"

            # レスポンスラインを作成
            response_line = "HTTP/1.1 200 OK\r\n"
            # レスポンスヘッダーを作成
            response_header = ""
            response_header += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            response_header += "Host: TestPythonServer/0.1\r\n"
            response_header += f"Content-Length: {len(respons_body.encode())}\r\n"
            response_header += "Connectin: Close\r\n"
            response_header += "Content-Type: text/html\r\n"

            # ヘッダーとボディを空行でくっつけた上で bytes に変換しレスポンス全体を作成する
            response = (response_line + response_header + "\r\n" + respons_body).encode()

            # クライアントへレスポンスを送信する
            client_socket.send(response)

            # 通信を終了する
            client_socket.close()

        finally:
            print("=== サーバーを停止します ===")

if __name__ == '__main__':
    server = WebServer()
    server.serve()
