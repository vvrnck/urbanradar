require('dotenv').config();
const path = require("path");
const fs = require("fs");

const history = require('connect-history-api-fallback');
const express = require("express");

const PORT = process.env.PORT || 3000;
const app = express(); // create express app

app.use(express.json());

app.post('/configuration', function(req, res) {
  try {
    const body = req.body;
  
    const filePath = path.resolve("app", "account.txt");
    if (!filePath) {
      res.status(500);
      res.end();
    }
    let [username, password,] = fs.readFileSync(filePath, "utf-8").split("\n");

    username = username.replace("username:", "");
    password = password.replace("password:", "");
    
    if (username === body.username && password === body.password) {
      res.status(200);
      res.send(JSON.stringify({ login: true }));  
    }

    res.send(JSON.stringify({ login: false }));
  } catch(e) {
    res.status(500);
    res.end();
  }
});

app.get('/', function (req,res) {
  res.sendFile(path.resolve("app", "dist", "index.html"));
});

//app.use(express.static(path.join(__dirname, "app", "dist"), { etag: false }));
const staticFileMiddleware = express.static(path.join(__dirname, "app", "dist"));
app.use(staticFileMiddleware);
app.use(history({
  disableDotRule: true,
  verbose: true
}));
app.use(staticFileMiddleware);

// start express server
app.listen(PORT, () => {
  console.log(`frontend server started on port ${PORT}`);
});