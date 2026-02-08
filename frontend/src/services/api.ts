import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const gameApi = {
  startGame: async (language = 'en', category = 'all') => {
    const { data } = await api.post('/api/game/start', { language, category })
    return data
  },

  submitAnswer: async (sessionId: string, answer: string) => {
    const { data } = await api.post('/api/game/answer', { session_id: sessionId, answer })
    return data
  },

  validateGuess: async (sessionId: string, correct: boolean, actualPlaceId?: string) => {
    const { data } = await api.post('/api/game/guess', { 
      session_id: sessionId, 
      correct,
      actual_place_id: actualPlaceId 
    })
    return data
  },
}

export default api