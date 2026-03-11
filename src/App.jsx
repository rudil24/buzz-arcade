import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [currentGame, setCurrentGame] = useState(null);

  useEffect(() => {
    const handleMessage = (event) => {
      if (event.data === 'returnToConcourse') {
        setCurrentGame(null);
      }
    };
    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

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
            <div className="cabinets-container" style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap', justifyContent: 'center' }}>
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

              <div className="game-cabinet" onClick={() => setCurrentGame('truth-evaders')}>
                <div className="screen-preview">
                  <div className="attract-mode">
                    <h3>TRUTH EVADERS</h3>
                    <p>Expose the List!</p>
                    <div className="demo-blocks">
                      <div className="block" style={{ borderColor: 'var(--neon-blue)', boxShadow: '0 0 5px var(--neon-blue)' }}></div>
                      <div className="block" style={{ borderColor: 'var(--neon-blue)', boxShadow: '0 0 5px var(--neon-blue)' }}></div>
                      <div className="block" style={{ borderColor: 'var(--neon-blue)', boxShadow: '0 0 5px var(--neon-blue)' }}></div>
                    </div>
                    <div style={{ fontSize: '0.6rem', marginTop: '10px', color: 'gray' }}>
                      8-bit Alien Shooter
                    </div>
                  </div>
                </div>
                <div className="cabinet-details">
                  <button className="play-btn">INSERT COIN</button>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="game-container">
            <button className="back-btn" onClick={() => setCurrentGame(null)}>
              ◀ BACK TO CONCOURSE
            </button>
            <div className="crt-screen">
              {currentGame && (
                <iframe
                  title={currentGame}
                  src={`${import.meta.env.BASE_URL}games/${currentGame}/index.html`}
                  className="game-frame"
                  onLoad={(e) => {
                    // Pygbag initializes its canvas size based on the window. 
                    // React DOM updates sometimes cause Pygbag to read the size before CSS is fully applied.
                    // Dispatching resize forces Pygbag's event listener to scale the canvas down to the container wrapper.
                    const enforceScaling = () => e.target.contentWindow?.dispatchEvent(new Event('resize'));
                    setTimeout(enforceScaling, 100);
                    setTimeout(enforceScaling, 500);
                    setTimeout(enforceScaling, 1500);
                  }}
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
