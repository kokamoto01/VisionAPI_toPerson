var {PythonShell} = require('python-shell');

require('dotenv').config(); // .envからAPIキーを持ってくる
const API_KEY = process.env.API_KEY 

var options = {
  mode: 'text', // testもしくはjson
  pythonPath: '/usr/local/bin/python3', // Python3のパスを指定しないと動かないので注意
  args: [API_KEY, 'test02.jpg'] // 引数を設定
};

var pyshell = new PythonShell('./test.py',options);
pyshell.on('message',function(message){
  console.log(message);
});