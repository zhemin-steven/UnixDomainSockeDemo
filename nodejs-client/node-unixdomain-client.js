const net = require('net');

const socketPath = '/tmp/test.sock';

function sendRequest(request) {
  return new Promise((resolve, reject) => {
    const client = net.createConnection(socketPath, () => {
      client.write(request);
    });

    client.on('data', (data) => {
      try {
        const response = JSON.parse(data.toString());
        resolve(response);
      } catch (err) {
        reject(err);
      }
      client.end();
    });

    client.on('end', () => {
      reject(new Error('Disconnected from server.'));
    });

    client.on('timeout', () => {
      reject(new Error('Connection timed out.'));
      client.destroy();
    });

    client.on('error', (err) => {
      reject(err);
      client.destroy();
    });

    client.setTimeout(1000);
  });
}

async function main() {
  try {
    console.log(`Sending request to server at ${socketPath}`);
    const response = await sendRequest('get_host_info');
    console.log(`Received response from server:`, response);
    console.log(`Sending request1 to server at ${socketPath}`);
    const response1 = await sendRequest('get_host_info');
    console.log(`Received response1 from server:`, response1);
  } catch (err) {
    console.error(`Error occurred: ${err}`);
  }
}

main();
