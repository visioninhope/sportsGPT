// components/InputForm.tsx
import type { NextPage } from 'next';
import React, { useState } from 'react';
import InputForm from '../components/InputForm';

const Input: NextPage = () => {
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
            <InputForm onSubmit={handleFormSubmit}></InputForm>
                <div className="mt-4">
                    <p className="text-gray-700">{response}</p>
                </div>
                <button
                type="submit"
                className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
                Submit
            </button>
         </div>
    );
};

export default Input;
