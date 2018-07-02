const moment = require('moment');
const storage = require('../storage');

function get(balanceBetweenDates, startingDateBalance) {
  return storage.balancePerAccountBetween({ dateLowerIn: balanceBetweenDates.start, dateUpperIn: balanceBetweenDates.end }).then((monthlyBalances) => {
    return storage.balancePerAccountAt({ date: startingDateBalance }).then((startingBalances) => {
      return { monthlyBalances, startingBalances };
    });
  });
}

function getCurrentMonth() {
  const startOfMonth = moment().startOf('month');
  const endOfMonth = moment().endOf('month');
  const endOfLastMonth = moment().subtract(1, 'month').endOf('month');
  const balanceBetweenDates = { start: startOfMonth, end: endOfMonth };
  return get(balanceBetweenDates, endOfLastMonth);
}

function getLastMonth() {
  const lastMonth = moment().subtract(1, 'month');
  const startOfMonth = lastMonth.clone().startOf('month');
  const endOfMonth = lastMonth.clone().endOf('month');
  const endOfLastMonth = lastMonth.clone().subtract(1, 'month').endOf('month');
  const balanceBetweenDates = { start: startOfMonth, end: endOfMonth };
  return get(balanceBetweenDates, endOfLastMonth);
}

module.exports = {
  getCurrentMonth,
  getLastMonth,
};
