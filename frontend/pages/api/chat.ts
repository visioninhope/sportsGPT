// pages/api/chat.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { readFileSync } from 'fs';
import parse from 'csv-parse/lib/sync';
import { OpenAIApi, Configuration } from 'openai';
import path from 'path';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
    const { prompt }: { prompt: string } = req.body;

    // Generate the current date string in YYYY-MM-DD format
    const currentDate = new Date().toISOString().split('T')[0];
    const csvFileName = `${currentDate}.csv`;

    // Define the path to the CSV file
    // Update this path according to your project structure
    const csvFilePath = path.join(process.cwd(), 'path/to/csv/directory', csvFileName);

    try {
        // Read and parse the CSV file
        const fileContent = readFileSync(csvFilePath, 'utf-8');
        const records = parse(fileContent, { columns: true });

        // Example logic to use CSV data with the prompt
        const csvDataString = records.map(record => JSON.stringify(record)).join('\n');
        const combinedPrompt = `${csvDataString}\n\n${prompt}`;

        // Configure OpenAI
        const configuration = new Configuration({
            apiKey: process.env.OPENAI_API_KEY,
        });
        const openai = new OpenAIApi(configuration);

        const response = await openai.createCompletion("text-davinci-003", {
            prompt: combinedPrompt,
            max_tokens: 150,
        });

        res.status(200.json({ answer: response.data.choices[0].text }));
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "An error occurred while processing the request" });
    }
}
