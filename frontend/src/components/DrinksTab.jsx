// src/components/DrinksTab.jsx
import React, { useEffect, useState } from 'react';
import MenuItem from './MenuItem';

const DrinksTab = () => {
  const [drinkItems, setDrinkItems] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/api/customer/menu?category=drink')
      .then(response => response.json())
      .then(data => setDrinkItems(data))
      .catch(error => console.error('Error fetching drinks items:', error));
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Drinks</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {drinkItems.map(item => (
          <MenuItem key={item.id} item={item} category="drink" />
        ))}
      </div>
    </div>
  );
};

export default DrinksTab;
