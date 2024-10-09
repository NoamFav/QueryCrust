// src/components/Cart.jsx
import React from 'react';
import { useCart } from '../context/CartContext'; // Import the useCart hook
import { Link } from 'react-router-dom'; // For navigation

const Cart = () => {
  const { cartItems, removeFromCart } = useCart(); // Destructure cartItems and removeFromCart from context

  // Calculate total price
  const totalPrice = cartItems.reduce((acc, item) => acc + item.total_price, 0);

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Your Cart</h2>

      {cartItems.length === 0 ? (
        <div className="text-center">
          <p className="text-gray-700 mb-4">Your cart is empty.</p>
          <Link to="/" className="text-blue-500 underline">
            Go to Menu
          </Link>
        </div>
      ) : (
        <>
          <ul className="space-y-4">
            {cartItems.map(item => (
              <li key={item.id} className="flex justify-between items-center bg-white shadow-md rounded p-4">
                <div>
                  <h3 className="text-xl font-semibold">{item.name}</h3>
                  <p className="text-gray-700">Price: ${item.price.toFixed(2)}</p>
                  <p className="text-gray-700">Quantity: {item.quantity}</p>
                  {Array.isArray(item.customizations) && item.customizations.length > 0 && (
                    <div className="mt-2">
                      <p className="font-semibold">Customizations:</p>
                      <ul className="list-disc list-inside">
                        {item.customizations.map((custom, index) => (
                          <li key={index}>
                            Ingredient: {custom.name || 'Unknown Ingredient'}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}                
                </div>
                <div className="flex flex-col items-end">
                  <p className="text-lg font-semibold">Total: ${item.total_price.toFixed(2)}</p>
                  <button
                    onClick={() => removeFromCart(item.id)}
                    className="mt-2 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                  >
                    Remove
                  </button>
                </div>
              </li>
            ))}
          </ul>

          <div className="mt-6 flex justify-between items-center">
            <p className="text-xl font-semibold">Grand Total: ${totalPrice.toFixed(2)}</p>
            <button className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
              Proceed to Checkout
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Cart;
