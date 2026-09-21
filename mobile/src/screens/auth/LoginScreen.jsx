import { useState } from 'react';
import { Link } from 'react-router-dom';
import { HiOutlineMail, HiOutlineLockClosed, HiOutlineEye, HiOutlineEyeOff } from 'react-icons/hi';
import useAuthStore from '../../store/authStore';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const { login, isLoading, error, clearError } = useAuthStore();

  const handleSubmit = async (e) => {
    e.preventDefault();
    clearError();
    await login(email, password);
  };

  return (
    <div className="auth-page">
      <div className="auth-logo">
        <h1>JobPilot AI</h1>
        <p>One profile. Multiple job portals. Smarter applications.</p>
      </div>

      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label" htmlFor="login-email">Email</label>
          <div style={{ position: 'relative' }}>
            <HiOutlineMail style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', fontSize: 18 }} />
            <input
              id="login-email"
              type="email"
              className="form-input"
              style={{ paddingLeft: 40 }}
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="login-password">Password</label>
          <div style={{ position: 'relative' }}>
            <HiOutlineLockClosed style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', fontSize: 18 }} />
            <input
              id="login-password"
              type={showPassword ? 'text' : 'password'}
              className="form-input"
              style={{ paddingLeft: 40, paddingRight: 40 }}
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              style={{ position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: 18 }}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? <HiOutlineEyeOff /> : <HiOutlineEye />}
            </button>
          </div>
        </div>

        {error && <div className="form-error" role="alert">{error}</div>}

        <button
          type="submit"
          className="btn btn-primary btn-block btn-lg"
          disabled={isLoading || !email || !password}
          id="login-submit"
        >
          {isLoading ? <span className="spinner" style={{ width: 20, height: 20 }} /> : 'Sign In'}
        </button>
      </form>

      <div className="auth-footer">
        <p>Don't have an account? <Link to="/register">Create one</Link></p>
      </div>
    </div>
  );
}
