import { useState } from 'react';
import { Link } from 'react-router-dom';
import { HiOutlineMail, HiOutlineLockClosed, HiOutlineUser, HiOutlineEye, HiOutlineEyeOff } from 'react-icons/hi';
import useAuthStore from '../../store/authStore';

export default function RegisterScreen() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [validationError, setValidationError] = useState('');
  const { register, isLoading, error, clearError } = useAuthStore();

  const handleSubmit = async (e) => {
    e.preventDefault();
    clearError();
    setValidationError('');

    if (password !== confirmPassword) {
      setValidationError('Passwords do not match.');
      return;
    }

    if (password.length < 8) {
      setValidationError('Password must be at least 8 characters.');
      return;
    }

    if (!/[A-Z]/.test(password) || !/[a-z]/.test(password) || !/[0-9]/.test(password)) {
      setValidationError('Password must contain uppercase, lowercase, and a digit.');
      return;
    }

    await register(name, email, password);
  };

  const displayError = validationError || error;

  return (
    <div className="auth-page">
      <div className="auth-logo">
        <h1>JobPilot AI</h1>
        <p>Create your account and start your job search journey</p>
      </div>

      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label" htmlFor="register-name">Full Name</label>
          <div style={{ position: 'relative' }}>
            <HiOutlineUser style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', fontSize: 18 }} />
            <input
              id="register-name"
              type="text"
              className="form-input"
              style={{ paddingLeft: 40 }}
              placeholder="Your full name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              autoComplete="name"
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="register-email">Email</label>
          <div style={{ position: 'relative' }}>
            <HiOutlineMail style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', fontSize: 18 }} />
            <input
              id="register-email"
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
          <label className="form-label" htmlFor="register-password">Password</label>
          <div style={{ position: 'relative' }}>
            <HiOutlineLockClosed style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', fontSize: 18 }} />
            <input
              id="register-password"
              type={showPassword ? 'text' : 'password'}
              className="form-input"
              style={{ paddingLeft: 40, paddingRight: 40 }}
              placeholder="Min 8 chars, uppercase, digit"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="new-password"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              style={{ position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: 18 }}
            >
              {showPassword ? <HiOutlineEyeOff /> : <HiOutlineEye />}
            </button>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="register-confirm">Confirm Password</label>
          <div style={{ position: 'relative' }}>
            <HiOutlineLockClosed style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', fontSize: 18 }} />
            <input
              id="register-confirm"
              type="password"
              className="form-input"
              style={{ paddingLeft: 40 }}
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              autoComplete="new-password"
            />
          </div>
        </div>

        {displayError && <div className="form-error" role="alert">{displayError}</div>}

        <button
          type="submit"
          className="btn btn-primary btn-block btn-lg"
          disabled={isLoading || !name || !email || !password || !confirmPassword}
          id="register-submit"
        >
          {isLoading ? <span className="spinner" style={{ width: 20, height: 20 }} /> : 'Create Account'}
        </button>
      </form>

      <div className="auth-footer">
        <p>Already have an account? <Link to="/login">Sign in</Link></p>
      </div>
    </div>
  );
}
