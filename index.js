const express = require('express');
const app = express();
const path = require('path');
const { exec } = require('child_process');

app.use(express.static(path.join(__dirname, '/public')));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '/views'));

app.get('/', (req, res) => {
    res.render('home');
});


app.get('/start_game', (req, res) => {
    res.render('game');

    exec('python3 main.py', { cwd: __dirname }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error!!! ${error.message}`);
        } else {
            console.log("Yayyy it ran successfully");
            console.log(`stdout: ${stdout}`);
            console.error(`stderr: ${stderr}`);
        }
    });
});

app.listen(3000, () => {
    console.log('listening on port 3000');
});
