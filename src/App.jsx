import { useState } from 'react';
import './App.css';

function App() {
  const [currentGame, setCurrentGame] = useState(null);

  return (
    <div className="arcade-wrapper">
      <header className="arcade-header">
        <h1>Buzz's All-American Arcade</h1>
        <p>Democracy & Retro 8-bit Action!</p>
      </header>

      <main className="arcade-main">
        {!currentGame ? (
          <div className="game-selector">
            <h2 className="glow-text">Select a Game</h2>
            <div className="game-cabinet" onClick={() => setCurrentGame('iceout')}>
              <div className="screen-preview">
                <h3>ICE-OUT</h3>
                <p>Break the Ice!</p>
              </div>
              <div className="cabinet-details">
                <button className="play-btn">INSERT COIN</button>
              </div>
            </div>
          </div>
        ) : (
          <div className="game-container">
            <button className="back-btn" onClick={() => setCurrentGame(null)}>
              ◀ BACK TO CONCOURSE
            </button>
            <div className="crt-screen">
              {currentGame === 'iceout' && (
                <iframe
                  title="IceOut"
                  src="/games/iceout/build/web/index.html"
                  className="game-frame"
                ></iframe>
              )}
            </div>
          </div>
        )}
      </main>

      <footer className="arcade-footer">
        <p>&copy; 2026 Buzz's Arcade. All Rights Reserved.</p>
      </footer>
    </div>
  );
}

export default App;
