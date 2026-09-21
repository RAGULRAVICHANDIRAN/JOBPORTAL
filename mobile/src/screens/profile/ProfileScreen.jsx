import { useEffect, useState } from 'react';
import useAuthStore from '../../store/authStore';
import api from '../../services/api';
import {
  HiOutlineUser, HiOutlineMail, HiOutlineLogout,
  HiOutlineAcademicCap, HiOutlineBriefcase, HiOutlineCode,
  HiOutlineDocumentText, HiOutlineCog, HiOutlineShieldCheck
} from 'react-icons/hi';

export default function ProfileScreen() {
  const { user, logout } = useAuthStore();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await api.get('/profile');
      setProfile(data);
    } catch (err) {
      console.error('Failed to load profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const strengthColor = (s) => {
    if (s >= 80) return 'var(--success)';
    if (s >= 50) return 'var(--warning)';
    return 'var(--error)';
  };

  return (
    <div className="page">
      {/* Profile Header */}
      <div style={{ textAlign: 'center', marginBottom: 'var(--space-lg)' }}>
        <div style={{
          width: 80, height: 80,
          borderRadius: '50%',
          background: 'linear-gradient(135deg, var(--primary-500), var(--accent-500))',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          margin: '0 auto var(--space-md)',
          fontSize: 32, fontWeight: 700, color: 'white',
        }}>
          {user?.name?.charAt(0)?.toUpperCase() || 'U'}
        </div>
        <h2 className="heading-2">{user?.name || 'User'}</h2>
        <p className="text-secondary text-sm">{user?.email}</p>
      </div>

      {/* Profile Strength */}
      {profile && (
        <div className="card" style={{ marginBottom: 'var(--space-md)', textAlign: 'center' }}>
          <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)', marginBottom: 8 }}>
            PROFILE STRENGTH
          </div>
          <div style={{
            fontSize: 'var(--font-size-3xl)', fontWeight: 800,
            color: strengthColor(profile.profile_strength),
          }}>
            {profile.profile_strength}%
          </div>
          <div style={{
            height: 6, borderRadius: 3,
            background: 'var(--border)',
            marginTop: 12, overflow: 'hidden',
          }}>
            <div style={{
              height: '100%', borderRadius: 3,
              width: `${profile.profile_strength}%`,
              background: strengthColor(profile.profile_strength),
              transition: 'width 0.6s ease',
            }} />
          </div>
        </div>
      )}

      {/* Sections */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
        <ProfileMenuItem icon={<HiOutlineUser />} label="Personal Info" count={null} />
        <ProfileMenuItem icon={<HiOutlineAcademicCap />} label="Education" count={profile?.education?.length || 0} />
        <ProfileMenuItem icon={<HiOutlineBriefcase />} label="Experience" count={profile?.experience?.length || 0} />
        <ProfileMenuItem icon={<HiOutlineCode />} label="Skills" count={profile?.skills?.length || 0} />
        <ProfileMenuItem icon={<HiOutlineDocumentText />} label="Resumes" count="Phase 2" />

        <div style={{ height: 1, background: 'var(--border)', margin: 'var(--space-sm) 0' }} />

        <ProfileMenuItem icon={<HiOutlineCog />} label="Settings" />
        <ProfileMenuItem icon={<HiOutlineShieldCheck />} label="Privacy Center" />

        <button
          className="btn btn-ghost btn-block"
          onClick={logout}
          style={{ color: 'var(--error)', marginTop: 'var(--space-md)', justifyContent: 'center' }}
          id="logout-button"
        >
          <HiOutlineLogout /> Sign Out
        </button>
      </div>
    </div>
  );
}

function ProfileMenuItem({ icon, label, count }) {
  return (
    <div className="card" style={{
      display: 'flex', alignItems: 'center', gap: 'var(--space-md)',
      cursor: 'pointer', padding: '12px var(--space-md)',
    }}>
      <span style={{ color: 'var(--primary-400)', fontSize: 20 }}>{icon}</span>
      <span style={{ flex: 1, fontWeight: 500, fontSize: 'var(--font-size-sm)' }}>{label}</span>
      {count !== undefined && count !== null && (
        <span className="badge badge-primary">{count}</span>
      )}
      <span style={{ color: 'var(--text-muted)' }}>›</span>
    </div>
  );
}
