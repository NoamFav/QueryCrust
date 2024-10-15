// src/context/AdminOrderContext.jsx
import React, { createContext, useState, useEffect, useContext } from 'react';

export const AdminOrderContext = createContext();

export const useAdminOrder = () => useContext(AdminOrderContext);

export const AdminOrderProvider = ({ children, isAuthenticated }) => {
    const [adminOrders, setAdminOrders] = useState([]);
    const [error, setError] = useState(null);

    const fetchAdminOrders = async () => {
        try {
            console.log("Fetching admin orders...");
            const response = await fetch('http://localhost:5001/api/admin/orders', {
                credentials: 'include', 
            });
            if (!response.ok) {
                throw new Error('Failed to fetch orders');
            }
            const data = await response.json();
            console.log("Admin orders fetched successfully:", data);
            setAdminOrders(data);
        } catch (err) {
            console.error("Error fetching admin orders:", err.message);
            setError(err.message);
        } 
    };

    const updateOrderStatus = async (orderId, newStatus) => {
        try {
            console.log(`Updating order ${orderId} status to ${newStatus}...`);
            const response = await fetch(`http://localhost:5001/api/admin/orders/${orderId}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ status: newStatus }),
            });
            if (!response.ok) {
                throw new Error('Failed to update order status');
            }
            console.log(`Order ${orderId} status updated to ${newStatus}`);
            fetchAdminOrders();
        } catch (err) {
            console.error(`Error updating order status for ${orderId}:`, err.message);
            setError(err.message);
        }
    };

    useEffect(() => {
        if (isAuthenticated) {
            fetchAdminOrders();
        } else {
            setAdminOrders([]);
        }
    }, [isAuthenticated]);

    return (
        <AdminOrderContext.Provider value={{ adminOrders, fetchAdminOrders, updateOrderStatus }}>
            {children}
        </AdminOrderContext.Provider>
    );
};
