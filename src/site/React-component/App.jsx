// src/site/App.jsx
import React from 'react';
import Button from './button'; // Import your button component

const App = () => {
  return (
    <div className="p-4 bg-blue-200">
      <h1 className="text-2xl font-bold">Hello, React with Tailwind!</h1>
      <p>This is your main React application component.</p>
      <Button />
    </div>
  );
};

export default App;
