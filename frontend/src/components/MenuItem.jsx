// src/components/MenuItem.jsx
import React from 'react';
import { useCart } from '../context/CartContext';
import { useNavigate } from 'react-router-dom';

const MenuItem = ({ item, category }) => {
  const { addToCart } = useCart();
  const navigate = useNavigate();

  const handleAddToCart = () => {
    if (category === 'pizza') {
      navigate(`/customize-pizza/${item.id}`);
    } else {
      addToCart(item.id, 1);
    }
  };

  return (
    <div className="bg-white shadow-md rounded p-4">
      <h3 className="text-xl font-semibold mb-2">{item.name}</h3>
      <p className="text-gray-700 mb-2">Price: ${item.price.toFixed(2)}</p>
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={handleAddToCart}
      >
        {category === 'pizza' ? 'Customize' : 'Add to Cart'}
      </button>
    </div>
  );
};

export default MenuItem;
