// src/components/ExtrasTab.jsx
import React, { useEffect, useState } from 'react';
import MenuItem from './MenuItem';

const ExtrasTab = () => {
  const [extraItems, setExtraItems] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/api/customer/menu?category=extra')
      .then(response => response.json())
      .then(data => setExtraItems(data))
      .catch(error => console.error('Error fetching extra items:', error));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">Our Extras</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {extraItems.map(item => (
          <MenuItem key={item.id} item={item} category="extra" />
        ))}
      </div>
    </div>
  );
};

export default ExtrasTab;
