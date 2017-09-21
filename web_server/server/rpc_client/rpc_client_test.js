var client = require('./rpc_client');

// invoke "getNewsSummariesForUser"
client.getNewsSummariesForUser('test_user', 1, function (response) {
    console.assert(response != null);
});

// invoke "logNewsClickForUser"
client.logNewsClickForUser('test_user', 'test_news');