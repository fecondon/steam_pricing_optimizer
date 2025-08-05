import React, { useEffect, useState } from 'react';

export default function GameSelector({ onSelect }) {
    const [games, setGames] = useState([]);
    const [selected, setSelected] = useState('');

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
    };

    return (
        <div className="mb-4">
            <label className="block text-lg font-medium text-gray-700 mb-1">Select Game:</label>
            <select
            className="w-full p-2 border rounded"
            value={selected}
            onChange={handleChange}
            >
                <option value="">-- Choose a game --</option>
                {games.map((title, i) => (
                    <option key={i} value={title}>{title}</option>
                ))}
            </select>
        </div>
    );
}