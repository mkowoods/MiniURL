const express = require('express');
const fetch = require('node-fetch');
const bodyParser = require('body-parser')
const app = express();
const router = express.Router();

const path = __dirname + '/views/';
const port = 8080;
const api_host = process.env.API_HOST
const api_port = process.env.API_PORT


app.use(bodyParser.json())

router.use(function (req, res, next) {
    console.log('/' + req.method);
    next();
});

router.get('/', function (req, res) {
    res.sendFile(path + 'index.html');
});

router.get('/:tag', function (req, res) {
    if (!req.params.tag || req.params.tag === 'favicon.ico') {
        return
    }
    const url = `http://${api_host}/api/${req.params.tag}`
    console.warn('url:', url)
    fetch(url)
        .then(res => {
            if (res.status !== 200) {
                console.log('Not 200 Error')
                throw new Error("Not 200 response")
            } else {
                return res.json()
            }
        })
        .then(data => {
            // Check that a URL is returned
            data.url && res.redirect(data.url)
        })
        .catch(err => {
            console.warn('Hit Error!!')
            res.send({'error': 'hit error!!'})
        })
});


app.post('/create_tag', (req, res) => {
    if (req.body && req.body.url) {
        const url = `http://${api_host}/api/urls`
        console.warn('posting', req.body.url, 'to', url)
        fetch(url, {
            method: 'POST',
            body: JSON.stringify({url: req.body.url}),
            headers: {
                'Content-Type': 'application/json'
            }

        })
            .then(res => {
                if (res.status !== 200) {
                    console.log('Not 200 Error', res)
                    throw new Error("Not 200 response")
                } else {
                    return res.json()
                }
            })
            .then(json => {
                res.send(json)
            })
            .catch(err => {
                console.warn('Hit Error!!')
                res.send({'error': 'hit error!!'})
            })
    }
})

app.use(express.static(path));
app.use('/', router);


app.listen(port, function () {
    console.log('API_HOST', process.env.API_HOST, 'API_PORT', process.env.API_PORT)
    console.log('Example app listening on port 8080!')
})