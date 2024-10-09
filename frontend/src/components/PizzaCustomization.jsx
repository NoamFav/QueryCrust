// src/components/PizzaCustomization.jsx
import React, { useEffect, useState, useContext } from 'react'; // Import useContext
import { useParams } from 'react-router-dom';
import { useCart } from '../context/CartContext'; // Import useCart

const PizzaCustomization = () => {
  const { id } = useParams();
  const [pizzaItem, setPizzaItem] = useState(null);
  const [ingredients, setIngredients] = useState([]);
  const [selectedIngredients, setSelectedIngredients] = useState([]);
  const { addToCart } = useCart(); // Use useCart hook

  useEffect(() => {
    // Fetch the pizza item
    fetch(`http://localhost:5001/api/customer/menu/${id}`)
      .then(response => response.json())
      .then(data => setPizzaItem(data))
      .catch(error => console.error('Error fetching pizza item:', error));

    // Fetch available ingredients
    fetch('http://localhost:5001/api/customer/ingredients')
      .then(response => response.json())
      .then(data => setIngredients(data))
      .catch(error => console.error('Error fetching ingredients:', error));
  }, [id]);

  const handleIngredientChange = (ingredientId) => {
    setSelectedIngredients(prevSelected => {
      if (prevSelected.includes(ingredientId)) {
        return prevSelected.filter(id => id !== ingredientId);
      } else {
        return [...prevSelected, ingredientId];
      }
    });
  };

  const handleAddToCart = () => {
    addToCart(pizzaItem.id, 1, selectedIngredients.map(ingredientId => ({
      ingredient_id: ingredientId,
      name: ingredients.find(ingredient => ingredient.id === ingredientId).name,
      action: 'add', // or 'remove' based on your logic
    })));
  };

  if (!pizzaItem) {
    return <p>Loading pizza details...</p>;
  }

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Customize Your {pizzaItem.name}</h2>
      <div>
        <h3 className="text-xl font-semibold mb-2">Select Ingredients:</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
          {ingredients.map(ingredient => (
            <label key={ingredient.id} className="flex items-center">
              <input
                type="checkbox"
                value={ingredient.id}
                checked={selectedIngredients.includes(ingredient.id)}
                onChange={() => handleIngredientChange(ingredient.id)}
                className="mr-2"
              />
              {ingredient.name} (+${ingredient.price.toFixed(2)})
            </label>
          ))}
        </div>
      </div>
      <button
        className="bg-green-500 text-white px-4 py-2 rounded mt-4"
        onClick={handleAddToCart}
      >
        Add to Cart
      </button>
    </div>
  );
};

export default PizzaCustomization;
