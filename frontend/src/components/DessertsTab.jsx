// src/components/DessertsTab.jsx
import React, { useEffect, useState } from 'react';
import MenuItem from './MenuItem';

const DessertsTab = () => {
  const [dessertItems, setDessertItems] = useState([]);

  useEffect(() => {
    fetch('/api/customer/menu?category=dessert')
      .then(response => response.json())
      .then(data => setDessertItems(data))
      .catch(error => console.error('Error fetching dessert items:', error));
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Desserts</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {dessertItems.map(item => (
          <MenuItem key={item.id} item={item} category="dessert" />
        ))}
      </div>
    </div>
  );
};

export default DessertsTab;
