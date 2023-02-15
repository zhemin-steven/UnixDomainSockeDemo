import asyncio
import os
import socket
import json


async def handle_connection(reader, writer):
    data = await reader.read(1024)
    if data:
        message = data.decode('utf-8').strip()
        print(f'Received message: {message}')
        if message == 'get_host_info':
            # 获取主机名和 IP 地址
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            # 发送主机名和 IP 地址到客户端
            response = {'hostname': hostname, 'ip_address': ip_address}
            writer.write(bytes(json.dumps(response), 'utf-8'))
            await writer.drain()
            writer.close()
    else:
        print('No data received from client')


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
