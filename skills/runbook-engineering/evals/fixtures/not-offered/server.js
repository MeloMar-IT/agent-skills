const http = require('http');

const server = http.createServer((req, res) => {
  if (req.method === 'GET' && req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('hello');
    return;
  }
  res.writeHead(404);
  res.end();
});

server.listen(process.env.PORT || 3000);
