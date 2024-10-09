// src/components/DrinksTab.jsx
import React, { useEffect, useState } from 'react';
import MenuItem from './MenuItem';

const DrinksTab = () => {
  const [drinkItems, setDrinkItems] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/api/customer/menu?category=drink', {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        }
    })
      .then(response => response.json())
      .then(data => setDrinkItems(data))
      .catch(error => console.error('Error fetching drinks items:', error));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">Our Drinks</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {drinkItems.map(item => (
          <MenuItem key={item.id} item={item} category="drink" />
        ))}
      </div>
    </div>
  );
};

export default DrinksTab;
