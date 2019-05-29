const appInsights = require('applicationinsights');
const logger = require('./logging');

// Setup Application Insights
if (process.env.APP_INSIGHTS_INSTRUMENTATION_KEY) {
    appInsights
        .setup(process.env.APP_INSIGHTS_INSTRUMENTATION_KEY)
        .setAutoDependencyCorrelation(true)
        .setAutoCollectRequests(true)
        .setAutoCollectPerformance(true)
        .setAutoCollectExceptions(true)
        .setAutoCollectDependencies(true)
        .setAutoCollectConsole(true)
        .setUseDiskRetryCaching(true);

    // We need to set the role to see the correct name in the map
    if (process.env.SERVICE_NAME) {
        appInsights.defaultClient.context.tags['ai.cloud.role'] = process.env.SERVICE_NAME;
    } else {
        logger.warn('Environment variable SERVICE_NAME does not exist or empty!');
    }

    if (process.env.NODE_ENV === 'test') {
        // We don't need to send telemetry while testing
        appInsights.defaultClient.config.disableAppInsights = true;
    } else {
        // Start Application Insights telemetry
        appInsights.start();
    }
} else {
    logger.warn('Environment variable APP_INSIGHTS_INSTRUMENTATION_KEY does not exist or empty!');
}
