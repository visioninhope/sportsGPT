// pages/api/chat.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { readFileSync } from 'fs';
import parse from 'csv-parse/lib/sync';
import { OpenAIApi, Configuration } from 'openai';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
    const { prompt }: { prompt: string } = req.body;

    // Read and parse the CSV file
    const fileContent = readFileSync('path/to/your/csv.csv', 'utf-8');
    const records = parse(fileContent, { columns: true });

    // Example logic to use CSV data with the prompt
    // This is a placeholder. You should replace it with your own logic.
    const csvDataString = records.map(record => JSON.stringify(record)).join('\n');
    const combinedPrompt = `${csvDataString}\n\n${prompt}`;

    // Configure OpenAI
    const configuration = new Configuration({
        apiKey: process.env.OPENAI_API_KEY,
    });
    const openai = new OpenAIApi(configuration);

    try {
        const response = await openai.createCompletion("text-davinci-003", {
            prompt: combinedPrompt,
            max_tokens: 150,
        });

        res.status(200).json({ answer: response.data.choices[0].text });
    } catch (error) {
        res.status(500).json({ error: "OpenAI request failed" });
    }
}
