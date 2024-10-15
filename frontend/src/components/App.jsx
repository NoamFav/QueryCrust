// src/components/App.jsx
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './Login'; 
import Register from './Register';
import Cart from './Cart';
import NavBar from './NavBar';
import CategoryTabs from './CategoryTabs';
import { CartProvider } from '../context/CartContext';
import { OrderProvider } from '../context/OrderContext';
import { AdminOrderProvider } from '../context/AdminOrderContext';
import PizzaCustomization from './PizzaCustomization';
import Checkout from './Checkout';
import Order from './Order';
import Admin from './AdminTab';
import AdminRecords from './AdminRecords';
import PersonalDetails from './PersonalInfo';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);

  return (
  <CartProvider isAuthenticated={isAuthenticated}>
      <OrderProvider isAuthenticated={isAuthenticated}>
        <AdminOrderProvider isAuthenticated={isAuthenticated}>
        <Router>
          <div>
            {isAuthenticated && <NavBar  isAdmin={isAdmin} />}
            
            <Routes>
              <Route path="/" element={
                  isAuthenticated ? <Navigate to="/menu" /> : <Login setIsAuthenticated={setIsAuthenticated} setIsAdmin={setIsAdmin}/>
              } />

              <Route path="/register" element={
                isAuthenticated ? <Navigate to="/main" /> : <Register />
              } />

              <Route path="/personal" element={
                  isAuthenticated ? <PersonalDetails /> : <Navigate to="/" />
              } />

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

              <Route path="/admin/records" element={
                  isAuthenticated && isAdmin ? <AdminRecords /> : <Navigate to="/" />
              } />

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
