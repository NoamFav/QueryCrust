import React, { useEffect, useState } from "react";
import MenuItem from "./MenuItem";

const PizzaTab = ({ isAdmin }) => {
  const [pizzaItems, setPizzaItems] = useState([]);

  const fetchMenuItems = () => {
    fetch("http://localhost:5001/api/customer/menu?category=pizza", {
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => setPizzaItems(data))
      .catch((error) => console.error("Error fetching pizza items:", error));
  };

  useEffect(() => {
    fetchMenuItems();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">
        Our Pizzas
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {pizzaItems.map((item) => (
          <MenuItem
            key={item.id}
            item={item}
            category="pizza"
            fetchMenuItems={fetchMenuItems}
            isAdmin={isAdmin}
          />
        ))}
      </div>
    </div>
  );
};

export default PizzaTab;
