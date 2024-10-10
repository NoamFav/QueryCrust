// src/components/App.jsx
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './Login'; // Login Component
import Register from './Register'; // Registration Component
import Cart from './Cart'; // Example of your main app pages
import NavBar from './NavBar'; // Navigation Bar
import CategoryTabs from './CategoryTabs'; // Main content page
import { CartProvider } from '../context/CartContext'; // Cart Context
import { OrderProvider } from '../context/OrderContext'; // Order Context
import { AdminOrderProvider } from '../context/AdminOrderContext'; // Admin Context
import PizzaCustomization from './PizzaCustomization';
import Checkout from './Checkout';
import Order from './Order';
import Admin from './AdminTab';

function App() {
  // State to track if the user is authenticated
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);

  return (
  <CartProvider isAuthenticated={isAuthenticated}>
      <OrderProvider isAuthenticated={isAuthenticated}>
        <AdminOrderProvider isAuthenticated={isAuthenticated}>
        <Router>
          <div>
            {/* If authenticated, show the Navbar */}
            {isAuthenticated && <NavBar  isAdmin={isAdmin} />}
            
            <Routes>
              {/* Login Route */}
              <Route path="/" element={
                  isAuthenticated ? <Navigate to="/menu" /> : <Login setIsAuthenticated={setIsAuthenticated} setIsAdmin={setIsAdmin}/>
              } />

              {/* Register Route */}
              <Route path="/register" element={
                isAuthenticated ? <Navigate to="/main" /> : <Register />
              } />

              {/* Main App Pages - Protected Routes */}
              <Route path="/menu" element={
                  isAuthenticated ? <CategoryTabs  isAdmin={isAdmin}/> : <Navigate to="/" />
              } />

              <Route path="/menu/customize-pizza/:id" element={
                isAuthenticated ? <PizzaCustomization /> : <Navigate to="/" />
              } />

              <Route path="/cart" element={
                  isAuthenticated ? <Cart /> : <Navigate to="/" />
              } />

              <Route path="/checkout" element={
                  isAuthenticated ? <Checkout /> : <Navigate to="/" />
              } />
                
              <Route path="/orders" isAdmin={isAdmin} element={
                  isAuthenticated ? <Order /> : <Navigate to="/" />
              } />

              <Route path="/admin" element={
                  isAuthenticated && isAdmin ? <Admin /> : <Navigate to="/" />
              } />

              {/* Catch-all Route */}
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </div>
        </Router>
        </AdminOrderProvider>
      </OrderProvider>
  </CartProvider>
  );
}

export default App;
