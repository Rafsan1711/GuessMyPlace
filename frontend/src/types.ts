/**
 * Type definitions for GuessMyPlace
 */

export type Category = 'country' | 'city' | 'historic_place';

export type AnswerType = 'yes' | 'no' | 'dont_know' | 'probably' | 'probably_not';

export interface Place {
  id: string;
  name: string;
  category: Category;
  description?: string;
  image_url?: string;
  characteristics: Record<string, any>;
}

export interface Question {
  id: string;
  text: string;
  characteristic: string;
  expected_value: any;
  category: Category | 'all';
}

export interface Statistics {
  total_games: number;
  correct_guesses: number;
  accuracy: number;
  avg_questions: number;
  category_breakdown?: {
    country: number;
    city: number;
    historic_place: number;
  };
}