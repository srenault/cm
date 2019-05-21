const moment = require('moment');
const storage = require('../storage');

function rewindEndOfMonthUntil(n) {
  const endOfLastMonth = moment().date(25).subtract(1, 'month')//.endOf('month');
  //const endOfLastMonth = moment().subtract(1, 'month').endOf('month');
  return (function step(acc, max) {
    if (acc.length < max) {
      const d = acc[0].clone();
      const endOfMonth = d.subtract(1, 'month')//.endOf('month');
      return step([endOfMonth].concat(acc), max);
    } else {
      return acc;
    }
  })([endOfLastMonth], n);
}

module.exports = {
  getLastMonths(n) {
    const dates = rewindEndOfMonthUntil(n);
    return storage.balancePerAccountIn({ dates });
  },
};
