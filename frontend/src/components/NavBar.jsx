// src/components/Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';

const Navbar = () => {
  const { cartItems } = useCart();

  // Calculate total quantity for cart badge
  const totalQuantity = cartItems.reduce((acc, item) => acc + item.quantity, 0);

return (
  <nav className="bg-red-600 p-4 flex items-center justify-between">
    <div className="text-white text-xl font-bold">
      QueryCrust    
    </div>
    <div className="flex items-center space-x-4">
      <Link to="/" className="text-white hover:text-gray-200">
        Menu
      </Link>
      <Link to="/cart" className="relative text-white hover:text-gray-200">
        Cart
        {totalQuantity > 0 && (
          <span className="absolute -top-2 -right-3 bg-red-500 text-white rounded-full text-xs w-5 h-5 flex items-center justify-center">
            {totalQuantity}
          </span>
        )}
      </Link>
    </div>  
  </nav>
)};

export default Navbar;
