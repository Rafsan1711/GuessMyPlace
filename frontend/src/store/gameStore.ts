import { create } from 'zustand'
import { GameState, Question, Place, Answer } from '@/types/game'
import { gameApi } from '@/services/api'

interface GameStore extends GameState {
  startGame: () => Promise<void>
  submitAnswer: (answer: Answer) => Promise<void>
  validateGuess: (correct: boolean) => Promise<void>
  reset: () => void
}

export const useGameStore = create<GameStore>((set, get) => ({
  sessionId: null,
  currentQuestion: null,
  isGuessing: false,
  guess: null,
  isLoading: false,

  startGame: async () => {
    set({ isLoading: true })
    try {
      const response = await gameApi.startGame()
      set({
        sessionId: response.data.session_id,
        currentQuestion: response.data.question,
        isGuessing: false,
        guess: null,
        isLoading: false,
      })
    } catch (error) {
      console.error('Failed to start game:', error)
      set({ isLoading: false })
    }
  },

  submitAnswer: async (answer: Answer) => {
    const { sessionId } = get()
    if (!sessionId) return

    set({ isLoading: true })
    try {
      const response = await gameApi.submitAnswer(sessionId, answer)
      
      if (response.data.type === 'guess') {
        set({
          isGuessing: true,
          guess: response.data.guess,
          currentQuestion: null,
          isLoading: false,
        })
      } else {
        set({
          currentQuestion: response.data.question,
          isLoading: false,
        })
      }
    } catch (error) {
      console.error('Failed to submit answer:', error)
      set({ isLoading: false })
    }
  },

  validateGuess: async (correct: boolean) => {
    const { sessionId } = get()
    if (!sessionId) return

    set({ isLoading: true })
    try {
      await gameApi.validateGuess(sessionId, correct)
      set({ isLoading: false })
    } catch (error) {
      console.error('Failed to validate guess:', error)
      set({ isLoading: false })
    }
  },

  reset: () => {
    set({
      sessionId: null,
      currentQuestion: null,
      isGuessing: false,
      guess: null,
      isLoading: false,
    })
  },
}))