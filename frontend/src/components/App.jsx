// src/components/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CategoryTabs from './CategoryTabs';
import PizzaCustomization from './PizzaCustomization';
import { CartProvider } from '../context/CartContext'; // Import CartProvider
import Navbar from './Navbar'; // Import Navbar

function App() {
  return (
    <CartProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<CategoryTabs />} />
          <Route path="/customize-pizza/:id" element={<PizzaCustomization />} />
        </Routes>
      </Router>
    </CartProvider>
  );
}

export default App;
