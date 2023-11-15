// pages/index.tsx
import type { NextPage } from 'next';
import React, { useState } from 'react';
import InputForm from '../components/InputForm';

const Home: NextPage = () => {
    const [response, setResponse] = useState('');

    const handleFormSubmit = async (input: string) => {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: input }),
        });

        const data = await res.json();
        setResponse(data.answer);
    };

    return (
        <div className="container mx-auto p-4">
            <InputForm onSubmit={handleFormSubmit} />
            <div className="mt-4">
                <p className="text-gray-700">{response}</p>
            </div>
        </div>
    );
};

export default Home;
