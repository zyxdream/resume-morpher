import React, { useState } from 'react';
import 'bulma/css/bulma.min.css';

function App() {
  const [inputValue1, setInputValue1] = useState('');
  const [inputValue2, setInputValue2] = useState('');
  const [result, setResult] = useState('');

  const handleMorph = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/morph', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input1: inputValue1, input2: inputValue2 }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      setResult(data.result);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  return (
    <div className="container">
      <div className="section">
        <figure className="image ">
          <img src="resume_morpher_christmas.png" alt="Header" />
        </figure>
      </div>

      <div className="section">
        <div className="field">
          <input 
            className="input" 
            type="text" 
            placeholder="Your Resume" 
            value={inputValue1} 
            onChange={(e) => setInputValue1(e.target.value)} 
          />
        </div>
        <div className="field">
          <input 
            className="input" 
            type="text" 
            placeholder="Target Job Posting" 
            value={inputValue2} 
            onChange={(e) => setInputValue2(e.target.value)} 
          />
        </div>
        <div className="field">
          <button className="button is-primary" onClick={handleMorph}>Morph</button>
        </div>
      </div>

      <div className="section">
        <div className="content">
          <p>The morphed resume goes here.{result}</p>
        </div>
      </div>
    </div>
  );
}

export default App;
