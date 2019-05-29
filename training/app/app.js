const express = require('express');
const bodyParser = require('body-parser');
const dotenv = require('dotenv');
const logger = require('./logging');

dotenv.config();

// Setup app insights
require('./app-insights');
// Environment variables validation
require('./validate-env-vars');

const app = express();

app.use(bodyParser.json());
app.use('/train', require('./routes/training-routes'));

app.get('/', (req, res) => res.send('Training Service is up.'));

const port = process.env.PORT;
app.listen(port, () => logger.info(`Training Service: Listening on port ${port}!`));
