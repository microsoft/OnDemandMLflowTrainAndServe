const rp = require('request-promise');
const logger = require('../logging');

const RUN_STATUS = {
    PENDING: 'pending',
    RUNNING: 'running',
    COMPLETED: 'completed',
};

const databricksWorkspaceUrl = process.env.DATABRICKS_WORKSPACE_URL;
const clusterId = process.env.DATABRICKS_CLUSTER_ID;
const runTimeout = process.env.DATABRICKS_RUN_TIMEOUT;
const modelTypes = JSON.parse(process.env.DATABRICKS_TYPE_MAPPING);

const defaultHeaders = {
    Accept: 'application/json',
    'Accept-Charset': 'utf-8',
    Authorization: `Bearer ${process.env.DATABRICKS_AUTH_TOKEN}`,
};

function getNotebookPath(modelType) {
    if (modelTypes[modelType]) {
        return modelTypes[modelType];
    }
    throw new Error('Invalid modelType: ', modelType);
}

function startCluster() {
    const options = {
        url: `${databricksWorkspaceUrl}/api/2.0/clusters/start`,
        method: 'POST',
        headers: defaultHeaders,
        json: {
            cluster_id: clusterId,
        },
    };
    return rp(options);
}

function getClusterInfo() {
    const options = {
        url: `${databricksWorkspaceUrl}/api/2.0/clusters/get?cluster_id=${clusterId}`,
        method: 'GET',
        headers: defaultHeaders,
    };
    return rp(options);
}

async function initCluster() {
    const clusterInfo = JSON.parse(await getClusterInfo());
    const clusterState = clusterInfo.state;
    logger.info(`Current cluster state is: ${clusterState}`);

    if (clusterState === 'TERMINATED') {
        logger.info('Starting cluster');
        startCluster();
    }
    return clusterState;
}

function submitNotebookRun(notebookPath, parameters) {
    const options = {
        url: `${databricksWorkspaceUrl}/api/2.0/jobs/runs/submit`,
        method: 'POST',
        headers: defaultHeaders,
        json: {
            run_name: `TrainingRun_${new Date().getTime()}`,
            existing_cluster_id: clusterId,
            notebook_task: {
                notebook_path: notebookPath,
                base_parameters: parameters,
            },
            timeout_seconds: runTimeout,
        },
    };
    return rp(options);
}

async function getRun(runId) {
    const options = {
        url: `${databricksWorkspaceUrl}/api/2.0/jobs/runs/get?run_id=${runId}`,
        method: 'GET',
        headers: defaultHeaders,
    };
    return rp(options);
}

/*
"state": {
    "life_cycle_state": "TERMINATED",
    "result_state": "SUCCESS",
    "state_message": ""
}
"state": {
    "life_cycle_state": "RUNNING",
    "state_message": "In run"
}
*/
function calcStatus(runState) {
    const status = {
        state: '',
        message: runState.state_message,
    };
    switch (runState.life_cycle_state) {
    case 'PENDING':
        status.state = RUN_STATUS.PENDING;
        break;

    case 'RUNNING':
        status.state = RUN_STATUS.RUNNING;
        break;

    default:
        status.state = RUN_STATUS.COMPLETED;
    }
    return status;
}

async function submitTrainingRequest(modelType, parameters) {
    // Get the notebook path according to the modelType:
    const notebookPath = getNotebookPath(modelType);

    // Make sure to start the cluster if it is not running:
    initCluster();

    try {
        // Run the notebook with the received parameters:
        const dbResponse = await submitNotebookRun(notebookPath, parameters);
        return dbResponse.run_id;
    } catch (err) {
        logger.error(`Error in submitting a notebook run: ${err.message}`);
        throw err;
    }
}

async function getRunStatus(runId) {
    try {
        const dbResponse = JSON.parse(await getRun(runId));
        const status = calcStatus(dbResponse.state);
        return status;
    } catch (err) {
        logger.error(`Error in getting run: ${err.message}`);
        throw err;
    }
}

module.exports.submitTrainingRequest = submitTrainingRequest;
module.exports.getRunStatus = getRunStatus;
