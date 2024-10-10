// src/context/CartContext.jsx
import React, { createContext, useState, useEffect, useContext } from 'react';

export const OrderContext = createContext();

// Custom hook for accessing order context
export const useOrder = () => useContext(OrderContext);

export const OrderProvider = ({ children, isAuthenticated }) => {
    const [orders, setOrders] = useState([]);
    
    // Function to fetch orders from backend
    const fetchOrders = () => {
        if (!isAuthenticated) return;
        fetch('http://localhost:5001/api/customer/orders', {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        })
        .then((response) => response.json())
        .then((data) => {
            setOrders(data); // Set orders after fetching
            console.log('Orders fetched:', data);
        })
        .catch((err) => {
            console.error('Error fetching orders:', err);
        });
    };

    const removeOrder = (orderId) => {
        if (!isAuthenticated) return;

        fetch(`http://localhost:5001/api/customer/orders/${orderId}/cancel`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
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
            setOrders((prevOrders) => prevOrders.filter((order) => order.id !== orderId));
            fetchOrders(); // Re-fetch orders after removing
            console.log('Order removed:', orderId);
        })
        .catch((err) => {
            console.error('Error removing order:', err);
        });
    };
    
    // Fetch orders when authenticated
    useEffect(() => {
        if (isAuthenticated) {
        fetchOrders(); // Fetch the orders when authenticated
        } else {
        setOrders([]); // Clear the orders when not authenticated
        }
    }, [isAuthenticated]);
    
    return (
        <OrderContext.Provider value={{ orders, fetchOrders, removeOrder}}>
            {children}
        </OrderContext.Provider>
    );
}

