import asyncio
import os
import socket
import struct
import json


async def handle_connection(reader, writer):
    try:
        while True:
            # 读取消息长度
            data = await reader.readexactly(4)
            msg_len = struct.unpack('!I', data)[0]

            # 读取消息体
            try:
                data = await asyncio.wait_for(reader.readexactly(msg_len), timeout=10)
            except asyncio.TimeoutError:
                print("Failed to read message body in 10 seconds")
                break
            message = data.decode('utf-8').strip()
            try:
                # 解析json对象
                message_json = json.loads(message)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return
            print(f'Received message: {message_json}')

            if message_json["request"]== 'get_host_info':
                # 获取主机名和 IP 地址
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                # 发送主机名和 IP 地址到客户端
                response = {'hostname': hostname, 'ip_address': ip_address}
                response_json = json.dumps(response)
                # 打包消息
                msg = struct.pack('!I', len(response_json)) + response_json.encode('utf-8')
                writer.write(msg)
                await writer.drain()
    except (asyncio.IncompleteReadError, ConnectionResetError):
        print('Client disconnected')
    finally:
        writer.close()


async def start_server():
    # 创建 Unix 域套接字
    server_address = '/tmp/test.sock'

    # 删除已存在的socket文件
    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise

    # 创建异步的 Unix 域套接字服务端
    server = await asyncio.start_unix_server(handle_connection, server_address)
    async with server:
        await server.serve_forever()


async def main():
    await start_server()


if __name__ == "__main__":
    asyncio.run(main())