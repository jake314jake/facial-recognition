import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Home from './Home';

function App() {
  return (
    <Router>
      <div>
        <Home />
      </div>
    </Router>
  );
}

export default App;
