

const express = require('express');
const mysql = require('mysql');
const Memcached = require('memcached');

const app = express();
const PORT = 3000;

// Create MySQL connection
const db = mysql.createConnection({
    host: 'db01',    // Replace with your SQL server host
    user: 'admin',        // Replace with your SQL username
    password: 'admin123',    // Replace with your SQL password
    database: 'personal_finance'      // Use the database you created
});

// Connect to MySQL
db.connect((err) => {
    if (err) throw err;
    console.log('Connected to MySQL database.');
});

// Create Memcached client
const memcached = new Memcached('mc01:11211'); // Replace with your Memcache server details

// Sample endpoint to get transactions
app.get('/transactions', (req, res) => {
    const cacheKey = 'transactions';

    // Check if data exists in Memcache
    memcached.get(cacheKey, (err, data) => {
        if (data) {
            // Data is in cache, return it
            return res.json(JSON.parse(data));
        } else {
            // Data is not in cache, fetch from SQL
            db.query('SELECT * FROM Transactions', (err, results) => {
                if (err) throw err;

                // Store the results in Memcache for next time
                memcached.set(cacheKey, JSON.stringify(results), 3600, (err) => {
                    if (err) throw err;
                });

                // Return the results
                return res.json(results);
            });
        }
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
