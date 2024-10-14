import React, { useState, useEffect } from 'react';

const PersonalDetails = () => {
  const [userDetails, setUserDetails] = useState(null); // To store user details
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state

  // Fetch the customer data on component mount
  useEffect(() => {
    fetch('http://localhost:5001/api/customer/details', {
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch user details');
        }
        return response.json();
      })
      .then(data => {
        setUserDetails(data); // Store user details in state
        setLoading(false); // Stop loading
      })
      .catch(error => {
        setError(error.message); // Store error if any
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="min-h-screen bg-gray-100 p-10 flex justify-center items-center">
      <div className="max-w-3xl w-full bg-white p-10 rounded-lg shadow-lg">
        <h2 className="text-4xl font-bold mb-8 text-center text-gray-800">Personal Details</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p className="text-lg font-semibold text-gray-700">Name:</p>
            <p className="text-gray-800">{userDetails.name}</p>
          </div>
          <div>
            <p className="text-lg font-semibold text-gray-700">Email:</p>
            <p className="text-gray-800">{userDetails.email}</p>
          </div>
          <div>
            <p className="text-lg font-semibold text-gray-700">Phone Number:</p>
            <p className="text-gray-800">{userDetails.phone_number}</p>
          </div>
          <div>
            <p className="text-lg font-semibold text-gray-700">Address:</p>
            <p className="text-gray-800">{userDetails.address}</p>
          </div>
          <div>
            <p className="text-lg font-semibold text-gray-700">Birthday:</p>
            <p className="text-gray-800">{new Date(userDetails.birthday).toLocaleDateString()}</p>
          </div>
          <div>
            <p className="text-lg font-semibold text-gray-700">Gender:</p>
            <p className="text-gray-800">{userDetails.gender}</p>
          </div>
          <div>
            <p className="text-lg font-semibold text-gray-700">Number of orders:</p>
            <p className="text-gray-800">{userDetails.previous_orders}</p>
          </div>
          <div>
            <p className="text-lg font-semibold text-gray-700">Last order:</p>
            <p className="text-gray-800">{userDetails.last_order}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PersonalDetails;
