import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import "./components/components/css/index.css"

const root = ReactDOM.createRoot(document.getElementById('root')); // Create the root
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);