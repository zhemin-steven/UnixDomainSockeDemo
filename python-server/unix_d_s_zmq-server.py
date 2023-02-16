import zmq
import json
import socket

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("ipc:///tmp/zmq-test.ipc")

while True:
    msg = socket.recv_json()
    print("Received: %s" % msg)

    if msg["command"] == "get_host_info":
        # 获取连接的主机名（在使用 ipc 协议时，这是空字符串）
        hostname = ""

        # 获取连接的 IP 地址（在使用 ipc 协议时，这是连接的端点）
        ip = socket.getsockopt_string(zmq.LAST_ENDPOINT)
        reply = {"status": "success", "hostname": hostname, "ip_address": ip}
        socket.send_json(reply)
    else:
        reply = {"status": "error", "message": "Invalid command"}
        socket.send_json(reply)