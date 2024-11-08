// src/components/Cart.jsx
import React from "react";
import { useCart } from "../context/CartContext";
import { Link, useNavigate } from "react-router-dom";

const Cart = () => {
  const { cartItems, removeFromCart } = useCart();
  const navigate = useNavigate();

  const totalPrice =
    cartItems.reduce((acc, item) => acc + item.total_price, 0) * 1.4 * 1.09;

  const handleProceedToCheckout = () => {
    navigate("/checkout");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-20">
      <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
        <h2 className="text-3xl font-bold mb-6 text-center">Your Cart</h2>

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
              {cartItems.map((item) => (
                <li
                  key={item.id}
                  className="flex justify-between items-center bg-gray-50 shadow-md rounded-lg p-4 hover:bg-gray-100"
                >
                  <div>
                    <h3 className="text-xl font-semibold">{item.name}</h3>
                    <p className="text-gray-600">
                      Price: ${item.price.toFixed(2)}
                    </p>
                    <p className="text-gray-600">Quantity: {item.quantity}</p>
                    {Array.isArray(item.customizations) &&
                      item.customizations.length > 0 && (
                        <div className="mt-2">
                          <p className="font-semibold">Customizations:</p>
                          <ul className="list-disc list-inside text-gray-600">
                            {item.customizations.map((custom, index) => (
                              <li key={index}>
                                Ingredient:{" "}
                                {custom.name || "Unknown Ingredient"} (
                                {custom.action === "add" ? "Add" : "Remove"}) -
                                ${custom.price.toFixed(2)}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                  </div>
                  <div className="flex flex-col items-end">
                    <p className="text-lg font-semibold">
                      Total: ${item.total_price.toFixed(2)}
                    </p>
                    <button
                      onClick={() => removeFromCart(item.id)}
                      className="mt-2 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition ease-in-out duration-200"
                    >
                      Remove
                    </button>
                  </div>
                </li>
              ))}
            </ul>

            <div className="mt-6 flex justify-between items-center">
              <p className="text-xl font-semibold">
                Grand Total: ${totalPrice.toFixed(2)}
              </p>
              <button
                className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition ease-in-out duration-200"
                onClick={handleProceedToCheckout}
              >
                Proceed to Checkout
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Cart;
