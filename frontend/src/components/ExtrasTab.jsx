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
    <div>
      <h2 className="text-2xl font-bold mb-4">Extra</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {extraItems.map(item => (
          <MenuItem key={item.id} item={item} category="extra" />
        ))}
      </div>
    </div>
  );
};

export default ExtrasTab;
