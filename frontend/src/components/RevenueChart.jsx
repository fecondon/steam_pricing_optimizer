import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

export default function RevenueChart({ game, onSimulated }) {
    const chartRef = useRef(null);
    const chartInstance = useRef(null);

    useEffect(() => {
        if (!game) return;

        // Simulate revenue curve
        const pricePoints = Array.from({ length: 20 }, (_, i) => (i + 1) * 1.0);
        const baseConversion = 0.05;
        const elasticity = -0.15;
        const revenues = pricePoints.map(p => p * (baseConversion * Math.exp(elasticity * p)));

        // Pass back to parent for LLM use
        onSimulated({ pricePoints, revenues });

        if (chartInstance.current) {
            chartInstance.current.destroy();
        }

        const ctx = chartRef.current.getContext("2d");
        chartInstance.current = new Chart(ctx, {
            type: "line",
            data: {
                labels: pricePoints,
                datasets: [{
                    label: 'Simulated Revenue for {game}',
                    data: revenues,
                    fill: false,
                    borderColor: "#3b82f6",
                    tension: 0.1,
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true },
                },
                scales: {
                    x: { title: { display: true, text: "Price ($)" } },
                    y: { title: { display: true, text: "Revenue ($)" } },
                },
            },
        });
    }, [game]);

    return <canvas ref={chartRef} className="w-full h-64 my-4" />;
}