/**
 * Created by paullichtenberger on 23.09.16.
 */
var log = require('winston');

exports.logger = new (log.Logger)({
    transports: [
        new (log.transports.File)({ filename: 'output.log' })
    ]
});