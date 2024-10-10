// src/components/Checkout.jsx
import React, { useContext, useState } from 'react';
import { CartContext } from '../context/CartContext';
import { OrderContext } from '../context/OrderContext';
import { useNavigate } from 'react-router-dom';

const Checkout = () => {
  const { cartItems, fetchCartItems } = useContext(CartContext); // Access the cart context
  const { fetchOrders } = useContext(OrderContext); // Access the order context
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [orderDetails, setOrderDetails] = useState(null);
  const navigate = useNavigate();

  const handleCheckout = () => {
    fetch('http://localhost:5001/api/customer/order', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        console.error('Error placing order:', data.error);
      } else {
        setOrderDetails(data);  // Store order details
        setOrderPlaced(true);   // Mark order as placed
        fetchCartItems();       // Explicitly re-fetch the cart after order
        fetchOrders();          // Explicitly re-fetch the orders after order
      }
    })
    .catch(err => console.error('Error during checkout:', err));
  };

  if (orderPlaced) {
    return (
      <div className="min-h-screen flex flex-col justify-center items-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
          <h1 className="text-2xl font-bold mb-6 text-center text-green-600">Order Confirmation</h1>
          <p className="text-lg">Order ID: <strong>{orderDetails.order_id}</strong></p>
          <p className="text-lg">Total Cost: <strong>${orderDetails.total_cost}</strong></p>
          <p className="text-lg">Order Date: <strong>{new Date(orderDetails.ordered_at).toLocaleString()}</strong></p>
          <p className="text-lg">Estimated Delivery Time: <strong>{new Date(orderDetails.delivery_eta).toLocaleString()}</strong></p>
          <p className="text-lg">Your order is being delivered by Driver #{orderDetails.driver_id}</p>
          <button 
            className="mt-6 w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-200" 
            onClick={() => navigate('/menu')}
          >
            Back to Menu
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
        <h1 className="text-2xl font-bold mb-6 text-center">Checkout</h1>

        {cartItems.length === 0 ? (
          <p className="text-center text-gray-500">Your cart is empty!</p>
        ) : (
          <>
            <ul className="space-y-4">
              {cartItems.map((item, index) => (
                <li key={index} className="flex flex-col">
                  <div className="flex justify-between">
                    <span>{item.name} x {item.quantity}</span>
                    <span>${(item.total_price).toFixed(2)}</span>
                  </div>

                  {/* Check if customizations exist and display them */}
                  {Array.isArray(item.customizations) && item.customizations.length > 0 && (
                    <div className="mt-2 text-sm text-gray-600">
                      <p className="font-semibold">Customizations:</p>
                      <ul className="list-disc list-inside">
                        {item.customizations.map((custom, customIndex) => (
                          <li key={customIndex}>
                            {custom.action === 'add' ? 'Add' : 'Remove'} {custom.name} (${custom.price.toFixed(2)})
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </li>
              ))}
            </ul>
            <div className="mt-6 border-t border-gray-300 pt-4">
              <p className="text-lg font-semibold text-right">Total: ${cartItems.reduce((acc, item) => acc + item.total_price, 0).toFixed(2)}</p>
            </div>

            <button 
              onClick={handleCheckout} 
              className="mt-6 w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition duration-200"
            >
              Place Order
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default Checkout;
