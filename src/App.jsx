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
                <div className="attract-mode">
                  <h3>ICE-OUT</h3>
                  <p>Break the Ice!</p>
                  <div className="demo-blocks">
                    <div className="block"></div>
                    <div className="block"></div>
                    <div className="block"></div>
                    <div className="block" style={{ borderColor: 'var(--neon-pink)', boxShadow: '0 0 5px var(--neon-pink)' }}></div>
                    <div className="block"></div>
                  </div>
                  <div style={{ fontSize: '0.6rem', marginTop: '10px', color: 'gray' }}>
                    Latino Family Rescue Mission
                  </div>
                </div>
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
                  src={`${import.meta.env.BASE_URL}games/iceout/index.html`}
                  className="game-frame"
                ></iframe>
              )}
            </div>
          </div>
        )}
      </main>

      <footer className="arcade-footer">
        <p>★ BORN IN THE USA ★ &copy; 2026 Buzz's Arcade. All Rights Reserved.</p>
      </footer>
    </div>
  );
}

export default App;
