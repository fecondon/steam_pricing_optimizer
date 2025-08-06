import React, { useState, useEffect } from 'react';
import './App.css';
import GameSelector from './components/GameSelector';
import RevenueChart from './components/RevenueChart';
import LLMAdvisor from './components/LLMAdvisor';

export default function App() {
  const [game, setGames] = useState(null);
  const [revenue, setRevenue] = useState(null);

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <h1 className="text-3x1 font-bold text-center mb-4">🎮 Steam Price Optimizer</h1>
      <GameSelector onSelect={setGames} />
      {game && <RevenueChart game={game} onSimulated={setRevenue} />}
      {game && revenue && <LLMAdvisor game={game} revenue={revenue} />}
    </div>
  );
}