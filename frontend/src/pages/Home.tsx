import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function Home() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center text-white"
      >
        <h1 className="text-6xl font-bold mb-4">🌍 GuessMyPlace</h1>
        <p className="text-xl mb-8">Think of a place, I'll guess it!</p>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => navigate('/game')}
          className="bg-white text-blue-600 px-8 py-4 rounded-full text-xl font-semibold shadow-lg hover:shadow-xl transition-shadow"
        >
          Start Game
        </motion.button>
      </motion.div>
    </div>
  )
}