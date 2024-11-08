// src/components/AdminTab.jsx
import React from "react";
import { useAdminOrder } from "../context/AdminOrderContext";
import { useEffect } from "react";

const AdminTab = () => {
  const { adminOrders, fetchAdminOrders, updateOrderStatus } = useAdminOrder();

  useEffect(() => {
    fetchAdminOrders();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      fetchAdminOrders();
    }, 60000);

    return () => clearInterval(interval);
  }, []);

  const handleStatusUpdate = (orderId, newStatus) => {
    updateOrderStatus(orderId, newStatus);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 pt-20">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Orders Overview</h2>
      {adminOrders.length === 0 ? (
        <p className="text-gray-500">No orders found.</p>
      ) : (
        <ul className="space-y-6">
          {adminOrders.map((order) => (
            <li
              key={order.order_id}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300"
            >
              <div className="flex justify-between items-center">
                <h3 className="text-xl font-semibold text-indigo-600">
                  Order ID: {order.order_id}
                </h3>
                <p className="text-gray-700 font-medium">
                  Total:{" "}
                  <span className="text-green-600">{order.total_cost} €</span>
                </p>
              </div>
              <p className="text-gray-500">Status: {order.status}</p>
              <p className="text-gray-500">
                Ordered At: {new Date(order.ordered_at).toLocaleString()}
              </p>

              <p className="text-gray-500">
                Driver IDs:{" "}
                {order.driver_ids.length > 0
                  ? order.driver_ids.join(", ")
                  : "N/A"}
              </p>

              <p className="text-gray-500">Customer: {order.customer_name}</p>
              <p className="text-gray-500">Address: {order.customer_address}</p>

              <ul className="mt-4 space-y-2">
                {order.items.map((item) => (
                  <li
                    key={item.item_id}
                    className="border-t border-gray-200 pt-2"
                  >
                    <p className="text-gray-700">
                      <span className="font-medium">{item.name}</span> x{" "}
                      {item.quantity}
                    </p>
                    <ul className="pl-4 text-gray-600">
                      {item.ingredients.map((ingredient) => (
                        <li key={ingredient.name}>
                          {ingredient.name}
                          <span
                            className={`text-${ingredient.action === "add" ? "green" : "red"}-500`}
                          >
                            ({ingredient.action === "add" ? "Add" : "Remove"})
                          </span>
                          - {ingredient.price} €
                        </li>
                      ))}
                    </ul>
                  </li>
                ))}
              </ul>

              <div className="mt-4 flex space-x-2">
                <button
                  className="bg-yellow-500 text-white py-2 px-4 rounded hover:bg-yellow-600"
                  onClick={() =>
                    handleStatusUpdate(order.order_id, "In Preparation")
                  }
                >
                  In Preparation
                </button>
                <button
                  className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
                  onClick={() =>
                    handleStatusUpdate(order.order_id, "In Delivery")
                  }
                >
                  In Delivery
                </button>
                <button
                  className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
                  onClick={() =>
                    handleStatusUpdate(order.order_id, "Delivered")
                  }
                >
                  Delivered
                </button>
                <button
                  className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
                  onClick={() =>
                    handleStatusUpdate(order.order_id, "Cancelled")
                  }
                >
                  Cancelled
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
export default AdminTab;
