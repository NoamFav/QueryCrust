// src/components/MenuItem.jsx
import React from 'react';
import { useCart } from '../context/CartContext';
import { useNavigate } from 'react-router-dom';

const MenuItem = ({ item, category, fetchMenuItems, isAdmin }) => {
  const { addToCart } = useCart();
  const navigate = useNavigate();

  const handleAddToCart = () => {
    if (category === 'pizza') {
      navigate(`/menu/customize-pizza/${item.id}`);
    } else {
      addToCart(item.id, 1);
    }
  };

  // Handle modifying the item
  const handleModify = () => {
    navigate(`/menu/modify/${item.id}`);  // Navigate to the modify page
  };

  // Handle removing the item
  const handleRemove = () => {
    fetch(`http://localhost:5001/api/admin/menu/${item.id}`, {
      method: 'DELETE',
      credentials: 'include',  // Include credentials
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then(response => {
        if (response.ok) {
          fetchMenuItems();  // Re-fetch the updated menu after deletion
        } else {
          console.error('Failed to remove menu item');
        }
      })
      .catch(error => {
        console.error('Error removing menu item:', error);
      });
  };

  return (
      <div className="bg-white shadow-lg rounded-lg p-6 hover:shadow-xl transition-shadow duration-300 ease-in-out">
        <h3 className="text-xl font-bold mb-3 text-gray-900">{item.name}</h3>
        <p className="text-gray-700 mb-4">Price: ${item.price.toFixed(2)}</p>
        
        <button
          className="bg-blue-500 text-white px-5 py-2 rounded-lg hover:bg-blue-600 transition ease-in-out duration-200 mb-3"
          onClick={handleAddToCart}
        >
          {category === 'pizza' ? 'Customize' : 'Add to Cart'}
        </button>

        {/* Conditionally render the Modify and Remove buttons if isAdmin is true */}
        {isAdmin && (
          <div className="flex space-x-4 mt-4">
            <button
              className="bg-yellow-500 text-white px-5 py-2 rounded-lg hover:bg-yellow-600 transition ease-in-out duration-200"
              onClick={handleModify}
            >
              Modify
            </button>

            <button
              className="bg-red-500 text-white px-5 py-2 rounded-lg hover:bg-red-600 transition ease-in-out duration-200"
              onClick={handleRemove}
            >
              Remove
            </button>
          </div>
        )}
      </div>
    );
};

export default MenuItem;
