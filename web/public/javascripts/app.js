(() => {

  // insert into balances values('3719100010983402#31#5#2018', "3719100010983402", "2018-05-31", 2018, 5, 31, 1280);
  // insert into balances values('3719100010480201#31#5#2018', "3719100010480201", "2018-05-31", 2018, 5, 31, 524.85);
  // insert into balances values('3719100010480102#31#5#2018', "3719100010480102", "2018-05-31", 2018, 5, 31, 1512.86);
  // insert into balances values('3719100010480101#31#5#2018', "3719100010480101", "2018-05-31", 2018, 5, 31, 1974.45);
  // insert into balances values('3719100010480004#31#5#2018', "3719100010480004", "2018-05-31", 2018, 5, 31, 6296.62);
  // insert into balances values('3719100010480003#31#5#2018', "3719100010480003", "2018-05-31", 2018, 5, 31, 8922.68);
  // insert into balances values('3719100010480002#31#5#2018', "3719100010480002", "2018-05-31", 2018, 5, 31, 324.58);
  // insert into balances values('3719100010480001#31#5#2018', "3719100010480001", "2018-05-31", 2018, 5, 31, 4129.40);

// insert into balances values('3719100010983402#30#4#2018', "3719100010983402", "2018-04-30", 2018, 4, 30, 245);
// insert into balances values('3719100010480201#30#4#2018', "3719100010480201", "2018-04-30", 2018, 4, 30, 73.27);
// insert into balances values('3719100010480102#30#4#2018', "3719100010480102", "2018-04-30", 2018, 4, 30, 2237.46);
// insert into balances values('3719100010480101#30#4#2018', "3719100010480101", "2018-04-30", 2018, 4, 30, 1755.48);
// insert into balances values('3719100010480004#30#4#2018', "3719100010480004", "2018-04-30", 2018, 4, 30, 6386.52);
// insert into balances values('3719100010480003#30#4#2018', "3719100010480003", "2018-04-30", 2018, 4, 30, 8822.68);
// insert into balances values('3719100010480002#30#4#2018', "3719100010480002", "2018-04-30", 2018, 4, 30, 324.58);
// insert into balances values('3719100010480001#30#4#2018', "3719100010480001", "2018-04-30", 2018, 4, 30, 822.10);

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

  function f(balances, computeValue) {
    const balanceGroupedByAccount = R.groupBy(balance => balance.account_id, balances);
    return Object.entries(balanceGroupedByAccount).map(([accountId, balances]) => {
      const accountName = ACCOUNTS[accountId];
      const values = sortBalances(balances).map(balance => {
        return computeValue(balance);
      });
      return [accountName].concat(values);
    });
  }

  function getDateLabels(balances) {
    return R.uniq(balances.map(balance => balance.date))
      .sort((sdateA, sdateB) => {
        const dateA = new Date(sdateA);
        const dateB = new Date(sdateB);
        return dateA.getTime() - dateB.getTime();
      });
  }

  function sortBalances(balances) {
    return balances.sort((balanceA, balanceB) => {
      const dateA = new Date(balanceA.date);
      const dateB = new Date(balanceB.date);
      return dateA.getTime() - dateB.getTime();
    });
  }

  const hiddenAccounts = Object.entries(ACCOUNTS)
        .filter(([id, ]) => id !== '3719100010480201')
        .map(([, label]) => label);

  window.CM = {
    buildMonthlyOverviewChart(elSelector, monthlyBalances, startingBalance) {
      const startingBalanceByAccountId = startingBalance.reduce((acc, balance) => {
        acc[balance.account_id] = balance;
        return acc;
      }, {});

      const dateLabels = R.uniq(monthlyBalances.map(balance => balance.date));
      const labels = [['x'].concat(dateLabels)];
      const values = f(monthlyBalances, balance => {
        return balance.balance;
      });
      const columns = labels.concat(values);
      const chart = c3.generate({
        bindto: elSelector,
        data: {
          x: 'x',
          columns,
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

    buildAverageOverviewChart(elSelector, averageBalances) {
      const dateLabels = R.uniq(averageBalances.map(balance => balance.day)).sort((sdayA, sdayB) => {
        return parseInt(sdayA, 10) - parseInt(sdayB, 10)
      });
      const labels = [['x'].concat(dateLabels)];
      const values = f(averageBalances, balance => balance.balance);
      const columns = labels.concat(values);

      const chart = c3.generate({
        bindto: elSelector,
        data: {
          x: 'x',
          columns,
          hide: hiddenAccounts,
        },
      });
    },

    buildTotalBalanceChart(elSelector, totalBalances) {
      const dateLabels = totalBalances.map(balance => balance.date);
      const labels = [['x'].concat(dateLabels)];
      const values = [['Total Balance'].concat(totalBalances.map(balance => balance.totalAmount))];
      const columns = labels.concat(values);

      const chart = c3.generate({
        bindto: elSelector,
        data: {
          x: 'x',
          columns,
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
