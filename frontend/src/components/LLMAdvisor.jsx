import React, { useState } from 'react';

export default function LLMAdvisor({ game, revenue }) {
    const [advice, setAdvice] = useState('');
    const [loading, setLoading] = useState(false);

    const getAdvice = async () => {
        setLoading(true);
        setAdvice('');

        const optimalIndex = revenue.revenues.indexOf(Math.max(...revenue.revenues));
        const optimalPrice = revenue.pricePoints[optimalIndex];
        const optimalRevenue = revenue.revenues[optimalIndex];

        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}/recommend`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: game,
                    discount_percent: 0.25,
                    conversion_prob: 0.18,
                    shap_uplift: 0.03,
                    is_new_release: 0,
                    optimalPrice: optimalPrice,
                    optimalRevenue: optimalRevenue
                })
            });

            const json = await res.json();
            if ( json.recommendation ) {
                setAdvice(json.recommendation);
            } else {
                setAdvice('Failed to get a recommendation')
            }
        } catch (err) {
            setAdvice('Error: ${err.message}')
        }

        setLoading(false);
    };

    return (
        <div className="my-4">
            <button
            onClick={getAdvice}
            className="bg-gradient-to-r from-purple-500 to-indigo-600 text-white px-4 py-2 rounded hover:opacity-90"
            >Get LLM Pricing Advice
            </button>
            {loading && <p className="mt-2 text-gray-600">Generating suggestion...</p>}
            {advice && (<div className="mt-4 p-4 border rounded bg-white shadow">
                <h3 className="font-bold text-lg mb-1">LLM Suggestion</h3>
                <p>{advice}</p>
            </div>)}
        </div>
    );
}