import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';


const QuizApp = () => {
  // State variables
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [score, setScore] = useState(0);

  // Fetch questions from the backend when the component mounts
  useEffect(() => {
    axios.get('http://localhost:5000/questions')
      .then(response => {
        console.log('Questions:', response.data);
        setQuestions(response.data);
        setAnswers(Array(response.data.length).fill(''));
      })
      .catch(error => console.error(error));
  }, []);

  // Handle answer change
  const handleAnswerChange = (event, questionIndex) => {
    const newAnswers = [...answers];
    newAnswers[questionIndex] = event.target.value;
    setAnswers(newAnswers);
  };

  // Handle form submission
  const handleSubmit = () => {
    axios.post('http://localhost:5000/submit-answers', { answers }) // URL with correct port
      .then(response => {
        console.log(response.data);
        // Process response, set score, show results, etc.
      })
      .catch(error => console.error(error));
  };

  return (
    <div className="quiz-container">
      {/* Render questions and input fields */}
      {questions.map((question, questionIndex) => (
        <div key={questionIndex} className="question">
          <p>{question.question}</p> {/* 'question' is the column name in the table */}
          <input
            type="text"
            value={answers[questionIndex]}
            onChange={(event) => handleAnswerChange(event, questionIndex)}
          />
        </div>
      ))}
      {/* Button to submit answers */}
      <button onClick={handleSubmit}>Submit Answers</button>
      {/* Display results */}
      {showResults && (
        <div className="results">
          <p>Your score: {score}</p>
          {/* Can add more results Details */}
        </div>
      )}
    </div>
  );
};

export default QuizApp;
