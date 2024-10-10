// src/context/AdminOrderContext.jsx
import React, { createContext, useState, useEffect, useContext } from 'react';

export const AdminOrderContext = createContext();

// Custom hook for accessing all the orders from clients
export const useAdminOrder = () => useContext(AdminOrderContext);

// Provider component
export const AdminOrderProvider = ({ children, isAuthenticated }) => {
    const [adminOrders, setAdminOrders] = useState([]); // State to hold orders
    const [error, setError] = useState(null); // Error state for handling errors

    // Fetch all orders from the API
    const fetchAdminOrders = async () => {
        try {
            console.log("Fetching admin orders...");
            const response = await fetch('http://localhost:5001/api/admin/orders', {
                credentials: 'include', // Include credentials if needed
            });
            if (!response.ok) {
                throw new Error('Failed to fetch orders');
            }
            const data = await response.json();
            console.log("Admin orders fetched successfully:", data); // Log fetched data
            setAdminOrders(data); // Set the orders state
        } catch (err) {
            console.error("Error fetching admin orders:", err.message); // Log error
            setError(err.message); // Set error if there's an issue
        } 
    };

    useEffect(() => {
        if (isAuthenticated) {
            fetchAdminOrders(); // Fetch the orders when authenticated
        } else {
            setAdminOrders([]); // Clear the orders when not authenticated
        }
    }, [isAuthenticated]);

    return (
        <AdminOrderContext.Provider value={{ adminOrders, fetchAdminOrders }}>
            {children}
        </AdminOrderContext.Provider>
    );
};
