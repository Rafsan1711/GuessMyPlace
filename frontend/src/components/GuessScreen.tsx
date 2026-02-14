import React, { useState } from 'react';
import { Place } from '../services/api';
import { ThumbsUp, ThumbsDown } from 'lucide-react';

interface GuessScreenProps {
  place: Place;
  onConfirm: (correct: boolean, actualPlace?: string) => void;
}

const GuessScreen: React.FC<GuessScreenProps> = ({ place, onConfirm }) => {
  const [showWrongInput, setShowWrongInput] = useState(false);
  const [actualPlace, setActualPlace] = useState('');

  const handleCorrect = () => {
    onConfirm(true);
  };

  const handleWrong = () => {
    setShowWrongInput(true);
  };

  const handleSubmitWrong = () => {
    if (actualPlace.trim()) {
      onConfirm(false, actualPlace.trim());
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto bg-white rounded-3xl shadow-2xl overflow-hidden animate-scale-in">
      <div className="relative h-64">
        <img 
          src={place.image_url || `https://picsum.photos/seed/${place.name}/800/600`}
          alt={place.name} 
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent flex items-end p-8">
          <div className="text-white">
            <p className="uppercase tracking-widest text-xs font-bold text-blue-400 mb-1">
              My Guess is...
            </p>
            <h2 className="text-4xl font-extrabold">{place.name}</h2>
          </div>
        </div>
      </div>

      <div className="p-8">
        {!showWrongInput ? (
          <>
            <p className="text-gray-600 text-lg mb-10 leading-relaxed">
              {place.description || `I think you're thinking of ${place.name}!`}
            </p>

            <h3 className="text-xl font-bold text-gray-800 mb-6 text-center">
              Is this correct?
            </h3>
            
            <div className="grid grid-cols-2 gap-4">
              <button 
                onClick={handleCorrect}
                className="flex items-center justify-center gap-2 bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-5 rounded-2xl transition-all active:scale-95"
              >
                <ThumbsUp className="w-6 h-6" />
                Yes, you're right!
              </button>
              <button 
                onClick={handleWrong}
                className="flex items-center justify-center gap-2 bg-rose-500 hover:bg-rose-600 text-white font-bold py-5 rounded-2xl transition-all active:scale-95"
              >
                <ThumbsDown className="w-6 h-6" />
                No, that's wrong
              </button>
            </div>
          </>
        ) : (
          <div className="space-y-6">
            <h3 className="text-xl font-bold text-gray-800 text-center">
              What were you thinking of?
            </h3>
            
            <input
              type="text"
              value={actualPlace}
              onChange={(e) => setActualPlace(e.target.value)}
              placeholder="Enter the place name..."
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none text-lg"
              autoFocus
            />

            <button
              onClick={handleSubmitWrong}
              disabled={!actualPlace.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-bold py-4 rounded-2xl transition-all active:scale-95"
            >
              Submit
            </button>

            <p className="text-sm text-gray-500 text-center">
              I'll learn from this to improve! 🧠
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default GuessScreen;