import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useGameStore } from '@/store/gameStore'
import { Answer } from '@/types/game'

export default function Game() {
  const navigate = useNavigate()
  const { 
    currentQuestion, 
    isGuessing, 
    guess, 
    isLoading, 
    startGame, 
    submitAnswer, 
    validateGuess,
    reset 
  } = useGameStore()

  useEffect(() => {
    startGame()
  }, [])

  const handleAnswer = (answer: Answer) => {
    submitAnswer(answer)
  }

  const handlePlayAgain = () => {
    reset()
    startGame()
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-2xl text-gray-600">Loading...</div>
      </div>
    )
  }

  if (isGuessing && guess) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-500 to-teal-600 flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white rounded-2xl p-8 max-w-md w-full shadow-2xl"
        >
          <h2 className="text-3xl font-bold mb-4 text-center">Is it...</h2>
          <h1 className="text-5xl font-bold text-center text-blue-600 mb-6">{guess.name}?</h1>
          
          <div className="flex gap-4">
            <button
              onClick={() => { validateGuess(true); handlePlayAgain() }}
              className="flex-1 bg-green-500 text-white py-3 rounded-lg font-semibold hover:bg-green-600"
            >
              Yes! 🎉
            </button>
            <button
              onClick={() => { validateGuess(false); handlePlayAgain() }}
              className="flex-1 bg-red-500 text-white py-3 rounded-lg font-semibold hover:bg-red-600"
            >
              No
            </button>
          </div>
          
          <button
            onClick={() => navigate('/')}
            className="w-full mt-4 text-gray-600 hover:text-gray-800"
          >
            Exit Game
          </button>
        </motion.div>
      </div>
    )
  }

  if (currentQuestion) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <motion.div
          key={currentQuestion.id}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-2xl p-8 max-w-2xl w-full shadow-xl"
        >
          <div className="mb-6">
            <span className="text-sm text-gray-500">Question {currentQuestion.question_number}</span>
          </div>
          
          <h2 className="text-3xl font-bold mb-8 text-center">{currentQuestion.text}</h2>
          
          <div className="space-y-3">
            <button
              onClick={() => handleAnswer('yes')}
              className="w-full bg-green-500 text-white py-4 rounded-lg text-xl font-semibold hover:bg-green-600 transition"
            >
              Yes
            </button>
            <button
              onClick={() => handleAnswer('probably')}
              className="w-full bg-blue-500 text-white py-4 rounded-lg text-xl font-semibold hover:bg-blue-600 transition"
            >
              Probably
            </button>
            <button
              onClick={() => handleAnswer('dont_know')}
              className="w-full bg-gray-400 text-white py-4 rounded-lg text-xl font-semibold hover:bg-gray-500 transition"
            >
              Don't Know
            </button>
            <button
              onClick={() => handleAnswer('probably_not')}
              className="w-full bg-orange-500 text-white py-4 rounded-lg text-xl font-semibold hover:bg-orange-600 transition"
            >
              Probably Not
            </button>
            <button
              onClick={() => handleAnswer('no')}
              className="w-full bg-red-500 text-white py-4 rounded-lg text-xl font-semibold hover:bg-red-600 transition"
            >
              No
            </button>
          </div>
        </motion.div>
      </div>
    )
  }

  return null
}