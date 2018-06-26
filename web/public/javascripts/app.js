(() => {

  const ACCOUNTS = {
    3719100010480001: 'Compte courant Sébastien',
    3719100010480002: 'CEL Sébastien',
    3719100010480003: 'PEL Sébastien',
    3719100010480004: 'LDD Sébastien',
    3719100010480101: 'Compte courant Pauline',
    3719100010480102: 'LDD Pauline',
    3719100010480201: 'Compte courant Sébastien & Pauline',
    3719100010983402: 'Livret Bleu Léon'
  };

  // insert into balances values('3719100010983402#31#5#2018', "3719100010983402", "2018-05-31", 2018, 5, 31, 1280);
  // insert into balances values('3719100010480201#31#5#2018', "3719100010480201", "2018-05-31", 2018, 5, 31, 524.85);
  // insert into balances values('3719100010480102#31#5#2018', "3719100010480102", "2018-05-31", 2018, 5, 31, 1512.86);
  // insert into balances values('3719100010480101#31#5#2018', "3719100010480101", "2018-05-31", 2018, 5, 31, 1974.45);
  // insert into balances values('3719100010480004#31#5#2018', "3719100010480004", "2018-05-31", 2018, 5, 31, 6296.62);
  // insert into balances values('3719100010480003#31#5#2018', "3719100010480003", "2018-05-31", 2018, 5, 31, 8922.68);
  // insert into balances values('3719100010480002#31#5#2018', "3719100010480002", "2018-05-31", 2018, 5, 31, 324.58);
  // insert into balances values('3719100010480001#31#5#2018', "3719100010480001", "2018-05-31", 2018, 5, 31, 4129.40)
  ;

  function buildDateLabels(averageBalances, monthlyBalances) {
    const x = averageBalances.map(averageBalance => averageBalance.date)
    const y = monthlyBalances.map(balance => balance.date)
    return R.uniq(x.concat(y));
  }

  window.CM = {
    buildMonthlyOverviewChart(elSelector, averageBalances, monthlyBalances, startingBalance) {
      const startingBalanceByAccountId = startingBalance.reduce((acc, balance) => {
        acc[balance.account_id] = balance, {};
        return acc;
      }, {});
      const dateLabels = buildDateLabels(averageBalances, monthlyBalances);

      function f(balances) {
        const balanceGroupedByAccount = R.groupBy(balance => balance.account_id, balances);
        return Object.entries(balanceGroupedByAccount).map(([accountId, balances]) => {
          const accountName = ACCOUNTS[accountId];
          const sortedBalances = R.sortBy(balance => dateLabels.indexOf(balance.date), balances);
          const values = sortedBalances.map(balance => {
            const startingBalance = startingBalanceByAccountId[balance.account_id];
            return balance.balance;
          });
          return [accountName].concat(values);
        });
      }

      const hiddenAccounts = Object.entries(ACCOUNTS)
            .filter(([id, ]) => id !== '3719100010480201')
            .map(([, label]) => label);

      const chart = c3.generate({
        bindto: elSelector,
        data: {
          x: 'x',
          columns: [['x'].concat(dateLabels)].concat(f(monthlyBalances)),
          hide: hiddenAccounts,
        },
        axis: {
          x: {
            type: 'timeseries',
            tick: {
              format: '%Y-%m-%d'
            }
          }
        }
      });
    },

    build(elSelector, lastThreeMonthBalances) {
      const dateLabels = lastThreeMonthBalances.map(balance => balance.date);
      const balanceValues = lastThreeMonthBalances.map(balance => balance.totalAmount);
      const chart = c3.generate({
        bindto: elSelector,
        data: {
          x: 'x',
          columns: [['x'].concat(dateLabels)].concat([['Total Balance'].concat([balanceValues])]),
          type: 'bar',
        },
        bar: {
          width: {
            ratio: 0.5
          }
        },
        axis: {
          x: {
            type: 'timeseries',
            tick: {
              format: '%Y-%m-%d'
            }
          }
        }
      });
    }
  }; 
})();
