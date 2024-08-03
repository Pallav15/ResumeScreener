    let express = require('express');
    let app = express();
    let bodyParser = require('body-parser');
    let multer = require('multer');
    let path = require('path');
    let fs = require('fs');
    let extract = require('extract-zip');
    const { name } = require('ejs');
    const fetch = require('node-fetch');

    let storage = multer.diskStorage({
        destination: function (req, file, cb) {
            let dir = './uploads/' + Date.now();
            if (!fs.existsSync(dir)){
                fs.mkdirSync(dir, { recursive: true });
            }
            cb(null, dir);
        },
        filename: function (req, file, cb) {
            cb(null, file.originalname);
        }
    });

    let upload = multer({ storage: storage });
    let http = require('http').Server(app);

    app.use(bodyParser.json());
    app.use(bodyParser.urlencoded({ extended: true }));
    app.set('view engine', 'ejs');

    __dirname = __dirname + '/public';

    app.get('/', function (req, res) {
        res.render(__dirname + '/index.ejs');
    });

    app.post('/upload', upload.fields([{ name: 'jd', maxCount: 1 }, { name: 'resume', maxCount: 1 }]), async function (req, res) {
        let jdFile = req.files.jd[0];
        let resumeFile = req.files.resume[0];

        console.log('Job Description File: ', jdFile);
        console.log('Resume File: ', resumeFile);

        // Extract the zip file
        try {
            await extract(resumeFile.path, { dir: path.resolve(resumeFile.destination) });
            console.log('Extraction complete');
        } catch (err) {
            console.log('Error during extraction: ', err);
        }

        results = {};

        jdName = jdFile.originalname.substring(0, jdFile.originalname.lastIndexOf('.'));
        resumeNames = [];
        // find the number of pdf files in the resumepath
        let resumePath = resumeFile.destination;
        let files = fs.readdirSync(resumePath);
        let a=0;
        files.forEach(file => {
            if (file.endsWith('.pdf')) {
                resumeNames.push({ name: file, score: Math.floor(Math.random() * 100) });
                a+=1;
            }
        });
        console.log("value os uploaded files are: ", a)



        await fetch('http://127.0.0.1:8000/process', {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ jd: jdFile.path, resume: resumeFile.path }),
        })
        .then(response => response.json())
        .then(data => {
            results['resume'] = data;
            console.log(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });


        results['jd'] = jdName;

        res.render(__dirname + '/results.ejs', { results: results });

    });

    // app.get('/demo', async (req, res) => {
    //     await fetch('http://127.0.0.1:8000/process', {
    //         method: 'POST', // or 'PUT'
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify({ jd: "Hello", resume: "Bye" }),
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data);
    //         // results['resume'] = data;
    //     })
    //     .catch((error) => {
    //         console.error('Error:', error);
    //     });
    //     res.send("testing");
    // });

    app.listen(3000, function () {
        console.log('Server is running..');
    });