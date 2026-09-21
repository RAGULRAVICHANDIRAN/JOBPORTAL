/**
 * JobPilot AI — Job Detail Bottom Sheet
 *
 * Full-screen bottom sheet showing detailed job information,
 * match score breakdown, skill analysis, and action buttons.
 */

import { useState, useEffect } from 'react';
import {
  HiOutlineX, HiOutlineLocationMarker, HiOutlineBriefcase,
  HiOutlineClock, HiOutlineCurrencyRupee, HiOutlineExternalLink,
  HiOutlineHeart, HiHeart, HiOutlineLightningBolt,
  HiOutlineCheckCircle, HiOutlineExclamationCircle,
  HiOutlineAcademicCap, HiOutlineOfficeBuilding,
  HiOutlineGlobe,
} from 'react-icons/hi';
import api from '../../services/api';

// ─── Helpers (same as JobsScreen) ────────────────────
function formatSalary(min, max, currency = 'INR', period = 'yearly') {
  if (!min && !max) return null;
  const fmt = (v) => {
    if (currency === 'INR') {
      if (period === 'yearly') {
        if (v >= 100000) return `₹${(v / 100000).toFixed(v % 100000 === 0 ? 0 : 1)}L`;
        return `₹${(v / 1000).toFixed(0)}K`;
      }
      return `₹${v.toLocaleString('en-IN')}`;
    }
    return `${currency} ${v.toLocaleString()}`;
  };
  if (min && max) return `${fmt(min)} — ${fmt(max)}`;
  if (min) return `${fmt(min)}+`;
  return `Up to ${fmt(max)}`;
}

function timeAgo(dateStr) {
  if (!dateStr) return '';
  const diff = Date.now() - new Date(dateStr).getTime();
  const hours = Math.floor(diff / 3600000);
  if (hours < 1) return 'Just now';
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days === 1) return '1 day ago';
  if (days < 30) return `${days} days ago`;
  return `${Math.floor(days / 30)}mo ago`;
}

function matchColor(score) {
  if (score >= 85) return '#6366f1';
  if (score >= 70) return '#10b981';
  if (score >= 50) return '#f59e0b';
  return '#f87171';
}

const avatarGradients = [
  'linear-gradient(135deg, #6366f1, #8b5cf6)',
  'linear-gradient(135deg, #f43f5e, #ec4899)',
  'linear-gradient(135deg, #10b981, #14b8a6)',
  'linear-gradient(135deg, #f59e0b, #f97316)',
  'linear-gradient(135deg, #3b82f6, #6366f1)',
  'linear-gradient(135deg, #8b5cf6, #a855f7)',
  'linear-gradient(135deg, #ef4444, #f43f5e)',
  'linear-gradient(135deg, #06b6d4, #3b82f6)',
];

function getAvatarGradient(company) {
  const hash = company.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0);
  return avatarGradients[hash % avatarGradients.length];
}

// ─── Match Circle ────────────────────────────────────
function MatchCircle({ score, size = 80 }) {
  const radius = (size - 10) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const color = matchColor(score);

  return (
    <div className="match-circle match-circle-lg">
      <svg>
        <circle className="match-circle-bg" cx={size / 2} cy={size / 2} r={radius} />
        <circle
          className="match-circle-progress"
          cx={size / 2} cy={size / 2} r={radius}
          stroke={color}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="match-circle-text" style={{ color }}>{Math.round(score)}%</div>
    </div>
  );
}

// ─── Score Bar ───────────────────────────────────────
function ScoreBar({ label, score }) {
  const color = matchColor(score);
  return (
    <div className="match-breakdown-item">
      <div className="match-breakdown-value" style={{ color }}>{Math.round(score)}</div>
      <div className="match-breakdown-label">{label}</div>
    </div>
  );
}

// ─── Main Component ──────────────────────────────────
export default function JobDetailSheet({ jobId, onClose, onToggleSave }) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDetail();
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = '';
    };
  }, [jobId]);

  const loadDetail = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.get(`/jobs/${jobId}`);
      setDetail(data);
    } catch (err) {
      setError(err.message || 'Failed to load job details.');
    } finally {
      setLoading(false);
    }
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) onClose();
  };

  const handleSave = () => {
    if (detail) onToggleSave(detail);
  };

  const salary = detail ? formatSalary(detail.salary_min, detail.salary_max, detail.salary_currency, detail.salary_period) : null;
  const match = detail?.match;

  return (
    <>
      <div className="bottom-sheet-overlay" onClick={handleOverlayClick} />
      <div className="bottom-sheet" role="dialog" aria-modal="true" id="job-detail-sheet">
        <div className="bottom-sheet-handle" />

        {/* Header */}
        <div className="bottom-sheet-header">
          <span className="text-sm text-muted">Job Details</span>
          <button className="bottom-sheet-close" onClick={onClose} aria-label="Close">
            <HiOutlineX />
          </button>
        </div>

        {/* Body */}
        <div className="bottom-sheet-body">
          {loading ? (
            <div style={{ display: 'flex', justifyContent: 'center', padding: 'var(--space-2xl)' }}>
              <div className="spinner" />
            </div>
          ) : error ? (
            <div className="empty-state" style={{ padding: 'var(--space-xl)' }}>
              <HiOutlineExclamationCircle className="empty-state-icon" />
              <h3 style={{ color: 'var(--text)' }}>Error</h3>
              <p className="text-sm">{error}</p>
              <button className="btn btn-secondary btn-sm" onClick={loadDetail} style={{ marginTop: 'var(--space-md)' }}>
                Retry
              </button>
            </div>
          ) : detail ? (
            <>
              {/* Company Header */}
              <div style={{ display: 'flex', gap: 'var(--space-md)', marginBottom: 'var(--space-lg)' }}>
                <div
                  className="job-card-avatar"
                  style={{
                    background: getAvatarGradient(detail.company),
                    width: 56, height: 56, fontSize: 'var(--font-size-md)',
                  }}
                >
                  {detail.company.replace(/\(DEMO\)/gi, '').trim().split(' ').slice(0, 2).map(w => w[0]).join('')}
                </div>
                <div style={{ flex: 1 }}>
                  <h2 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 700, lineHeight: 1.3 }}>
                    {detail.title}
                  </h2>
                  <div style={{ color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)', marginTop: 2 }}>
                    {detail.company.replace(' (DEMO)', '')}
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 8 }}>
                    {detail.location && (
                      <span className="job-card-meta-item">
                        <HiOutlineLocationMarker /> {detail.location}
                      </span>
                    )}
                    {detail.remote_type && (
                      <span className="badge badge-primary" style={{ padding: '2px 8px', fontSize: 10 }}>
                        {detail.remote_type}
                      </span>
                    )}
                    {detail.employment_type && (
                      <span className="job-card-meta-item">
                        <HiOutlineBriefcase /> {detail.employment_type}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Salary & Experience Row */}
              <div className="card" style={{ marginBottom: 'var(--space-lg)', display: 'flex', justifyContent: 'space-around', textAlign: 'center' }}>
                {salary && (
                  <div>
                    <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)' }}>SALARY</div>
                    <div style={{ fontWeight: 700, color: 'var(--success)', marginTop: 4 }}>{salary}</div>
                    {detail.salary_period !== 'yearly' && (
                      <div className="text-xs text-muted">/{detail.salary_period}</div>
                    )}
                  </div>
                )}
                {detail.experience_max !== null && (
                  <div>
                    <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)' }}>EXPERIENCE</div>
                    <div style={{ fontWeight: 700, marginTop: 4 }}>
                      {detail.experience_min === 0 && detail.experience_max === 0
                        ? 'Fresher'
                        : `${detail.experience_min || 0}–${detail.experience_max} yrs`}
                    </div>
                  </div>
                )}
                {detail.company_type && (
                  <div>
                    <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)' }}>TYPE</div>
                    <div style={{ fontWeight: 700, marginTop: 4, textTransform: 'capitalize' }}>
                      {detail.company_type}
                    </div>
                  </div>
                )}
              </div>

              {/* Match Score Section */}
              {match && (
                <div className="detail-section">
                  <div className="detail-section-title">
                    <HiOutlineLightningBolt style={{ verticalAlign: 'middle', marginRight: 4 }} />
                    AI Match Score
                  </div>

                  <div className="card" style={{
                    display: 'flex', alignItems: 'center', gap: 'var(--space-lg)',
                    marginBottom: 'var(--space-md)',
                    background: 'linear-gradient(135deg, rgba(99,102,241,0.08), rgba(244,63,94,0.04))',
                    borderColor: 'rgba(99,102,241,0.2)',
                  }}>
                    <MatchCircle score={match.overall_score} />
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 700, fontSize: 'var(--font-size-md)', marginBottom: 4 }}>
                        {match.overall_score >= 85 ? 'Excellent Match!' :
                         match.overall_score >= 70 ? 'Good Match' :
                         match.overall_score >= 50 ? 'Fair Match' : 'Low Match'}
                      </div>
                      {match.match_reasons?.map((reason, i) => (
                        <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 'var(--font-size-xs)', color: 'var(--text-secondary)' }}>
                          <HiOutlineCheckCircle style={{ color: 'var(--success)', flexShrink: 0 }} /> {reason}
                        </div>
                      ))}
                      {match.warnings?.map((warn, i) => (
                        <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 'var(--font-size-xs)', color: 'var(--warning)' }}>
                          <HiOutlineExclamationCircle style={{ flexShrink: 0 }} /> {warn}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Breakdown Grid */}
                  <div className="match-breakdown-grid">
                    <ScoreBar label="Skills" score={match.skills_score} />
                    <ScoreBar label="Experience" score={match.experience_score} />
                    <ScoreBar label="Education" score={match.education_score} />
                    <ScoreBar label="Location" score={match.location_score} />
                    <ScoreBar label="Salary" score={match.salary_score} />
                    <ScoreBar label="Fit" score={match.preference_score} />
                  </div>
                </div>
              )}

              {/* Skills Analysis */}
              {(match?.matching_skills?.length > 0 || match?.missing_skills?.length > 0) && (
                <div className="detail-section">
                  <div className="detail-section-title">Skills Analysis</div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                    {match.matching_skills?.map((skill) => (
                      <span key={skill} className="skill-tag skill-tag--match">
                        <HiOutlineCheckCircle /> {skill}
                      </span>
                    ))}
                    {match.missing_skills?.map((skill) => (
                      <span key={skill} className="skill-tag skill-tag--missing">
                        <HiOutlineExclamationCircle /> {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Required Skills */}
              {detail.skills?.length > 0 && (
                <div className="detail-section">
                  <div className="detail-section-title">Required Skills</div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                    {detail.skills.map((skill) => (
                      <span
                        key={skill.id || skill.name}
                        className={`skill-tag skill-tag--default${skill.is_required ? ' skill-tag--required' : ''}`}
                      >
                        {skill.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Description */}
              {detail.description && (
                <div className="detail-section">
                  <div className="detail-section-title">About This Role</div>
                  <div className="detail-section-content">{detail.description}</div>
                </div>
              )}

              {/* Requirements */}
              {detail.requirements && (
                <div className="detail-section">
                  <div className="detail-section-title">Requirements</div>
                  <div className="detail-section-content">{detail.requirements}</div>
                </div>
              )}

              {/* Benefits */}
              {detail.benefits && (
                <div className="detail-section">
                  <div className="detail-section-title">Benefits</div>
                  <div className="detail-section-content">{detail.benefits}</div>
                </div>
              )}

              {/* Posted Info */}
              <div style={{
                fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)',
                display: 'flex', alignItems: 'center', gap: 4, marginTop: 'var(--space-md)',
              }}>
                <HiOutlineClock /> Posted {timeAgo(detail.posted_at)}
                {detail.source && (
                  <>
                    <span className="job-card-meta-divider" />
                    Source: {detail.source}
                  </>
                )}
              </div>
            </>
          ) : null}
        </div>

        {/* Footer Actions */}
        {detail && !loading && (
          <div className="bottom-sheet-footer">
            <button
              className={`btn ${detail.is_saved ? 'btn-secondary' : 'btn-ghost'}`}
              onClick={handleSave}
              style={{ flex: '0 0 auto' }}
              id="detail-save-btn"
            >
              {detail.is_saved ? <HiHeart style={{ color: 'var(--accent-500)' }} /> : <HiOutlineHeart />}
              {detail.is_saved ? 'Saved' : 'Save'}
            </button>

            {detail.external_url && (
              <a
                href={detail.external_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-secondary"
                style={{ flex: '0 0 auto' }}
                id="detail-portal-btn"
              >
                <HiOutlineExternalLink /> Portal
              </a>
            )}

            <button
              className="btn btn-primary"
              style={{ flex: 1 }}
              id="detail-apply-btn"
            >
              <HiOutlineLightningBolt /> Apply
            </button>
          </div>
        )}
      </div>
    </>
  );
}
