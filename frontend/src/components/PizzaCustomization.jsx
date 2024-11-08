// src/components/PizzaCustomization.jsx
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useParams } from "react-router-dom";
import { useCart } from "../context/CartContext";

const PizzaCustomization = () => {
  const { id } = useParams();
  const [pizzaItem, setPizzaItem] = useState(null);
  const [ingredients, setIngredients] = useState([]);
  const [selectedIngredients, setSelectedIngredients] = useState([]);
  const { addToCart } = useCart();

  useEffect(() => {
    fetch(`http://localhost:5001/api/customer/menu/${id}`, {
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => setPizzaItem(data))
      .catch((error) => console.error("Error fetching pizza item:", error));

    fetch("http://localhost:5001/api/customer/ingredients", {
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => setIngredients(data))
      .catch((error) => console.error("Error fetching ingredients:", error));
  }, [id]);

  const handleIngredientChange = (ingredientId) => {
    setSelectedIngredients((prevSelected) => {
      if (prevSelected.includes(ingredientId)) {
        return prevSelected.filter((id) => id !== ingredientId);
      } else {
        return [...prevSelected, ingredientId];
      }
    });
  };

  const handleAddToCart = () => {
    addToCart(
      pizzaItem.id,
      1,
      selectedIngredients.map((ingredientId) => ({
        ingredient_id: ingredientId,
        name: ingredients.find((ingredient) => ingredient.id === ingredientId)
          .name,
        action: "add",
        price: ingredients.find((ingredient) => ingredient.id === ingredientId)
          .price,
      })),
    );
  };

  if (!pizzaItem) {
    return <p>Loading pizza details...</p>;
  }

  return (
    <div className="container mx-auto p-6 bg-gray-100 min-h-screen">
      <h2 className="text-3xl font-bold mb-6 text-center text-gray-900">
        Customize Your {pizzaItem.name}
      </h2>
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">
          Select Ingredients:
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {ingredients.map((ingredient) => (
            <label
              key={ingredient.id}
              className="flex items-center text-gray-700 bg-gray-50 p-2 rounded-lg shadow-sm"
            >
              <input
                type="checkbox"
                value={ingredient.id}
                checked={selectedIngredients.includes(ingredient.id)}
                onChange={() => handleIngredientChange(ingredient.id)}
                className="mr-3 accent-green-500"
              />
              <span>
                {ingredient.name} (+${ingredient.price.toFixed(2)})
              </span>
              <span>{ingredient.is_vegetarian ? " 🌱" : ""}</span>
              <span>{ingredient.is_vegan ? " 🥗" : ""}</span>
            </label>
          ))}
        </div>
        <Link to="/menu">
          <button
            className="w-full mt-6 bg-green-500 text-white font-semibold px-4 py-2 rounded-lg hover:bg-green-600 transition duration-200"
            onClick={handleAddToCart}
          >
            Add to Cart
          </button>
        </Link>
      </div>
    </div>
  );
};

export default PizzaCustomization;
