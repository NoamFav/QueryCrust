// src/components/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CategoryTabs from './CategoryTabs';
import PizzaCustomization from './PizzaCustomization';
import { CartProvider } from '../context/CartContext'; // Import CartProvider
import Navbar from './NavBar'; // Import Navbar
import Cart from './Cart'; // Import Cart

function App() {
  return (
    <CartProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<CategoryTabs />} />
          <Route path="/customize-pizza/:id" element={<PizzaCustomization />} />
          <Route path="/cart" element={<Cart />} />
        </Routes>
      </Router>
    </CartProvider>
  );
}

export default App;
