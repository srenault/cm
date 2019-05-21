const express = require('express');
const router = express.Router();
const sqlite3 = require('sqlite3').verbose();
const moment = require('moment');
const storage = require('../storage');
const TotalBalancesGraph = require('../graph/totalBalances');
const MonthlyOverviewGraph = require('../graph/monthlyOverview');
const AvertageMonthlyOverviewGraph = require('../graph/averageMonthlyOverview');

router.get('/', (req, res, next) => {
  TotalBalancesGraph.getLastMonths(12).then((totalBalances) => {
    return MonthlyOverviewGraph.getCurrentMonth().then(({ startingBalances, monthlyBalances }) => {
      return MonthlyOverviewGraph.getLastMonth().then(({ monthlyBalances: lastMonthBalances, startingBalances: lastMonthStartingBalances }) => {
        return AvertageMonthlyOverviewGraph.get().then((averageBalances) => {
          res.render('index', {
            averageBalances,
            monthlyBalances,
            startingBalances,
            lastMonthBalances,
            lastMonthStartingBalances,
            totalBalances
          });
        });
      });
    });
  }).catch(next);
});

module.exports = router;
