import socket
import os

class TCPServer:
    """
    TCP通信を行うサーバークラス
    """
    def serve(self):
        print("===サーバーを起動===")

        try:
            # socketを生成
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # socketをlocalhostのポート8080番に割り当てる
            server_socket.bind(("localhost", 8080))
            server_socket.listen(10)

            # 外部からの接続を待ち、接続があったらコネクションを確立する
            print("=== クライアントからの接続を待ちます ===")
            (client_socket, address) = server_socket.accept()
            print(f"=== クライアントとの接続が完了しました remote_address: {address} ===")

            # クライアントから送られてきたデータを取得する
            request = client_socket.recv(4096)

            # logs ディレクトリが存在しなければ作成
            log_dir = os.path.join(os.path.dirname(__file__), 'logs')
            os.makedirs(log_dir, exist_ok=True)

            # クライアントから送られてきたデータをファイルに書き出す
            file_path = os.path.join(log_dir, "server_recv.txt")
            with open(file_path, "wb") as f:
                f.write(request)

            # 返事は特に返さず、通信を終了させる
            client_socket.close()

        finally:
            print("=== サーバーを停止します。 ===")

if __name__ == '__main__':
    server = TCPServer()
    server.serve()