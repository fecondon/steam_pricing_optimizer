import React from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";


export default function RevenueChart({ revenueData }) {
    console.log("RevenueChart props:", revenueData);
    if (
        !revenueData ||
        !Array.isArray(revenueData.price) ||
        !Array.isArray(revenueData.revenue) ||
        !Array.isArray(revenueData.conversion_prob) 
    ) {
        return <p className="mt-4">Select a game to see its revenue curve.</p>;
    }

    const chartData = {
        labels: revenueData.price.map((p) => p.toFixed(2)),
        datasets: [
            {
                label: "Revenue ($)",
                data: revenueData.revenue,
                fill: false,
                borderColor: "rgb(75, 192, 192)",
                tension: 0.1
            },
            {
                label: "Conversion Probability",
                data: revenueData.conversion_prob.map((c) => c * Math.max(...revenueData.revenue)),
                fill: false,
                borderColor: "rgb(255, 99, 132)",
                tension: 0.1,
                yAxisID: "y2"
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        interaction: { mode: "index", intersect: false },
        scales: {
            y: {
                beginAtZero: true,
                title: { display: true, text: "Revenue ($)"},
            },
            y2: {
                beginAtZero: true,
                position: "right",
                title: { display: true, text: "Conversion Probability"},
            },
        },
    };

    return (
        <div className="w-full max-w-4xl mx-auto bg-white p-4 rounded-lg shadow-lg overflow-hidden" style={{ height: "400px" }}>
            <h2 className="text-lg font-bold mg-2">Revenue Curve</h2>
            <div className="w-full h-96 overflow-hidden" >
                <Line data={chartData} options={chartOptions}/>
            </div>
        </div>
    );
}