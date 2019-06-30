/* eslint-disable func-names */
/* eslint-disable no-undef */
/* eslint-disable no-unused-vars */
const proxyquire = require('proxyquire').noCallThru();
const { expect } = require('chai');
const fs = require('fs');

const trainingModuleStub = {};
const trainingRoutes = proxyquire('../app/routes/training-routes', {
    '../modules/training-module': trainingModuleStub,
});

describe('Simulation Routes Tests', () => {
    const TRAIN_REQUEST_BODY = JSON.parse(fs.readFileSync('./tests/data/train-request.json', 'utf8'));
    beforeEach(() => {
        // Stub methods:
        trainingModuleStub.submitTrainingRequest = function (modelType, parameters) {
            return new Promise((resolve, reject) => {
                resolve(10);
            });
        };
    });

    it('submitTrainingRequest() returns correct runId', async () => {
        // Stub methods:
        trainingModuleStub.submitTrainingRequest = (modelType, parameters) => new Promise(
            (resolve, reject) => {
                resolve(10);
            },
        );

        const runIdRes = await trainingRoutes.submitTrainingRequest('TYPE1', {});
        expect(runIdRes).to.equal(10);
    });

    it('getRunStatus() returns correct status', async () => {
        const status = {
            state: 'COMPLETED',
            message: 'message',
        };
        // Stub methods:
        trainingModuleStub.getRunStatus = () => new Promise((resolve) => {
            resolve(status);
        });

        const statusRes = await trainingRoutes.getRunStatus(10);
        expect(statusRes).to.equal(status);
    });

    it('getModelType() returns correct modelType value from the request body', async () => {
        const req = {
            body: TRAIN_REQUEST_BODY,
        };
        const type = trainingRoutes.getRequestModelType(req);
        expect(type).to.equal(TRAIN_REQUEST_BODY.modelType);
    });

    it('getParameters() returns correct parameters value from the request body', async () => {
        const req = {
            body: TRAIN_REQUEST_BODY,
        };
        const parameters = trainingRoutes.getRequestParameters(req);
        expect(parameters).to.equal(TRAIN_REQUEST_BODY.parameters);
    });
});
