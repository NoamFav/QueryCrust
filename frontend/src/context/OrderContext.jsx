// src/context/CartContext.jsx
import React, { createContext, useState, useEffect, useContext } from 'react';

export const OrderContext = createContext();

export const useOrder = () => useContext(OrderContext);

export const OrderProvider = ({ children, isAuthenticated }) => {
    const [orders, setOrders] = useState([]);
    
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
            setOrders(data);
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
            fetchOrders();
            console.log('Order removed:', orderId);
        })
        .catch((err) => {
            console.error('Error removing order:', err);
        });
    };
    
    useEffect(() => {
        if (isAuthenticated) {
        fetchOrders();
        } else {
        setOrders([]);
        }
    }, [isAuthenticated]);
    
    return (
        <OrderContext.Provider value={{ orders, fetchOrders, removeOrder}}>
            {children}
        </OrderContext.Provider>
    );
}

