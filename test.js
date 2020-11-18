var {PythonShell} = require('python-shell');
var options = {
  mode: 'text', // testもしくはjson
  pythonPath: '/usr/local/bin/python3', // Python3のパスを指定しないと動かないので注意
  args: ['AIzaSyCLp2_-BzLz1hozOAuqXlyvhi5iR8BzaGY', 'test03.png'] // 引数を設定
};

var pyshell = new PythonShell('./test.py',options);
pyshell.on('message',function(message){
  console.log(message);
});