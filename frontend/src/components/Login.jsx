// src/components/Login.jsx

import React, { useState, useEffect} from 'react';
import { Link } from 'react-router-dom';

const Login = ({ setIsAuthenticated }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);

    const handleSubmit = (e) => {
        e.preventDefault(); // Prevent default form submission behavior

        fetch('http://localhost:5001/api/customer/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        })
        .then(response => {
            if (!response.ok) {
                // Handle HTTP errors
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            setIsAuthenticated(true); // Set the user as authenticated
            console.log(data.message);
            // TODO: Handle successful login (e.g., store user data, redirect)
        })
        .catch(error => {
            console.error('Error logging in:', error);
            setError(error.error || 'An error occurred during login.');
        });
    };

    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
                <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label htmlFor="email" className="block text-sm font-semibold text-gray-700">Email:</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded"
                            required
                        />
                    </div>
                    <div className="mb-4">
                        <label htmlFor="password" className="block text-sm font-semibold text-gray-700">Password:</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded"
                            required
                        />
                    </div>
                    {error && <div className="mb-4 text-red-500">{error}</div>}
                    <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Login</button>
                </form>

                <div className="mt-6 text-center">
                    <Link to="/register" className="text-blue-500 underline">
                        Not a member? Sign up here
                    </Link>
                </div>
            </div>
        </div>
    );
}
export default Login;

