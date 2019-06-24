const validator = require('validator');
const logger = require('./logging');

function logAndThrowError(msg) {
    logger.error(msg);
    throw new Error(msg);
}

function validateVarNotEmpty(varName) {
    if (!process.env[varName]) {
        logAndThrowError(`Environment variable ${varName} was not supplied or empty`);
    }
}

function validateVarIsUrl(varName) {
    if (!validator.isURL(process.env[varName], { require_tld: false })) {
        logAndThrowError(`Environment variable ${varName} with invalid url: ${process.env[varName]}`);
    }
}

function validateVarIsJson(varName) {
    if (!validator.isJSON(process.env[varName])) {
        logAndThrowError(`Environment variable ${varName} with invalid json: ${process.env[varName]}`);
    }
}

if (process.env.NODE_ENV === 'test') {
    logger.warn('Service is up in TEST mode!');
} else {
    logger.debug('Validating ENV vars');

    validateVarNotEmpty('DATABRICKS_WORKSPACE_URL');
    validateVarIsUrl('DATABRICKS_WORKSPACE_URL');

    validateVarNotEmpty('DATABRICKS_AUTH_TOKEN');
    validateVarNotEmpty('DATABRICKS_CLUSTER_ID');
    validateVarNotEmpty('DATABRICKS_RUN_TIMEOUT');

    validateVarNotEmpty('DATABRICKS_TYPE_MAPPING');
    validateVarIsJson('DATABRICKS_TYPE_MAPPING');
}
