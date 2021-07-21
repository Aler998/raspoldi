const express = require('express')
require('dotenv').config()
const mysql = require('mysql2')
const cors = require('cors')
const mergeAndSort = require('./utils/mergeAndSort')
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

app.get('/delete/:id', (req, res) => {
    console.log(req.params.id)
    try {
        const query = "DELETE FROM transazioni WHERE id = " + req.params.id
        connection.query(query, (error, result, fields) => {
            if (error) throw error
            res.status(200).send('ok')
        })
    } catch (error) {
        try {
            const query = "DELETE FROM transazioni_telegram WHERE id = " + req.params.id
            connection.query(query, (error, result, fields) => {
                if (error) throw error
                res.status(200).send('ok')
            })
        } catch (error) {
            res.status(404).send('This id does not exist')
        }
        
    }

    
})

app.get('/transazioni', (req, res) => {

    const query = "SELECT * FROM (SELECT * FROM transazioni \
                                    UNION \
                                    SELECT update_id as id, tipo, euro, descrizione, created_at, categoria FROM transazioni_telegram) AS tabella \
                    ORDER BY created_at DESC \
                    LIMIT 11"

    connection.query(query, (error, result, fields) => {
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

app.get('/categoria_mensile', (req, res) => {
    const today = new Date()
    const query = "SELECT categoria, SUM(euro) as total FROM transazioni WHERE tipo = 0 AND created_at BETWEEN '" + String(today.getFullYear()) + "-" + String(today.getMonth() + 1) + "-01' AND '" + + String(today.getFullYear()) + "-" + String(today.getMonth() + 1) + "-31' GROUP BY categoria"
    connection.query(query, (error, result, fields) => {
        if (error) throw error
        res.send(result)
    })
})

app.listen(5000, () => {
    console.log(`Example app listening at http://localhost:5000`)
})