// components/InputForm.tsx
import React, { useState } from 'react';

interface InputFormProps {
  onSubmit: (input: string) => void;
}

const InputForm: React.FC<InputFormProps> = ({ onSubmit }) => {
    const [input, setInput] = useState('');

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        onSubmit(input);
    };

    return (
        <form onSubmit={handleSubmit} className="mt-4">
            <label htmlFor="userInput" className="block text-sm font-medium text-gray-700">
                What data would you like to see?
            </label>
            <div className="mt-1 ml-4">
                <input
                    type="text"
                    id="userInput"
                    placeholder='What stat do you want to see?'
                    className="shadow-sm pl-4 focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}

                />
            </div>
             <button
                type="submit"
                className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
                Submit
            </button>
        </form>
    );
};

export default InputForm;
