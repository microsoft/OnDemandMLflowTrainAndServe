const { createLogger, format, transports } = require('winston');

// set the log level if supplied
const logLevel = process.env.LOG_LEVEL ? process.env.LOG_LEVEL : 'info';

const logger = createLogger({
    level: logLevel,
    format: format.combine(format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }), format.json()),
    transports: [new transports.Console()],
});

module.exports = logger;
