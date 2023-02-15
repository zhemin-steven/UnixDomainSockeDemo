const net = require('net');
const { BufferList } = require('bl');
const { promisify } = require('util');

// 创建 Unix 域套接字连接
const socketPath = '/tmp/test.sock';
const client = net.createConnection(socketPath);

const readData = () => new Promise(resolve => client.on('data', resolve));
const endConnection = promisify(client.end).bind(client);

async function requestHostInfo() {
  try {
    await new Promise((resolve, reject) => {
      client.once('connect', resolve);
      client.once('error', reject);
    });

    console.log(`Connected to server at ${socketPath}`);

    // 发送请求到服务端
    const request = 'get_host_info';
    console.log(`Sending request: ${request}`);

    const message = JSON.stringify({ request });
    const messageLength = Buffer.alloc(4);
    messageLength.writeUInt32BE(message.length);
    client.write(Buffer.concat([messageLength, Buffer.from(message, 'utf-8')]));

    const buffer = new BufferList();
    let messageBytesReceived = 0;
    while (true) {
      const data = await readData();
      buffer.append(data);
      messageBytesReceived += data.length;

      while (messageBytesReceived >= 4) {
        const messageLength = buffer.readUInt32BE(0);
        if (messageBytesReceived >= messageLength + 4) {
          const message = buffer.slice(4, messageLength + 4);
          try {
            const response = JSON.parse(message.toString('utf-8'));
            console.log(`Received response from server:`, response);
          } catch (err) {
            console.error(`Error parsing JSON: ${err}`);
          }
          await endConnection();
          return;
        }
        break;
      }
    }
  } catch (err) {
    console.error(`Error occurred: ${err}`);
  } finally {
    console.log(`Disconnected from server at ${socketPath}`);
  }
}

requestHostInfo();
