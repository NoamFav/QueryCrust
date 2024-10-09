// src/context/CartContext.jsx
import React, { createContext, useState, useEffect, useContext } from 'react';

export const CartContext = createContext();

// Custom hook for accessing cart context
export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children, isAuthenticated }) => {
  const [cartItems, setCartItems] = useState([]);

  // Function to fetch cart items from backend
  const fetchCartItems = () => {
    fetch('http://localhost:5001/api/customer/cart', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setCartItems(data); // Set cart items after fetching
        console.log('Cart fetched:', data);
      })
      .catch((err) => {
        console.error('Error fetching cart:', err);
      });
  };

  // Fetch cart items when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      fetchCartItems(); // Fetch the cart when authenticated
    } else {
      setCartItems([]); // Clear the cart when not authenticated
    }
  }, [isAuthenticated]);

  const addToCart = (menuId, quantity = 1, customizations = []) => {
    if (!isAuthenticated) return;

    console.log(`Adding to cart: menuId: ${menuId}, quantity: ${quantity}, customizations:`, customizations);

    fetch('http://localhost:5001/api/customer/cart/add', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ menu_id: menuId, quantity, customizations }),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((err) => {
            throw err;
          });
        }
        return response.json();
      })
      .then(() => {
        fetchCartItems(); // Refresh cart after adding an item
      })
      .catch((error) => {
        console.error('Error adding to cart:', error);
      });
  };

  const removeFromCart = (cartItemId) => {
    if (!isAuthenticated) return;

    fetch('http://localhost:5001/api/customer/cart/remove', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ cart_item_id: cartItemId }),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((err) => {
            throw err;
          });
        }
        return response.json();
      })
      .then(() => {
        fetchCartItems(); // Refresh cart after removing an item
      })
      .catch((error) => {
        console.error('Error removing from cart:', error);
      });
  };

  return (
    <CartContext.Provider value={{ cartItems, addToCart, removeFromCart, fetchCartItems }}>
      {children}
    </CartContext.Provider>
  );
};
