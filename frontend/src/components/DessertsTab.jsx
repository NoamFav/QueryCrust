// src/components/DessertsTab.jsx
import React, { useEffect, useState } from 'react';
import MenuItem from './MenuItem';

const DessertsTab = () => {
  const [dessertItems, setDessertItems] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/api/customer/menu?category=dessert')
      .then(response => response.json())
      .then(data => setDessertItems(data))
      .catch(error => console.error('Error fetching dessert items:', error));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">Our Deserts</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {dessertItems.map(item => (
          <MenuItem key={item.id} item={item} category="dessert" />
        ))}
      </div>
    </div>
  );
};

export default DessertsTab;
