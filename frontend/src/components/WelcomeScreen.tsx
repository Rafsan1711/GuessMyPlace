import React from 'react';
import { Globe, Building2, Landmark } from 'lucide-react';

type Category = 'country' | 'city' | 'historic_place';

interface WelcomeScreenProps {
  onStart: (category: Category) => void;
  stats: {
    total_games?: number;
    accuracy?: number;
    gamesPlayed?: number;
  };
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onStart, stats }) => {
  const totalGames = stats.total_games || stats.gamesPlayed || 0;
  const accuracy = stats.accuracy || 0;

  return (
    <div className="flex flex-col items-center justify-center p-6 text-center animate-fade-in">
      <div className="mb-8 animate-float">
        <Globe className="w-24 h-24 text-blue-500 mx-auto" />
      </div>
      
      <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">
        GuessMyPlace
      </h1>
      
      <p className="text-gray-300 text-lg mb-10 max-w-md mx-auto">
        I can guess any Country, City, or Historic Place you're thinking of. 
        Think of one and let's begin!
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-3xl mb-12">
        <button 
          onClick={() => onStart('country')}
          className="bg-white/10 hover:bg-white/20 text-white p-6 rounded-2xl flex flex-col items-center gap-3 border border-white/5 transition-all group active:scale-95"
        >
          <div className="p-3 bg-blue-500/20 rounded-xl group-hover:scale-110 transition-transform">
            <Globe className="w-8 h-8 text-blue-400" />
          </div>
          <span className="font-bold text-lg">Countries</span>
        </button>

        <button 
          onClick={() => onStart('city')}
          className="bg-white/10 hover:bg-white/20 text-white p-6 rounded-2xl flex flex-col items-center gap-3 border border-white/5 transition-all group active:scale-95"
        >
          <div className="p-3 bg-emerald-500/20 rounded-xl group-hover:scale-110 transition-transform">
            <Building2 className="w-8 h-8 text-emerald-400" />
          </div>
          <span className="font-bold text-lg">Cities</span>
        </button>

        <button 
          onClick={() => onStart('historic_place')}
          className="bg-white/10 hover:bg-white/20 text-white p-6 rounded-2xl flex flex-col items-center gap-3 border border-white/5 transition-all group active:scale-95"
        >
          <div className="p-3 bg-amber-500/20 rounded-xl group-hover:scale-110 transition-transform">
            <Landmark className="w-8 h-8 text-amber-400" />
          </div>
          <span className="font-bold text-lg">Historic Places</span>
        </button>
      </div>

      <div className="flex gap-10 text-gray-400 font-medium">
        <div>
          <span className="block text-white text-2xl font-bold">{totalGames}</span>
          <span className="text-sm">Games Played</span>
        </div>
        <div>
          <span className="block text-white text-2xl font-bold">{accuracy.toFixed(0)}%</span>
          <span className="text-sm">Success Rate</span>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;