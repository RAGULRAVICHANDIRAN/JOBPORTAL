import { HiOutlineCog } from 'react-icons/hi';

export default function AutomationScreen() {
  return (
    <div className="page">
      <h2 className="heading-2" style={{ marginBottom: 'var(--space-md)' }}>Automation</h2>

      {/* Status Card */}
      <div className="card" style={{ marginBottom: 'var(--space-lg)', textAlign: 'center' }}>
        <div style={{
          width: 64, height: 64,
          borderRadius: '50%',
          background: 'rgba(100, 116, 139, 0.15)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          margin: '0 auto var(--space-md)',
          color: 'var(--text-muted)',
          fontSize: 28,
        }}>
          <HiOutlineCog />
        </div>
        <div style={{ fontWeight: 600, marginBottom: 4 }}>AUTO APPLY</div>
        <div className="badge" style={{ background: 'rgba(100,116,139,0.15)', color: 'var(--text-muted)' }}>
          ● INACTIVE
        </div>
      </div>

      {/* Daily Stats */}
      <div className="card" style={{ marginBottom: 'var(--space-md)' }}>
        <h3 style={{ fontSize: 'var(--font-size-sm)', fontWeight: 600, marginBottom: 'var(--space-md)', color: 'var(--text-secondary)' }}>
          Today's Activity
        </h3>
        {[
          ['Jobs scanned', '0'],
          ['Jobs matched', '0'],
          ['Applications prepared', '0'],
          ['Applications submitted', '0'],
          ['Manual review required', '0'],
          ['Skipped', '0'],
        ].map(([label, value]) => (
          <div key={label} style={{
            display: 'flex', justifyContent: 'space-between',
            padding: '8px 0', borderBottom: '1px solid var(--border-light)',
            fontSize: 'var(--font-size-sm)',
          }}>
            <span className="text-secondary">{label}</span>
            <span style={{ fontWeight: 600 }}>{value}</span>
          </div>
        ))}
      </div>

      <button className="btn btn-primary btn-block" disabled>
        Configure Automation (Phase 8)
      </button>

      {/* Kill Switch */}
      <button className="btn btn-danger btn-block" disabled style={{ marginTop: 'var(--space-sm)', opacity: 0.4 }}>
        🛑 EMERGENCY STOP
      </button>
    </div>
  );
}
