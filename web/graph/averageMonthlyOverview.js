const moment = require('moment');
const storage = require('../storage');

function get() {
  const startOfMonth = moment().startOf('month');
  return storage.averageBalancePerAccount({ dateUpper: startOfMonth });
}

module.exports = {
  get,
};
