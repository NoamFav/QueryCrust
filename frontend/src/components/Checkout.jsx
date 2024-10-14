// src/components/Checkout.jsx
import React, { useContext, useState, useEffect } from 'react';
import { CartContext } from '../context/CartContext';
import { OrderContext } from '../context/OrderContext';
import { useNavigate } from 'react-router-dom';

const Checkout = () => {
  const { cartItems, fetchCartItems } = useContext(CartContext); // Access the cart context
  const { fetchOrders } = useContext(OrderContext); // Access the order context
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [orderDetails, setOrderDetails] = useState(null);
  const [deliveryAddress, setDeliveryAddress] = useState('');
  const [discountCode, setDiscountCode] = useState('');
  const [discountValue, setDiscountValue] = useState(0);
  const [totalCost, setTotalCost] = useState(cartItems.reduce((acc, item) => acc + item.total_price, 0));
  const [originalCost, setOriginalCost] = useState(totalCost); // Original cost before applying discount
  const [appliedDiscount, setAppliedDiscount] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://localhost:5001/api/customer/details', {
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => setDeliveryAddress(data.address)) // Pre-fill address from user details
      .catch((err) => setError('Failed to fetch user details.'));
  }, []);

  const handleCheckout = () => {
    if (!deliveryAddress.trim()) {
      setError('Please enter a valid address.');
      return;
    }

    if(!appliedDiscount) {
        setDiscountValue(0); // Set discount value to 0 if no discount applied
        setDiscountCode(''); // Clear discount code
    }

    fetch('http://localhost:5001/api/customer/order', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
        body: JSON.stringify({ address: deliveryAddress, discountValue: discountValue, discountName: discountCode }), // Pass the address to the backend
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          console.error('Error placing order:', data.error);
        } else {
          setOrderDetails(data); // Store order details
          setOrderPlaced(true); // Mark order as placed
          fetchCartItems(); // Re-fetch the cart after the order
          fetchOrders(); // Re-fetch orders after the order
        }
      })
      .catch((err) => console.error('Error during checkout:', err));
  };

  const applyDiscount = () => {
    if (!discountCode.trim()) {
      setError('Please enter a promo code.');
      return;
    }

    // Prevent applying more than one discount
    if (appliedDiscount) {
      setError('A discount code has already been applied. Please remove it before applying a new one.');
      return;
    }

    fetch('http://localhost:5001/api/customer/discount', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ discount_code: discountCode }), // Send discount code to the backend
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          setError(data.error); // Show error message if the discount code is invalid
          setDiscountCode(''); // Reset discount code if invalid
        } else {
          setError(''); // Clear error
          setAppliedDiscount(true); // Mark that a discount is applied
          setOriginalCost(totalCost); // Store original cost before applying discount
          setTotalCost((prevTotal) => prevTotal * (1 - data.discount_value)); // Apply discount and update total cost
          setDiscountValue(data.discount_value); // Store the discount value
          setDiscountCode(data.discount_name); // Store the discount code
        }
      })
      .catch((err) => {
        console.error('Error applying discount:', err);
        setError('Failed to apply discount code.');
      });
  };

  // Function to remove the discount
  const removeDiscount = () => {
    setAppliedDiscount(false); // Reset discount state
    setTotalCost(originalCost); // Revert to original cost
    setDiscountCode(''); // Clear discount code
    setError(''); // Clear any error messages
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
          <p className="text-lg">Your order is being delivered by the following drivers:</p>
            <ul>
              {orderDetails.delivery_drivers.map((driverId, index) => (
                <li key={index}>Driver #{driverId}</li>
              ))}
            </ul>
          <p className="text-lg">Delivery Address: <strong>{orderDetails.address}</strong></p>
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

            <div className="mt-6">
              <label className="block mb-2 font-semibold text-gray-700">Delivery Address:</label>
              <input
                type="text"
                className="w-full px-4 py-2 border rounded-lg text-gray-700"
                value={deliveryAddress}
                onChange={(e) => setDeliveryAddress(e.target.value)} // Update the address
              />
              {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>

            <div className="mt-6">
              <label className="block mb-2 font-semibold text-gray-700">Promo Code:</label>
              <input
                type="text"
                className="w-full px-4 py-2 border rounded-lg text-gray-700"
                placeholder="Enter promo code"
                value={discountCode}
                disabled={appliedDiscount}
                onChange={(e) => setDiscountCode(e.target.value)} // Handle promo code input
              />
              <button
                onClick={applyDiscount} // Apply the discount code
                className="mt-2 bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-200"
                disabled={appliedDiscount} // Disable if discount is already applied
              >
                Apply Promo Code
              </button>
              {appliedDiscount && (
                <button
                  onClick={removeDiscount} // Remove the discount
                  className="mt-2 ml-2 bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600 transition duration-200"
                >
                  Remove Promo Code
                </button>
              )}
              {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>

            <div className="mt-6 border-t border-gray-300 pt-4 text-right">
              {appliedDiscount ? (
                <p className="text-lg font-semibold">
                  <span className="text-gray-500 line-through">${originalCost.toFixed(2)}</span>
                  <span className="text-green-600">${totalCost.toFixed(2)}</span> 
                </p>
              ) : (
                <p className="text-lg font-semibold">
                  <span>${totalCost.toFixed(2)}</span> 
                </p>
              )}
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
