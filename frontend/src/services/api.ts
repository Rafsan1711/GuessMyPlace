/**
 * API Service for GuessMyPlace Backend
 */

import { Place, Question, Category, AnswerType, Statistics } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface StartGameResponse {
  session_id: string;
  category: string;
  question: Question;
  remaining_count: number;
  question_count: number;
}

export interface AnswerResponse {
  type: 'question' | 'guess' | 'no_match';
  session_id: string;
  question?: Question;
  guessed_place?: Place;
  remaining_count?: number;
  question_count?: number;
  total_questions?: number;
  message?: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  /**
   * Start a new game session
   */
  async startGame(category: Category): Promise<StartGameResponse> {
    return this.request<StartGameResponse>('/api/game/start', {
      method: 'POST',
      body: JSON.stringify({ category }),
    });
  }

  /**
   * Submit an answer to the current question
   */
  async submitAnswer(
    sessionId: string,
    questionId: string,
    answer: AnswerType
  ): Promise<AnswerResponse> {
    return this.request<AnswerResponse>('/api/game/answer', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        question_id: questionId,
        answer,
      }),
    });
  }

  /**
   * Submit feedback on the guess
   */
  async submitFeedback(
    sessionId: string,
    isCorrect: boolean,
    actualPlaceName?: string
  ): Promise<{ status: string; message: string }> {
    return this.request('/api/game/feedback', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        is_correct: isCorrect,
        actual_place_name: actualPlaceName,
      }),
    });
  }

  /**
   * Get game statistics
   */
  async getStatistics(): Promise<Statistics> {
    return this.request<Statistics>('/api/stats');
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string }> {
    return this.request('/api/health');
  }
}

export const api = new ApiService();
export { Place, Question, Category, AnswerType, Statistics };