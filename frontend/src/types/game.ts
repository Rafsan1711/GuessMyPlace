export interface Question {
  id: string
  text: string
  question_number: number
  total_questions_asked: number
}

export interface Place {
  id: string
  name: string
  type: string
  details?: Record<string, any>
  image_url?: string
}

export interface GameState {
  sessionId: string | null
  currentQuestion: Question | null
  isGuessing: boolean
  guess: Place | null
  isLoading: boolean
}

export type Answer = 'yes' | 'no' | 'dont_know' | 'probably' | 'probably_not'