const router = require('express').Router();
const trainingModule = require('../modules/training-module');

const HTTP_STATUS_CODES = {
    BAD_REQUEST: 400,
    INTERNAL_ERROR: 500,
};

function getRequestModelType(req) {
    return req.body.modelType;
}

function getRequestParameters(req) {
    return req.body.parameters ? req.body.parameters : {};
}

async function submitTrainingRequest(modelType, parameters) {
    const trainingRequest = await trainingModule.submitTrainingRequest(modelType, parameters);
    return trainingRequest;
}

async function getRunStatus(runId) {
    const runStatus = await trainingModule.getRunStatus(runId);
    return runStatus;
}

async function newTrainingReq(req, res) {
    const modelType = getRequestModelType(req);
    const parameters = getRequestParameters(req);

    if (!modelType) {
        // If modelType does not exist in the request, return Bad Request error:
        res.status(HTTP_STATUS_CODES.BAD_REQUEST).send(
            'modelType must be specified in the request body',
        );
        return;
    }

    try {
        // Send a request to TrainingModule for a new training, and receive a runId:
        const runId = await submitTrainingRequest(modelType, parameters);

        // Return response with runId to the client:
        res.send({
            runId,
        });
    } catch (err) {
        // In case of error, return error response to the client:
        res.status(HTTP_STATUS_CODES.INTERNAL_ERROR).send(
            `Failed to request a model training. ${err.message}`,
        );
    }
}

async function getRunStatusReq(req, res) {
    const runId = req.params.id;
    if (!runId) {
        res.status(HTTP_STATUS_CODES.BAD_REQUEST).send(
            'runId must be specified in the path parameters',
        );
        return;
    }

    try {
        // Send a request to TrainingModule to get the status of a run:
        const runStatus = await getRunStatus(runId);

        // Return the runStatus to the client:
        res.send(runStatus);
    } catch (err) {
        // In case of error, return error response to the client:
        res.status(HTTP_STATUS_CODES.INTERNAL_ERROR).send(
            `Failed to get training status. ${err.message}`,
        );
    }
}

router.post('/', newTrainingReq);
router.get('/:id', getRunStatusReq);

module.exports = router;

if (process.env.NODE_ENV === 'test') {
    module.exports.submitTrainingRequest = submitTrainingRequest;
    module.exports.getRunStatus = getRunStatus;
    module.exports.getRequestModelType = getRequestModelType;
    module.exports.getRequestParameters = getRequestParameters;
}
