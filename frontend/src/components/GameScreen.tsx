import React from 'react';
import { Question, AnswerType } from '../types';
import ProgressBar from './ProgressBar';
import { ChevronLeft, Info } from 'lucide-react';

interface GameScreenProps {
  question: Question | null;
  count: number;
  remainingCount: number;
  onAnswer: (answer: AnswerType) => void;
  onBack: () => void;
}

const GameScreen: React.FC<GameScreenProps> = ({ 
  question, 
  count, 
  remainingCount, 
  onAnswer, 
  onBack 
}) => {
  if (!question) return null;

  return (
    <div className="w-full max-w-xl mx-auto bg-white rounded-3xl shadow-2xl overflow-hidden animate-fade-in">
      <div className="bg-slate-50 p-6 border-b border-gray-100">
        <div className="flex justify-between items-center mb-4">
          <button 
            onClick={onBack}
            className="p-2 hover:bg-gray-200 rounded-full transition-colors text-gray-500"
          >
            <ChevronLeft className="w-6 h-6" />
          </button>
          <span className="text-gray-400 font-semibold uppercase tracking-wider text-xs">
            Question {count}
          </span>
          <div className="w-10"></div>
        </div>
        <ProgressBar current={count} total={20} />
      </div>

      <div className="p-8 md:p-12">
        <h2 className="text-2xl md:text-3xl font-bold text-slate-800 text-center mb-12 min-h-[5rem] flex items-center justify-center">
          {question.text}
        </h2>

        <div className="grid grid-cols-1 gap-3">
          <button 
            onClick={() => onAnswer('yes')}
            className="bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-4 rounded-xl transition-all active:scale-95"
          >
            Yes
          </button>
          <button 
            onClick={() => onAnswer('no')}
            className="bg-rose-500 hover:bg-rose-600 text-white font-bold py-4 rounded-xl transition-all active:scale-95"
          >
            No
          </button>
          
          <div className="grid grid-cols-2 gap-3">
            <button 
              onClick={() => onAnswer('probably')}
              className="bg-emerald-100 hover:bg-emerald-200 text-emerald-700 font-semibold py-4 rounded-xl transition-all active:scale-95"
            >
              Probably
            </button>
            <button 
              onClick={() => onAnswer('probably_not')}
              className="bg-rose-100 hover:bg-rose-200 text-rose-700 font-semibold py-4 rounded-xl transition-all active:scale-95"
            >
              Probably Not
            </button>
          </div>
          
          <button 
            onClick={() => onAnswer('dont_know')}
            className="bg-gray-100 hover:bg-gray-200 text-gray-600 font-semibold py-4 rounded-xl transition-all active:scale-95"
          >
            I don't know
          </button>
        </div>
      </div>

      <div className="bg-slate-50 p-4 text-center border-t border-gray-100">
        <p className="text-sm text-gray-400 flex items-center justify-center gap-1">
          <Info className="w-4 h-4" />
          {remainingCount} possibilities remaining
        </p>
      </div>
    </div>
  );
};

export default GameScreen;