import React, { useEffect, useState } from 'react';

const LLMAdvisor = ({ game, revenue }) => {
    const [advice, setAdvice] = useState('');
    const [loading, setLoading] = useState(false);
    const [gameData, setGameData] = useState(null);

    // Fetch game metadata on select
    useEffect(() => {
        const fetchGameData = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/data`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title: game })
                });

                const json = await res.json();
                setGameData(json);
            } catch (err) {
                console.error('❌ Failed to load game data: ', err);
                setGameData(null);
            }
        };

        if (game) {
            fetchGameData();
        }
    }, [game]);

    const getAdvice = async () => {
        if (!gameData) return;

        setLoading(true);
        setAdvice('');

        const optimalIndex = revenue.revenue.indexOf(Math.max(...revenue.revenue));
        const optimalPrice = revenue.price[optimalIndex];
        const optimalRevenue = revenue.revenue[optimalIndex];

        try {

            console.log("Payload: ", {
                title: game,
                discount_percent: gameData.discount_percent,
                conversion_prob: gameData.conversion_prob,
                shap_uplift: gameData.shap_uplift,
                is_new_release: gameData.is_new_release,
                optimal_price: optimalPrice,
                optimal_revenue: optimalRevenue
            });

            const res = await fetch(`${import.meta.env.VITE_API_URL}/recommend`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: gameData.title,
                    discount_percent: gameData.discount_percent,
                    conversion_prob: gameData.conversion_prob,
                    shap_uplift: gameData.shap_uplift,
                    is_new_release: gameData.is_new_release,
                    optimal_price: optimalPrice,
                    optimal_revenue: optimalRevenue
                })
            });

            const json = await res.json();
            if ( json.recommendation ) {
                setAdvice(json.recommendation);
            } else {
                setAdvice('❌ Failed to get a recommendation')
            }
        } catch (err) {
            setAdvice('❌ Error: ${err.message}')
        }

        setLoading(false);
    };

    return (
        <div className="w-full">
        <button
          onClick={getAdvice}
          className="w-full bg-gradient-to-r from-purple-500 to-indigo-600 text-white px-4 py-2 rounded hover:opacity-90 disabled:opacity-50"
          disabled={!gameData || loading}
        >
          {loading ? 'Generating suggestion...' : 'Get LLM Pricing Advice'}
        </button>
  
        {advice && (
          <div
            className="mt-4 p-4 border rounded bg-gray-50 text-gray-800 shadow max-w-xl whitespace-normal break-words"
          >
            <h3 className="font-semibold text-lg mb-2">LLM Suggestion</h3>
            <p>{advice}</p>
          </div>
        )}
      </div>
    );
};

export default LLMAdvisor;