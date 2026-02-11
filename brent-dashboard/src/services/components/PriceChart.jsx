import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function PriceChart() {
  const [prices, setPrices] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/prices")
      .then((res) => res.json())
      .then((data) => setPrices(data))
      .catch((err) => console.error("Error fetching prices:", err));
  }, []);

  if (prices.length === 0) return <p>Loading chart...</p>;

  const labels = prices.map((p) => p.Date.split("T")[0]);
  const priceData = prices.map((p) => p.Price);

  const data = {
    labels,
    datasets: [
      {
        label: "Brent Price",
        data: priceData,
        borderColor: "steelblue",
        backgroundColor: "rgba(70,130,180,0.3)",
        tension: 0.2,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Brent Oil Prices" },
    },
  };

  return <Line data={data} options={options} />;
}

export default PriceChart;
