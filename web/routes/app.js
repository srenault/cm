const express = require('express');
const router = express.Router();
const sqlite3 = require('sqlite3').verbose();
const moment = require('moment');
const storage = require('../storage');

router.get('/', (req, res, next) => {
  const startOfMonth = moment().startOf('month');
  const endOfMonth = moment().endOf('month');
  const endOfLastMonth = moment().subtract(1, 'month').endOf('month');
  const lastThreeMonths = (function f(acc, max) {
    if (acc.length < max) {
      const d = acc[0].clone();
      return f([d.subtract(1, 'month')].concat(acc), max);
    } else {
      return acc;
    }
  })([endOfLastMonth], 3);
  console.log(lastThreeMonths);
  storage.balancePerAccountIn({ dates: lastThreeMonths }, (err, lastThreeMonthBalances) => {
    storage.balancePerAccountAt({ date: endOfLastMonth }, (err, startingBalances) => {
      storage.averageBalancePerAccount({ dateUpper: startOfMonth }, (err, averageBalances) => {
        storage.balancePerAccountBetween({ dateLowerIn: startOfMonth, dateUpperIn: endOfMonth }, (err, monthlyBalances) => {
          res.render('index', { averageBalances,  monthlyBalances, startingBalances, lastThreeMonthBalances });
        });
      });
    });
  });
});

module.exports = router;
