// src/components/MenuItem.jsx
import React from 'react';
import { useCart } from '../context/CartContext';
import { useNavigate } from 'react-router-dom';

const MenuItem = ({ item, category }) => {
  const { addToCart } = useCart();
  const navigate = useNavigate();

  const handleAddToCart = () => {
    if (category === 'pizza') {
      navigate(`/menu/customize-pizza/${item.id}`);
    } else {
      addToCart(item.id, 1);
    }
  };

  return (
    <div className="bg-white shadow-lg rounded-lg p-6 hover:shadow-xl transition-shadow duration-300 ease-in-out">
      <h3 className="text-xl font-bold mb-3 text-gray-900">{item.name}</h3>
      <p className="text-gray-700 mb-4">Price: ${item.price.toFixed(2)}</p>
      <button
        className="bg-blue-500 text-white px-5 py-2 rounded-lg hover:bg-blue-600 transition ease-in-out duration-200"
        onClick={handleAddToCart}
      >
        {category === 'pizza' ? 'Customize' : 'Add to Cart'}
      </button>
    </div>
  );
};

export default MenuItem;
