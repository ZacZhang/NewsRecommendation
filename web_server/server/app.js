let bodyParser = require('body-parser');
let cors = require('cors');
let express = require('express');
let mongoose = require('mongoose');
let passport = require('passport');
let path = require('path');

let index = require('./routes/index');
let news = require('./routes/news');
let auth = require('./routes/auth');

let app = express();

let config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri);

// view engine setup
// 之后可以把react前端npm run build 到'../client/build/'文件夹下，这样就不用同时开react前端和node.js的前端，只需要node.js就可以了
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

app.use(cors());
app.use(bodyParser.json());

// load passport strategies
app.use(passport.initialize());
let localSignupStrategy = require('./passport/signup_passport');
let localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// pass the authentication checker middleware
const authCheckMiddleware = require('./middleware/auth_checker');
app.use('/news', authCheckMiddleware);

app.use('/', index);
app.use('/news', news);
app.use('/auth', auth);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    let err = new Error('Not Found');
    err.status = 404;
    res.send('404 Not Found');
});

module.exports = app;
