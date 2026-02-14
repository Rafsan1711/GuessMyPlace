import React, { useEffect, useState } from 'react';
import { Place } from '../types';
import { RotateCcw, Home, Sparkles, AlertCircle } from 'lucide-react';

interface ResultScreenProps {
  isCorrect: boolean;
  guessedPlace: Place | null;
  questionCount: number;
  onRestart: () => void;
  onHome: () => void;
}

const ResultScreen: React.FC<ResultScreenProps> = ({ 
  isCorrect, 
  guessedPlace, 
  questionCount, 
  onRestart, 
  onHome 
}) => {
  const [showConfetti, setShowConfetti] = useState(false);

  useEffect(() => {
    if (isCorrect) {
      setShowConfetti(true);
    }
  }, [isCorrect]);

  return (
    <div className="flex flex-col items-center justify-center w-full max-w-2xl animate-fade-in p-6 text-center">
      <div className="mb-8">
        {isCorrect ? (
          <div className="relative">
            <div className="p-6 bg-emerald-500 rounded-full animate-bounce">
              <Sparkles className="w-16 h-16 text-white" />
            </div>
            {showConfetti && (
              <div className="absolute -inset-4 z-[-1] animate-pulse opacity-50 bg-emerald-400 blur-3xl rounded-full" />
            )}
          </div>
        ) : (
          <div className="p-6 bg-rose-500 rounded-full">
            <AlertCircle className="w-16 h-16 text-white" />
          </div>
        )}
      </div>

      <h2 className="text-4xl font-extrabold text-white mb-4">
        {isCorrect ? "I Knew It!" : "Aww, You Stumped Me!"}
      </h2>

      <p className="text-gray-300 text-xl mb-12">
        {isCorrect 
          ? `I guessed ${guessedPlace?.name} in just ${questionCount} questions.` 
          : "Your choice was too hard for my current brain. I will learn from this!"}
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-md">
        <button 
          onClick={onRestart}
          className="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-8 rounded-2xl transition-all active:scale-95"
        >
          <RotateCcw className="w-5 h-5" />
          Play Again
        </button>
        <button 
          onClick={onHome}
          className="flex items-center justify-center gap-2 bg-white/10 hover:bg-white/20 text-white font-bold py-4 px-8 rounded-2xl transition-all active:scale-95 border border-white/5"
        >
          <Home className="w-5 h-5" />
          Main Menu
        </button>
      </div>
    </div>
  );
};

export default ResultScreen;