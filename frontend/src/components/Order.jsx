import React, { useEffect, useState } from 'react';
import { useOrder } from '../context/OrderContext';
import { Link } from 'react-router-dom';

const Order = () => {
    const { orders, removeOrder} = useOrder();
    const [updatedOrders, setUpdatedOrders] = useState([]);

    const canCancelOrder = (order) => {
        if (order.status === 'Pending') {
            const now = new Date();
            const orderedAt = new Date(order.ordered_at);
            const timeDiff = (now - orderedAt) / 1000;
            return timeDiff < 300;
        }
        return false;
    };

    useEffect(() => {
        const newOrders = orders.map((order) => ({
            ...order,
            canCancel: canCancelOrder(order),
        }));
        setUpdatedOrders(newOrders);
    }, [orders]);

    useEffect(() => {
        const interval = setInterval(() => {
            const newOrders = orders.map((order) => ({
                ...order,
                canCancel: canCancelOrder(order),
            }));
            setUpdatedOrders(newOrders);
        }, 10000);

        return () => clearInterval(interval);
    }, [orders]);

    return (
        <div className="min-h-screen bg-gray-100 p-20">
            <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
                <h2 className="text-3xl font-bold mb-6 text-center">Your Orders</h2>

                {orders.length === 0 ? (
                    <div className="text-center">
                        <p className="text-gray-700 mb-4">You have no orders.</p>
                        <Link to="/" className="text-blue-500 underline">
                            Go to Menu
                        </Link>
                    </div>
                ) : (
                    <>
                    <ul className="space-y-4">
                            {updatedOrders.map((order) => (
                                <li key={order.order_id} className="flex justify-between items-center bg-gray-50 shadow-md rounded-lg p-4 hover:bg-gray-100">
                                    <div>
                                        <h3 className="text-xl font-semibold">Order ID: {order.order_id}</h3>
                                        <p className="text-gray-600">Total: {order.total_cost} €</p>
                                        <p className="text-gray-600">Date: {new Date(order.ordered_at).toLocaleString()}</p>
                                        <p className="text-gray-600">Address: {order.address}</p>
                                        <p className="text-gray-600">ETA: {order.delivery_eta ? new Date(order.delivery_eta).toLocaleString() : 'N/A'}</p>

                                        <p className="text-gray-600">Drivers: {order.delivery_drivers.join(', ') || 'N/A'}</p>

                                        <p className="text-gray-600">Status: {order.status}</p>
                                    </div>
                                    <div className="flex flex-col items-end">
                                        <button
                                            onClick={() => {
                                                removeOrder(order.order_id);
                                            }}
                                            disabled={order.status === 'In Delivery' || (order.status === 'Pending' && !order.canCancel)}
                                            className={`mt-2 px-4 py-2 rounded-lg transition ease-in-out duration-200 ${
                                                order.status === 'Delivered' || order.status === 'Cancelled'
                                                    ? 'bg-red-500 text-white hover:bg-red-600'
                                                    : order.status === 'In Delivery' || !order.canCancel
                                                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                                    : 'bg-yellow-500 text-white hover:bg-yellow-600'
                                            }`}
                                        >
                                            {order.status === 'Delivered' || order.status === 'Cancelled' 
                                                ? 'Remove'
                                                : order.status === 'Pending' && order.canCancel
                                                ? 'Cancel'
                                                : 'Cannot Cancel'}
                                        </button>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </>
                )}
            </div>
        </div>
    );
}
export default Order;
