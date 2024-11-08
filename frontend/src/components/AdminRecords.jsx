// src/components/AdminRecords.jsx
import React, { useEffect, useState } from "react";
import { Bar, Line, Pie, Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
);

const AdminRecords = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5001/api/admin/records", {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => setOrders(data))
      .catch((error) => console.log(error));
  }, []);

  const getTotalCostData = () => {
    return orders.map((order) => order.total_cost);
  };

  const parseDate = (dateString) => {
    const parsedDate = new Date(dateString);
    const year = parsedDate.getFullYear();
    const month = String(parsedDate.getMonth() + 1).padStart(2, "0");
    return `${year}-${month}`;
  };

  const getOrderDates = () =>
    orders.map((order) => parseDate(order.ordered_at));

  const getMonthlyData = () => {
    const monthlyTotals = {};
    orders.forEach((order) => {
      const month = parseDate(order.ordered_at);
      if (!monthlyTotals[month]) {
        monthlyTotals[month] = 0;
      }
      monthlyTotals[month] += order.total_cost;
    });
    return monthlyTotals;
  };

  const getAnnualData = () => {
    const annualTotals = {};
    orders.forEach((order) => {
      const year = new Date(order.ordered_at).getFullYear();
      if (!annualTotals[year]) {
        annualTotals[year] = 0;
      }
      annualTotals[year] += order.total_cost;
    });
    return annualTotals;
  };

  const getTotalCostPerCustomer = () => {
    const customerTotals = {};
    orders.forEach((order) => {
      const customerId = order.customer_id;
      if (!customerTotals[customerId]) {
        customerTotals[customerId] = 0;
      }
      customerTotals[customerId] += order.total_cost;
    });
    return customerTotals;
  };

  const getDriverData = () => {
    const driverMap = {};
    orders.forEach((order) => {
      order.driver_ids.forEach((driverId) => {
        driverMap[driverId] = (driverMap[driverId] || 0) + 1;
      });
    });
    return Object.keys(driverMap).map((driverId) => ({
      driver: `Driver ${driverId}`,
      count: driverMap[driverId],
    }));
  };

  const getGenderData = () => {
    const genderCount = { Male: 0, Female: 0, Other: 0 };
    orders.forEach((order) => {
      genderCount[order.customer_gender] =
        (genderCount[order.customer_gender] || 0) + 1;
    });
    return genderCount;
  };

  const getAgeData = () => {
    const ageGroups = { "18-25": 0, "26-35": 0, "36-45": 0, "46+": 0 };
    orders.forEach((order) => {
      const age = order.customer_age;
      if (age >= 18 && age <= 25) ageGroups["18-25"]++;
      else if (age >= 26 && age <= 35) ageGroups["26-35"]++;
      else if (age >= 36 && age <= 45) ageGroups["36-45"]++;
      else ageGroups["46+"]++;
    });
    return ageGroups;
  };

  const getLocationData = () => {
    const locationMap = {};
    orders.forEach((order) => {
      const location = order.customer_address;
      locationMap[location] = (locationMap[location] || 0) + 1;
    });
    return locationMap;
  };

  const getMostUsedItems = () => {
    const itemMap = {};
    orders.forEach((order) => {
      order.items.forEach((item) => {
        itemMap[item.name] = (itemMap[item.name] || 0) + item.quantity;
      });
    });
    return itemMap;
  };

  const getMostUsedIngredients = () => {
    const ingredientMap = {};
    orders.forEach((order) => {
      order.items.forEach((item) => {
        item.ingredients.forEach((ingredient) => {
          ingredientMap[ingredient.name] =
            (ingredientMap[ingredient.name] || 0) + 1;
        });
      });
    });
    return ingredientMap;
  };

  const barData = {
    labels: getOrderDates(),
    datasets: [
      {
        label: "Total Order Cost",
        data: getTotalCostData(),
        backgroundColor: "rgba(54, 162, 235, 0.6)",
      },
    ],
  };

  const pieData = {
    labels: getDriverData().map((d) => d.driver),
    datasets: [
      {
        label: "Number of Orders Delivered by Driver",
        data: getDriverData().map((d) => d.count),
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
        ],
      },
    ],
  };

  const monthlyReport = {
    labels: Object.keys(getMonthlyData()),
    datasets: [
      {
        label: "Monthly Total Cost",
        data: Object.values(getMonthlyData()),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
      },
    ],
  };

  const annualReport = {
    labels: Object.keys(getAnnualData()),
    datasets: [
      {
        label: "Annual Total Cost",
        data: Object.values(getAnnualData()),
        backgroundColor: "rgba(153, 102, 255, 0.6)",
      },
    ],
  };

  const totalCostPerCustomer = {
    labels: Object.keys(getTotalCostPerCustomer()),
    datasets: [
      {
        label: "Total Cost per Customer",
        data: Object.values(getTotalCostPerCustomer()),
        backgroundColor: "rgba(255, 159, 64, 0.6)",
      },
    ],
  };

  const genderData = {
    labels: Object.keys(getGenderData()),
    datasets: [
      {
        label: "Gender Distribution",
        data: Object.values(getGenderData()),
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
        ],
      },
    ],
  };

  const ageData = {
    labels: Object.keys(getAgeData()),
    datasets: [
      {
        label: "Age Distribution",
        data: Object.values(getAgeData()),
        backgroundColor: [
          "rgba(153, 102, 255, 0.6)",
          "rgba(255, 159, 64, 0.6)",
          "rgba(75, 192, 192, 0.6)",
          "rgba(255, 205, 86, 0.6)",
        ],
      },
    ],
  };

  const locationData = {
    labels: Object.keys(getLocationData()),
    datasets: [
      {
        label: "Orders by Location",
        data: Object.values(getLocationData()),
        backgroundColor: "rgba(54, 162, 235, 0.6)",
      },
    ],
  };

  const itemData = {
    labels: Object.keys(getMostUsedItems()),
    datasets: [
      {
        label: "Most Ordered Items",
        data: Object.values(getMostUsedItems()),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
      },
    ],
  };

  const ingredientData = {
    labels: Object.keys(getMostUsedIngredients()),
    datasets: [
      {
        label: "Most Used Ingredients",
        data: Object.values(getMostUsedIngredients()),
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(75, 192, 192, 0.6)",
        ],
      },
    ],
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-4">Admin Records</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white shadow-lg rounded-lg p-4">
          <h2 className="text-2xl font-bold mb-2">Monthly Earnings</h2>
          <Bar data={monthlyReport} />
        </div>

        <div className="bg-white shadow-lg rounded-lg p-4">
          <h2 className="text-2xl font-bold mb-2">Annual Earnings</h2>
          <Bar data={annualReport} />
        </div>

        <div className="bg-white shadow-lg rounded-lg p-4">
          <h2 className="text-2xl font-bold mb-2">
            Total Earnings per Customer
          </h2>
          <Bar data={totalCostPerCustomer} />
        </div>

        <div className="bg-white shadow-lg rounded-lg p-4">
          <h2 className="text-2xl font-bold mb-2">Total Earnings of Orders</h2>
          <Bar data={barData} />
        </div>

        <div className="bg-white shadow-lg rounded-lg p-4">
          <h2 className="text-2xl font-bold mb-2">
            Orders Delivered by Driver
          </h2>
          <Pie data={pieData} />
        </div>

        <div className="bg-white shadow-lg rounded-lg p-4">
          <h2 className="text-2xl font-bold mb-2">Gender Distribution</h2>
          <Doughnut data={genderData} />
        </div>

        <div className="bg-white shadow-lg rounded-lg p-4">
          <h2 className="text-2xl font-bold mb-2">Age Distribution</h2>
          <Bar data={ageData} />
        </div>

        <div className="bg-white shadow-lg rounded-lg p-4">
          <h2 className="text-2xl font-bold mb-2">Orders by Location</h2>
          <Bar data={locationData} />
        </div>

        <div className="bg-white shadow-lg rounded-lg p-4">
          <h2 className="text-2xl font-bold mb-2">Most Ordered Items</h2>
          <Bar data={itemData} />
        </div>

        <div className="bg-white shadow-lg rounded-lg p-4">
          <h2 className="text-2xl font-bold mb-2">Most Used Ingredients</h2>
          <Pie data={ingredientData} />
        </div>
      </div>
    </div>
  );
};
export default AdminRecords;
