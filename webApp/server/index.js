const express = require('express');
const app = express();
const PORT = process.env.PORT || 3001;


// Parse incoming JSON requests
app.use(express.json());
const messages = ["Hello World!", "How are you?", "I'm doing great!"];
const track = {};
const competitors = {};


app.post('/api/msgs', (req, res) => {
  //console.log(req.body); // Log the message from the request body
  res.status(200).send('Message received');
  messages.push(req.body['content']);
//  res.json({ message: "Hello from server!" });
});

app.post('/api/competitors', (req, res) => {
  //console.log(req.body); // Log the message from the request body
  res.status(200).send('Message received');
  competitors[req.body['id']] = [req.body['x'], req.body['y']];
//  res.json({ message: "Hello from server!" });
});

app.post('/api/track', (req, res) => {
  //console.log(track); // Log the message from the request body
  res.status(200).send('Message received');
  track[req.body['id']] = [req.body['a'], req.body['b'], req.body['flag']];
//  res.json({ message: "Hello from server!" });
});

app.get("/api/msgs", (req, res) => {
  res.json({ message: messages });
});
app.get("/api/competitors", (req, res) => {
  res.json({ competitors: competitors });
});
app.get("/api/track", (req, res) => {
  res.json({ track: track });
});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
