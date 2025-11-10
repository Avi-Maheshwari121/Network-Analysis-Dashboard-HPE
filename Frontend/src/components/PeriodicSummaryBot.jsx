// Frontend/src/components/PeriodicSummaryBot.jsx
import React, { useState, useEffect, useRef } from 'react';
import { Bot, X, LoaderCircle, History } from 'lucide-react'; // Import Bot and History

export default function PeriodicSummaryBot({ periodicSummary, captureStatus, setActiveView }) {
  const [isOpen, setIsOpen] = useState(false);
  const [isFadingOut, setIsFadingOut] = useState(false);
  const [isGlowing, setIsGlowing] = useState(false);
  const [currentSummary, setCurrentSummary] = useState(null);
  const autoCloseTimer = useRef(null);

  // This effect triggers when a NEW summary arrives from the WebSocket
  useEffect(() => {
    if (periodicSummary && periodicSummary.summary) {
      // A new summary has arrived.
      // 1. Store it
      setCurrentSummary(periodicSummary);
      
      // 2. Force-open the bubble and start the glow
      setIsOpen(true);
      setIsFadingOut(false);
      setIsGlowing(true);

      // 3. Clear any existing timer
      if (autoCloseTimer.current) {
        clearTimeout(autoCloseTimer.current);
      }

      // 4. Set a new timer to auto-close the bubble after 10 seconds
      autoCloseTimer.current = setTimeout(() => {
        setIsFadingOut(true); // Start fade-out animation
      }, 10000); // 10 seconds
    }
  }, [periodicSummary]); // Only re-run when the periodicSummary prop changes
  
  // This effect resets the bot when capture stops
  useEffect(() => {
    if (captureStatus === 'stopped') {
      setCurrentSummary(null);
      setIsOpen(false);
      setIsFadingOut(false);
      setIsGlowing(false);
      if (autoCloseTimer.current) {
        clearTimeout(autoCloseTimer.current);
      }
    }
  }, [captureStatus]);

  // This effect handles the *end* of the fade-out animation
  useEffect(() => {
    if (isFadingOut) {
      const fadeOutTimer = setTimeout(() => {
        setIsOpen(false);
        setIsFadingOut(false);
      }, 500); // Must match the `animate-fadeOut` duration
      return () => clearTimeout(fadeOutTimer);
    }
  }, [isFadingOut]);

  // Manual click on the floating bot icon
  const handleIconClick = () => {
    setIsGlowing(false); // Acknowledge the notification
    
    // Stop any auto-close timer since the user is interacting
    if (autoCloseTimer.current) {
      clearTimeout(autoCloseTimer.current);
      autoCloseTimer.current = null;
    }
    
    if (isOpen) {
      if (!isFadingOut) {
        setIsFadingOut(true); // Start closing
      }
    } else {
      setIsOpen(true); // Open
      setIsFadingOut(false);
    }
  };
  
  // Manual click on the 'X' inside the bubble
  const handleCloseClick = (e) => {
    e.stopPropagation(); // Stop the click from bubbling to the icon
    setIsGlowing(false);
    if (autoCloseTimer.current) {
      clearTimeout(autoCloseTimer.current);
      autoCloseTimer.current = null;
    }
    setIsFadingOut(true);
  };

  const formattedTimestamp = currentSummary 
    ? new Date(currentSummary.timestamp).toLocaleTimeString() 
    : '';

  return (
    // *** THIS IS THE FIX: Changed z-50 to z-[1000] ***
    <div className="fixed bottom-6 left-6 z-[1000]">
      {/* Summary Bubble - Renders based on state */}
      {isOpen && (
        <div
          className={`summary-bot-bubble absolute bottom-full mb-3 w-80 max-w-xs bg-surface-dark border border-border-dark rounded-lg shadow-lg p-4 ${
            isFadingOut ? 'animate-fadeOut' : 'animate-fadeIn'
          }`}
        >
          <button
            onClick={handleCloseClick}
            className="absolute top-2 right-2 text-text-secondary hover:text-text-main"
          >
            <X size={18} />
          </button>
          
          {currentSummary ? (
            // --- SUMMARY VIEW ---
            <>
              <h4 className="font-bold text-primary-accent mb-2">Periodic Analysis</h4>
              <p className="text-sm text-text-main mb-2">
                {currentSummary.summary}
              </p>
              {/* --- UPDATED FOOTER --- */}
              <div className="flex justify-between items-center mt-2 pt-2 border-t border-border-dark">
                <button 
                  onClick={() => setActiveView('summaryhistory')}
                  className="text-xs text-text-secondary hover:text-primary-accent flex items-center gap-1 transition-colors"
                >
                  <History size={14} />
                  View History
                </button>
                <p className="text-xs text-text-secondary text-right">
                  {formattedTimestamp}
                </p>
              </div>
            </>
          ) : (
            // --- WAITING VIEW ---
            <>
              <h4 className="font-bold text-primary-accent mb-2 flex items-center gap-2">
                <LoaderCircle size={16} className="animate-spin" />
                Waiting for Analysis
              </h4>
              <p className="text-sm text-text-main mb-2">
                {captureStatus === 'running' 
                  ? "Periodic insights will appear here after 60 seconds of active capture."
                  : "Start a capture to receive live AI insights."
                }
              </p>
            </>
          )}
        </div>
      )}

      {/* Floating Bot Icon - Always visible */}
      <button
        onClick={handleIconClick}
        className={`bg-primary-accent text-base-dark p-3 rounded-full shadow-lg transition-transform hover:scale-110 ${
          isGlowing ? 'animate-pulse' : 'animate-float'
        }`}
      >
        <Bot size={28} /> {/* --- ICON CHANGED --- */}
      </button>
    </div>
  );
}