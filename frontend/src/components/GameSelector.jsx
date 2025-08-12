import React, { useEffect, useState } from 'react';

export default function GameSelector({ onSelect, onRevenue }) {
    const [games, setGames] = useState([]);
    const [selected, setSelected] = useState('');
    const [loading, setLoading] = useState(false);
    const [revenue, setRevenue] = useState(null);

    // Fetch the game list from /games API
    useEffect(() => {
        fetch(`${import.meta.env.VITE_API_URL}/games`)
        .then((res) => res.json())
        .then((data) => setGames(data))
        .catch((err) => {
            console.error("Failed to fetch games", err);
            setGames([]);
        });
    }, []);

    const handleChange = (e) => {
        const game = e.target.value;
        setSelected(game);
        onSelect(game); // pass to parent

        // Fetch simulation data for selected game
        fetch(`${import.meta.env.VITE_API_URL}/simulate`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ title: game })
        })
            .then((res) => res.json())
            .then((data) => {
                if (Array.isArray(data) && data.length > 0) {
                    const revenueObj = ({
                        revenue: data.map(d => d.revenue ?? d.expected_revenue ?? 0),
                        price: data.map(d => d.price ?? 0),
                        conversion_prob: data.map(d => d.conversion_prob ?? 0),
                    });
                    setRevenue(revenueObj);
                    onRevenue(revenueObj);
                } else {
                    setRevenue(null);
                    onRevenue(null);
                }
                setLoading(false);
            })
            .catch((err) => {
                console.error("Failed to fetch simulation", err);
                setLoading(false);
            });
    };

    return (
        <div className="mb-4">
            <label htmlFor="gameSelect" className="block text-lg font-medium text-gray-700 mb-1">Select Game:</label>
            <select
            id="gameSelect"
            className="w-full p-2 border rounded"
            value={selected}
            onChange={handleChange}
            >
                <option value="">-- Choose a game --</option>
                {games.map((title, i) => (
                    <option key={i} value={title}>{title}</option>
                ))}
            </select>
            {loading && <p className="mt-2 text-gray-600">Loading simulation...</p>}
        </div>
    );
}