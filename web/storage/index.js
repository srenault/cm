const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('/Users/sre/data/srebox/credit_mutuel/stats/cm.db');

function formatDate(date) {
  return date.format('YYYY-MM-DD');
}

function averageBalancePerAccount({ dateUpper }) {
  return new Promise((resolve, reject) => {
    db.serialize(function() {
      const query = `SELECT AVG(balance) as balance, account_id, day FROM balances
                   WHERE date < "${formatDate(dateUpper)}"
                   GROUP BY day, account_id ORDER BY date;`;

      db.all(query, (err, balances) => {
        if (err) {
          reject(err);
        } else {
          resolve(balances);
        }
      })
    });
  });
}

function balancePerAccountBetween({ dateLowerIn, dateUpperIn }) {
  return new Promise((resolve, reject) => {
    db.serialize(function() {
      const query = `SELECT account_id, balance, date FROM balances
                   WHERE date BETWEEN "${formatDate(dateLowerIn)}" AND "${formatDate(dateUpperIn)}"
                   ORDER BY date;`;

      db.all(query, (err, balances) => {
        if (err) {
          reject(err);
        } else {
          resolve(balances);
        }
      })
    });
  });
}

function balancePerAccountAt({ date }) {
  return new Promise((resolve, reject) => {
    db.serialize(function() {
      const query = `SELECT account_id, balance, date FROM balances
                   WHERE date = "${formatDate(date)}"
                   ORDER BY date;`;

      db.all(query, (err, balances) => {
        if (err) {
          reject(err);
        } else {
          resolve(balances);
        }
      })
    });
  });
}

function balancePerAccountIn({ dates }) {
  return new Promise((resolve, reject) => {
    db.serialize(function() {
      const query = `SELECT SUM(balance) as totalAmount, date FROM balances
                   WHERE date IN (${dates.map(date => `"${formatDate(date)}"`).join(', ')})
                   GROUP BY date
                   ORDER BY date;`;

      db.all(query, (err, balances) => {
        if (err) {
          reject(err);
        } else {
          resolve(balances);
        }
      })
    });
  });
}

module.exports = {
  averageBalancePerAccount,
  balancePerAccountBetween,
  balancePerAccountAt,
  balancePerAccountIn,
};
