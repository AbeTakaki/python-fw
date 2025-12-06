import socket
import os

class TCPClient:
    """
    TCP通信を行うクライアントクラス
    """
    def request(self):
        """
        サーバーへリクエストを送る
        """

        print("=== クライアントを起動します ===")

        try:
            # socket を生成
            client_socket = socket.socket()
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # サーバーと接続する
            print("=== サーバーと接続します ===")
            client_socket.connect(("127.0.0.1", 80))
            print("=== サーバーとの接続が完了しました ===")

            # サーバーに送信するリクエストをファイルから取得する
            with open("client_send.txt", "rb") as f:
                request = f.read()

            # サーバーへリクエストを送信
            client_socket.send(request)

            # レスポンスを待ち取得する
            response = client_socket.recv(4096)

            # レスポンス内容をファイルに書き出す
            # logs ディレクトリが存在しなければ作成
            log_dir = os.path.join(os.path.dirname(__file__), 'logs')
            os.makedirs(log_dir, exist_ok=True)

            # クライアントから送られてきたデータをファイルに書き出す
            file_path = os.path.join(log_dir, "server_recv.txt")
            with open(file_path, "wb") as f:
                f.write(response)

            # 通信を終了
            client_socket.close()
        finally:
            print("=== クライアントを停止します ===")

if __name__ == '__main__':
    client = TCPClient()
    client.request()