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

  // Handle removing the item
  const handleRemove = () => {
      fetch(`http://localhost:5001/api/admin/menu/${item.id}`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        }
      })
        .then(response => {
          if (!response.ok) {
            return response.json().then(data => {
              // Use the detailed error message returned from the backend
              throw new Error(data.error);
            });
          }
          fetchMenuItems();  // Re-fetch the updated menu after deletion
        })
        .catch(error => {
          console.error('Failed to remove menu item:', error.message);
          alert(`Error: ${error.message}`);  // Display a clear error message to the user
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

        {isAdmin && (
          <div className="flex space-x-4 mt-4">
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
