// src/site/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './component/App'; // Import your main App component
import './styles/tailwind.css'; // Import your Tailwind CSS

// Create the root and render the App component
const root = ReactDOM.createRoot(document.getElementById('app'));
root.render(
  <React.StrictMode>
    <App /> {}
  </React.StrictMode>
);
