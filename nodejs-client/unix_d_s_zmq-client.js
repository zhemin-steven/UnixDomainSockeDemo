const zmq = require('zeromq')
const json = require('json-bigint')

const socket = zmq.socket('pair')
socket.connect('ipc:///tmp/zmq-test.ipc')

const request = {"command": "get_host_info"}
socket.send(json.stringify(request))
console.log(`Sent: ${JSON.stringify(request)}`)

socket.on('message', (msg) => {
  const reply = json.parse(msg.toString())
  console.log(`Received: ${JSON.stringify(reply)}`)
})

process.on('SIGINT', () => {
  socket.close()
  console.log('\nClosed the socket.')
  process.exit(0)
})