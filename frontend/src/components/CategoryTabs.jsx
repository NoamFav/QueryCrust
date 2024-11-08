// src/components/CategoryTabs.jsx
import React, { useState } from "react";
import PizzaTab from "./PizzaTab";
import DessertsTab from "./DessertsTab";
import DrinksTab from "./DrinksTab";
import ExtrasTab from "./ExtrasTab";

const CategoryTabs = ({ isAdmin }) => {
  const [activeTab, setActiveTab] = useState("Pizza");

  const renderTabContent = () => {
    switch (activeTab) {
      case "Pizza":
        return <PizzaTab isAdmin={isAdmin} />;
      case "Desserts":
        return <DessertsTab isAdmin={isAdmin} />;
      case "Drinks":
        return <DrinksTab isAdmin={isAdmin} />;
      case "Extras":
        return <ExtrasTab isAdmin={isAdmin} />;
      default:
        return <PizzaTab isAdmin={isAdmin} />;
    }
  };

  return (
    <div className="pt-20">
      <nav className="flex justify-center bg-gray-100 shadow-md rounded-lg p-4 mb-6 space-x-8">
        <button
          className={`px-6 py-2 font-semibold transition-colors duration-200 ${
            activeTab === "Pizza"
              ? "text-blue-500 border-b-4 border-blue-500"
              : "text-gray-600 hover:text-blue-500"
          }`}
          onClick={() => setActiveTab("Pizza")}
        >
          Pizza
        </button>
        <button
          className={`px-6 py-2 font-semibold transition-colors duration-200 ${
            activeTab === "Desserts"
              ? "text-blue-500 border-b-4 border-blue-500"
              : "text-gray-600 hover:text-blue-500"
          }`}
          onClick={() => setActiveTab("Desserts")}
        >
          Desserts
        </button>
        <button
          className={`px-6 py-2 font-semibold transition-colors duration-200 ${
            activeTab === "Drinks"
              ? "text-blue-500 border-b-4 border-blue-500"
              : "text-gray-600 hover:text-blue-500"
          }`}
          onClick={() => setActiveTab("Drinks")}
        >
          Drinks
        </button>
        <button
          className={`px-6 py-2 font-semibold transition-colors duration-200 ${
            activeTab === "Extras"
              ? "text-blue-500 border-b-4 border-blue-500"
              : "text-gray-600 hover:text-blue-500"
          }`}
          onClick={() => setActiveTab("Extras")}
        >
          Extras
        </button>
      </nav>
      <div className="p-6 bg-white rounded-lg shadow-lg">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default CategoryTabs;
