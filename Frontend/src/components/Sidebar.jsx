export default function Sidebar({ activeView, setActiveView }) {
  const NavButton = ({ view, children }) => (
    <button
      onClick={() => setActiveView(view)}
      className={`w-full p-3 text-left rounded-lg text-lg font-semibold transition-colors ${
        activeView === view
          ? 'bg-primary-accent text-base-dark'
          : 'text-text-secondary hover:bg-surface-dark hover:text-text-main'
      }`}
    >
      {children}
    </button>
  );

  return (
    <aside className="w-60 h-screen bg-surface-dark p-6 flex flex-col border-r border-border-dark sticky top-0">
      <h1 className="text-3xl font-bold text-primary-accent mb-12">NetPulse</h1>
      <nav className="flex flex-col gap-4">
        <NavButton view="dashboard">Dashboard</NavButton>
        <NavButton view="rawdata">Raw Data</NavButton>
      </nav>
    </aside>
  );
}