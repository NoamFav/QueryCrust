// src/components/AdminTab.jsx
import React from 'react';
import { useAdminOrder } from '../context/AdminOrderContext';
import { useEffect } from 'react';

const AdminTab = () => {
    const {adminOrders, fetchAdminOrders} = useAdminOrder(); // Use the custom hook

    useEffect(() => {
        fetchAdminOrders(); // Fetch orders when component
    });

    return (
        <div className="min-h-screen bg-gray-100 p-6 pt-20">
            <h2 className="text-2xl font-bold mb-4">Orders Overview</h2>
            {adminOrders.length === 0 ? (
                <p>No orders found.</p> // Handle case with no orders
            ) : (
                <ul className="space-y-4">
                    {adminOrders.map(adminOrders => (
                        <li className="bg-white p-4 rounded shadow-md">
                            <h3 className="text-xl font-semibold">Order ID: {adminOrders.order_id}</h3>
                            <p>Total Cost: {adminOrders.total_cost} €</p>
                            <p>Status: {adminOrders.status}</p>
                            <p>Ordered At: {new Date(adminOrders.ordered_at).toLocaleString()}</p>
                            <p>Driver ID: {adminOrders.delivery_driver}</p>
                            <ul className="list-disc list-inside">
                                {adminOrders.items.map(item => (
                                    <li key={item.id}>
                                        {item.name} x {item.quantity}
                                        <ul className="list-disc list-inside">
                                            {item.ingredients.map(ingredient => (
                                                <li key={ingredient.id}>
                                                    {ingredient} ({ingredient.action === 'add' ? 'Add' : 'Remove'}) - {ingredient.price} €
                                                </li>
                                            ))}
                                        </ul>
                                    </li>
                                ))}
                            </ul>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default AdminTab;
