const express = require('express')
require('dotenv').config()
const mysql = require('mysql2')
const cors = require('cors')
const app = express()

app.use(cors())

const connection = mysql.createConnection({
    host     : process.env.DB_HOST,
    user     : process.env.DB_USER,
    password : process.env.DB_PASSWORD,
    database : process.env.DB_NAME
})

connection.connect()

app.get('/', (req, res) => {
    res.send('hello world')
})

app.get('/transazioni', (req, res) => {
    connection.query('SELECT * FROM transazioni ORDER BY created_at DESC LIMIT 11', (error, result, fields) => {
        if (error) throw error
        res.send(result)
    })
})

app.get('/totale_mensile', (req, res) => {
    const today = new Date()
    const query = "SELECT tipo, SUM(euro) as total FROM transazioni WHERE created_at BETWEEN '" + String(today.getFullYear()) + "-" + String(today.getMonth() + 1) + "-01' AND '" + + String(today.getFullYear()) + "-" + String(today.getMonth() + 1) + "-31' GROUP BY tipo"
    connection.query(query, (error, result, fields) => {
        if (error) throw error
        res.send(result)
    })
})

app.listen(5000, () => {
    console.log(`Example app listening at http://localhost:5000`)
})