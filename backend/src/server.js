const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const app = express();

app.use(bodyParser.json());

// MySQL connection
const db = mysql.createConnection({
  host: 'localhost',
  port: 3306,
  user: 'root',
  password: 'Abilaash13',
  database: 'lumoslore'
});

db.connect((err) => {
  if (err) throw err;
  console.log('Connected to MySQL database');
});

// API endpoint to fetch questions and correct answers from the database
app.get('/data', (req, res) => {
  // Query to fetch data from a table (replace 'your_table' with your actual table name)
  const query = 'SELECT * FROM questions';

  // Execute the query
  db.query(query, (err, results) => {
    if (err) {
      console.error('Error fetching data from MySQL:', err);
      return res.status(500).send('Internal server error');
    }
    res.json(results); // Send the fetched data as JSON response
  });
});

// API endpoint to store user answers in the database
app.post('/submit-answers', (req, res) => {
  const { user_answers } = req.body;

  const values = user_answers.map(answer => [answer.question_id, answer.user_answer]);
  
  db.query('INSERT INTO user_answers (question_id, user_answer) VALUES ?', [values], (err, result) => {
    if (err) {
      console.error("Error inserting answers:", err);
      return res.status(500).json({ error: "Internal server error" });
    }
    res.sendStatus(200);
  });
});


const port = 5001;

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

