// src/components/PizzaTab.jsx
import React, { useEffect, useState } from 'react';
import MenuItem from './MenuItem';

const PizzaTab = () => {
  const [pizzaItems, setPizzaItems] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/api/customer/menu?category=pizza')
      .then(response => response.json())
      .then(data => setPizzaItems(data))
      .catch(error => console.error('Error fetching pizza items:', error));
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Pizzas</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {pizzaItems.map(item => (
          <MenuItem key={item.id} item={item} category="pizza" />
        ))}
      </div>
    </div>
  );
};

export default PizzaTab;
