// src/components/CategoryTabs.jsx
import React, { useState } from 'react';
import PizzaTab from './PizzaTab';
import DessertsTab from './DessertsTab';
import DrinksTab from './DrinksTab';
import ExtrasTab from './ExtrasTab';

const CategoryTabs = () => {
  const [activeTab, setActiveTab] = useState('Pizza');

  const renderTabContent = () => {
    switch (activeTab) {
      case 'Pizza':
        return <PizzaTab />;
      case 'Desserts':
        return <DessertsTab />;
      case 'Drinks':
        return <DrinksTab />;
      case 'Extras':
        return <ExtrasTab />;
      default:
        return <PizzaTab />;
    }
  };

  return (
    <div>
      <nav className="flex justify-center bg-gray-100">
        <button
          className={`px-4 py-2 ${activeTab === 'Pizza' ? 'text-blue-500 border-b-2 border-blue-500' : ''}`}
          onClick={() => setActiveTab('Pizza')}
        >
          Pizza
        </button>
        <button
          className={`px-4 py-2 ${activeTab === 'Desserts' ? 'text-blue-500 border-b-2 border-blue-500' : ''}`}
          onClick={() => setActiveTab('Desserts')}
        >
          Desserts
        </button>
        <button
          className={`px-4 py-2 ${activeTab === 'Drinks' ? 'text-blue-500 border-b-2 border-blue-500' : ''}`}
          onClick={() => setActiveTab('Drinks')}
        >
          Drinks
        </button>
        <button
          className={`px-4 py-2 ${activeTab === 'Extras' ? 'text-blue-500 border-b-2 border-blue-500' : ''}`}
          onClick={() => setActiveTab('Extras')}
        >
          Extras
        </button>
      </nav>
      <div className="p-4">{renderTabContent()}</div>
    </div>
  );
};

export default CategoryTabs;
