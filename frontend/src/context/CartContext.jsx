// src/context/CartContext.jsx
// src/context/CartContext.jsx
import React, { createContext, useState, useEffect, useContext } from 'react';

export const CartContext = createContext();

// Custom hook for accessing cart context
export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);

  // Fetch cart items from backend on mount
  useEffect(() => {
    fetch('http://localhost:5001/api/customer/cart', { 
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => setCartItems(data))
      .catch(error => console.error('Error fetching cart items:', error));
  }, []);

  const addToCart = (menuId, quantity = 1, customizations = []) => {
    console.log(`Sending addToCart with menuId: ${menuId}, quantity: ${quantity}, customizations:`, customizations);
    fetch('http://localhost:5001/api/customer/cart/add', {
      method: 'POST',
      credentials: 'include',
      headers: { 
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify({ menu_id: menuId, quantity, customizations }),
    })
      .then(response => {
        if (!response.ok) {
          // Handle HTTP errors
          return response.json().then(err => { throw err; });
        }
        return response.json();
      })
      .then(data => {
        console.log(data.message);
        // Refresh cart items
        return fetch('http://localhost:5001/api/customer/cart', { 
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          }
        });
      })
      .then(response => response.json())
      .then(data => setCartItems(data))
      .catch(error => console.error('Error adding to cart:', error));
  };

  const removeFromCart = (cartItemId) => {
    fetch('http://localhost:5001/api/customer/cart/remove', {
      method: 'POST',
      credentials: 'include',
      headers: { 
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify({ cart_item_id: cartItemId }),
    })
      .then(response => {
        if (!response.ok) {
          // Handle HTTP errors
          return response.json().then(err => { throw err; });
        }
        return response.json();
      })
      .then(data => {
        console.log(data.message);
        // Update cart items
        setCartItems(cartItems.filter(item => item.id !== cartItemId));
      })
      .catch(error => console.error('Error removing from cart:', error));
  };

  return (
    <CartContext.Provider value={{ cartItems, addToCart, removeFromCart }}>
      {children}
    </CartContext.Provider>
  );
};
