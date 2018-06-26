const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('/Users/sre/data/srebox/credit_mutuel/stats/cm.db');

function formatDate(date) {
  return date.format('YYYY-MM-DD');
}

function averageBalancePerAccount({ dateUpper }, callback) {
  db.serialize(function() {
    const query = `SELECT AVG(balance) as balance, date, account_id, day FROM balances
                   WHERE date < "${formatDate(dateUpper)}"
                   GROUP BY day, account_id ORDER BY date;`;

    db.all(query, (err, balances) => {
      callback && callback(err, balances);
    })
  });
}

function balancePerAccountBetween({ dateLowerIn, dateUpperIn }, callback) {
  db.serialize(function() {
    const query = `SELECT account_id, balance, date FROM balances
                   WHERE date BETWEEN "${formatDate(dateLowerIn)}" AND "${formatDate(dateUpperIn)}"
                   ORDER BY date;`;

    db.all(query, (err, balances) => {
      callback && callback(err, balances);
    })
  });
}

function balancePerAccountAt({ date }, callback) {
  db.serialize(function() {
    const query = `SELECT account_id, balance, date FROM balances
                   WHERE date = "${formatDate(date)}"
                   ORDER BY date;`;

    db.all(query, (err, balances) => {
      callback && callback(err, balances);
    })
  });
}

function balancePerAccountIn({ dates }, callback) {
  db.serialize(function() {
    const query = `SELECT SUM(balance) as totalAmount, date FROM balances
                   WHERE date IN (${dates.map(date => `"${formatDate(date)}"`).join(', ')})
                   GROUP BY date
                   ORDER BY date;`;

    db.all(query, (err, balances) => {
      callback && callback(err, balances);
    })
  });
}

module.exports = {
  averageBalancePerAccount,
  balancePerAccountBetween,
  balancePerAccountAt,
  balancePerAccountIn,
};
