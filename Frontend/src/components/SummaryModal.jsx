// SummaryModal.jsx

export default function SummaryModal({ summary, isOpen, onClose }) {
  if (!isOpen || !summary) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 animate-fade-in">
      <div className="bg-surface-dark p-6 rounded-lg shadow-lg w-full max-w-2xl border border-border-dark">
        <h2 className="text-xl font-bold mb-4 text-primary-accent">Capture Session Summary</h2>
        {/* whitespace-pre-wrap respects newlines and formatting from the AI's response */}
        <p className="text-text-secondary whitespace-pre-wrap leading-relaxed max-h-[60vh] overflow-y-auto pr-2">
          {summary}
        </p>
        <div className="flex justify-end mt-6">
          <button 
            onClick={onClose} 
            className="bg-primary-accent text-base-dark px-4 py-2 rounded font-bold hover:opacity-90 transition-opacity"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}