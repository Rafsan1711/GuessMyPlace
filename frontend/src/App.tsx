import React, { useState, useEffect } from 'react';
import WelcomeScreen from './components/WelcomeScreen';
import GameScreen from './components/GameScreen';
import GuessScreen from './components/GuessScreen';
import ResultScreen from './components/ResultScreen';
import { api } from './services/api';
import { Question, Place, Statistics, Category, AnswerType } from './types';

type Screen = 'welcome' | 'playing' | 'guessing' | 'result';

interface GameState {
  screen: Screen;
  category: Category | null;
  sessionId: string | null;
  currentQuestion: Question | null;
  questionCount: number;
  remainingCount: number;
  guessedPlace: Place | null;
  stats: Statistics | null;
}

const App: React.FC = () => {
  const [gameState, setGameState] = useState<GameState>({
    screen: 'welcome',
    category: null,
    sessionId: null,
    currentQuestion: null,
    questionCount: 0,
    remainingCount: 0,
    guessedPlace: null,
    stats: null
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load statistics on mount
  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const stats = await api.getStatistics();
      setGameState(prev => ({ ...prev, stats }));
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  const startGame = async (category: Category) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.startGame(category);
      
      setGameState({
        screen: 'playing',
        category,
        sessionId: response.session_id,
        currentQuestion: response.question,
        questionCount: 1,
        remainingCount: response.remaining_count,
        guessedPlace: null,
        stats: gameState.stats
      });
    } catch (err: any) {
      setError(err.message || 'Failed to start game');
      console.error('Start game error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = async (answer: AnswerType) => {
    if (!gameState.sessionId || !gameState.currentQuestion) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.submitAnswer(
        gameState.sessionId,
        gameState.currentQuestion.id,
        answer
      );

      if (response.type === 'question') {
        // Continue with next question
        setGameState(prev => ({
          ...prev,
          currentQuestion: response.question!,
          questionCount: (response.question_count || 0) + 1,
          remainingCount: response.remaining_count || 0
        }));
      } else if (response.type === 'guess') {
        // Show guess
        setGameState(prev => ({
          ...prev,
          screen: 'guessing',
          guessedPlace: response.guessed_place!,
          questionCount: response.total_questions || prev.questionCount
        }));
      } else if (response.type === 'no_match') {
        // No places match - show error
        setError(response.message || 'No matches found');
        setTimeout(() => {
          resetGame();
        }, 3000);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to submit answer');
      console.error('Submit answer error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmGuess = async (isCorrect: boolean, actualPlace?: string) => {
    if (!gameState.sessionId) return;
    
    setLoading(true);
    
    try {
      await api.submitFeedback(
        gameState.sessionId,
        isCorrect,
        actualPlace
      );

      // Reload stats
      await loadStats();

      // Show result screen
      setGameState(prev => ({
        ...prev,
        screen: 'result'
      }));
    } catch (err: any) {
      setError(err.message || 'Failed to submit feedback');
      console.error('Feedback error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetGame = () => {
    setGameState(prev => ({
      screen: 'welcome',
      category: null,
      sessionId: null,
      currentQuestion: null,
      questionCount: 0,
      remainingCount: 0,
      guessedPlace: null,
      stats: prev.stats
    }));
    setError(null);
  };

  const restartSameCategory = () => {
    if (gameState.category) {
      startGame(gameState.category);
    }
  };

  return (
    <div className="min-h-screen gradient-bg flex flex-col items-center justify-center p-4">
      {/* Error Display */}
      {error && (
        <div className="fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in">
          {error}
        </div>
      )}

      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 shadow-xl">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600 font-medium">Loading...</p>
          </div>
        </div>
      )}

      {/* Welcome Screen */}
      {gameState.screen === 'welcome' && (
        <WelcomeScreen 
          onStart={startGame}
          stats={gameState.stats || { total_games: 0, correct_guesses: 0, accuracy: 0, avg_questions: 0 }}
        />
      )}

      {/* Game Screen */}
      {gameState.screen === 'playing' && gameState.currentQuestion && (
        <GameScreen
          question={gameState.currentQuestion}
          count={gameState.questionCount}
          remainingCount={gameState.remainingCount}
          onAnswer={handleAnswer}
          onBack={resetGame}
        />
      )}

      {/* Guess Screen */}
      {gameState.screen === 'guessing' && gameState.guessedPlace && (
        <GuessScreen
          place={gameState.guessedPlace}
          onConfirm={handleConfirmGuess}
        />
      )}

      {/* Result Screen */}
      {gameState.screen === 'result' && (
        <ResultScreen
          isCorrect={true}
          guessedPlace={gameState.guessedPlace}
          questionCount={gameState.questionCount}
          onRestart={restartSameCategory}
          onHome={resetGame}
        />
      )}

      {/* Footer */}
      <footer className="mt-12 text-gray-400 text-sm font-medium">
        © 2026 GuessMyPlace • Intelligent Geo Guesser
      </footer>
    </div>
  );
};

export default App;