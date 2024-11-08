// src/context/CartContext.jsx
import React, { createContext, useState, useEffect, useContext } from "react";

export const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children, isAuthenticated }) => {
  const [cartItems, setCartItems] = useState([]);

  const fetchCartItems = () => {
    fetch("http://localhost:5001/api/customer/cart", {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setCartItems(data);
        console.log("Cart fetched:", data);
      })
      .catch((err) => {
        console.error("Error fetching cart:", err);
      });
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchCartItems();
    } else {
      setCartItems([]);
    }
  }, [isAuthenticated]);

  const addToCart = (menuId, quantity = 1, customizations = []) => {
    if (!isAuthenticated) return;

    console.log(
      `Adding to cart: menuId: ${menuId}, quantity: ${quantity}, customizations:`,
      customizations,
    );

    fetch("http://localhost:5001/api/customer/cart/add", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
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
        fetchCartItems();
      })
      .catch((error) => {
        console.error("Error adding to cart:", error);
      });
  };

  const removeFromCart = (cartItemId) => {
    if (!isAuthenticated) return;

    fetch("http://localhost:5001/api/customer/cart/remove", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
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
        fetchCartItems();
      })
      .catch((error) => {
        console.error("Error removing from cart:", error);
      });
  };

  return (
    <CartContext.Provider
      value={{ cartItems, addToCart, removeFromCart, fetchCartItems }}
    >
      {children}
    </CartContext.Provider>
  );
};
