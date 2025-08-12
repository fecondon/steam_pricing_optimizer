import React, { useState, useEffect } from 'react';
import './App.css';
import './index.css';
import GameSelector from './components/GameSelector';
import RevenueChart from './components/RevenueChart';
import LLMAdvisor from './components/LLMAdvisor';

export default function App() {
  const [game, setGame] = useState(null);
  const [revenue, setRevenue] = useState(null);

  const handleGameSelect = (game) => {
    setGame(game);
  };

  const handleSetRevenue = (revenue) => {
    console.log("App.jsx received revenue: ", revenue);
    setRevenue(revenue);
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <h1 className="text-3x1 font-bold text-center mb-4">🎮 Steam Price Optimizer</h1>
      <GameSelector onSelect={handleGameSelect} onRevenue={handleSetRevenue} />

      { revenue && (
        <>
        <div className="max-w-3xl mx-auto flex flex-col items-center space-y-8 mt-8 border border-red-400 bg-white p-4 relative">
          { /* Chart */ }
          <div className="w-full max-w-2xl" >
            <RevenueChart revenueData={revenue} />
          </div>
        </div>
          { /* Floating Button */}
          <div className="fixed bottom-6 right-6 z-50 p-4" style={{ padding: '48px' }} >
            <LLMAdvisor game={game} revenue={revenue} />
          </div>
        </>
      )}
    </div>
  );
}