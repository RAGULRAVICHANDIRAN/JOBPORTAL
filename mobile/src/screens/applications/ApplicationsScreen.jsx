import { HiOutlineClipboardList } from 'react-icons/hi';

export default function ApplicationsScreen() {
  const columns = ['Saved', 'Ready', 'Applied', 'Interview', 'Offer', 'Rejected'];

  return (
    <div className="page">
      <h2 className="heading-2" style={{ marginBottom: 'var(--space-lg)' }}>Applications</h2>

      {/* Status Summary */}
      <div style={{
        display: 'flex', gap: 'var(--space-sm)',
        overflowX: 'auto', marginBottom: 'var(--space-lg)',
        paddingBottom: 4,
      }}>
        {columns.map((col) => (
          <div key={col} style={{
            textAlign: 'center', minWidth: 70,
            padding: '8px 12px',
            background: 'var(--bg-card)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-sm)',
          }}>
            <div style={{ fontWeight: 700, fontSize: 'var(--font-size-lg)' }}>0</div>
            <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)' }}>{col}</div>
          </div>
        ))}
      </div>

      <div className="empty-state">
        <HiOutlineClipboardList className="empty-state-icon" />
        <h3 style={{ marginBottom: 4, color: 'var(--text)' }}>No Applications Yet</h3>
        <p className="text-sm">Your application tracker will appear here.</p>
        <p className="text-xs text-muted" style={{ marginTop: 8 }}>
          Kanban board will be built in Phase 5.
        </p>
      </div>
    </div>
  );
}
