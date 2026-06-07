import { OpenAI } from 'openai';

export function createOpenAIClient(apiKey?: string): OpenAI | null {
  try {
    if (!apiKey || apiKey === 'dummy-key-for-now') {
      console.log('OpenAI API key not available, using mock mode');
      return null;
    }
    return new OpenAI({ apiKey });
  } catch (error) {
    console.error('Failed to create OpenAI client:', error);
    return null;
  }
}