const mysql = require('mysql2/promise');
const fs = require('fs');

async function initDb() {
    try {
        const connection = await mysql.createConnection({
            host: 'localhost',
            user: 'root',
            password: '',
            multipleStatements: true
        });

        const sql = fs.readFileSync('setup.sql', 'utf8');
        await connection.query(sql);
        console.log("Database initialized successfully.");
        await connection.end();
    } catch (error) {
        console.error("Failed to initialize DB:", error);
    }
}

initDb();
