/**
 * JobPilot AI — Jobs Screen
 *
 * Full-featured job discovery with search, filter chips, job cards with
 * match scores, and a bottom-sheet detail view.
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import {
  HiOutlineSearch, HiOutlineX, HiOutlineLocationMarker,
  HiOutlineClock, HiOutlineCurrencyRupee, HiOutlineBriefcase,
  HiOutlineHeart, HiHeart, HiOutlineOfficeBuilding,
} from 'react-icons/hi';
import api from '../../services/api';
import JobDetailSheet from './JobDetailSheet';

// ─── Avatar gradient palette ─────────────────────────
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

// ─── Salary formatter ────────────────────────────────
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

// ─── Time ago ────────────────────────────────────────
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

// ─── Match score color ───────────────────────────────
function matchColor(score) {
  if (score >= 85) return '#6366f1';
  if (score >= 70) return '#10b981';
  if (score >= 50) return '#f59e0b';
  return '#f87171';
}

// ─── Match Circle Component ──────────────────────────
function MatchCircle({ score, size = 48 }) {
  const radius = (size - 8) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const color = matchColor(score);

  return (
    <div className={`match-circle${size > 48 ? ' match-circle-lg' : ''}`}>
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

// ─── Skeleton Loader ─────────────────────────────────
function JobSkeleton() {
  return (
    <div className="job-skeleton">
      <div className="job-skeleton-header">
        <div className="job-skeleton-avatar skeleton" />
        <div className="job-skeleton-lines">
          <div className="job-skeleton-line job-skeleton-line--title skeleton" />
          <div className="job-skeleton-line job-skeleton-line--sub skeleton" />
        </div>
      </div>
      <div className="job-skeleton-line job-skeleton-line--short skeleton" style={{ marginBottom: 8 }} />
      <div className="job-skeleton-chips">
        <div className="job-skeleton-chip skeleton" />
        <div className="job-skeleton-chip skeleton" />
        <div className="job-skeleton-chip skeleton" />
      </div>
    </div>
  );
}

// ─── Filter Chips ────────────────────────────────────
const FILTER_CHIPS = [
  { key: 'all', label: 'All', params: {} },
  { key: 'remote', label: 'Remote', params: { remote_type: 'remote' } },
  { key: 'hybrid', label: 'Hybrid', params: { remote_type: 'hybrid' } },
  { key: 'onsite', label: 'Onsite', params: { remote_type: 'onsite' } },
  { key: 'fresher', label: 'Fresher', params: { experience_max: 0 } },
  { key: 'fulltime', label: 'Full-time', params: { employment_type: 'full-time' } },
  { key: 'internship', label: 'Internship', params: { employment_type: 'internship' } },
];

// ─── Job Card Component ──────────────────────────────
function JobCard({ job, onSelect, onToggleSave }) {
  const salary = formatSalary(job.salary_min, job.salary_max, job.salary_currency, job.salary_period);
  const initials = job.company.replace(/\(DEMO\)/gi, '').trim().split(' ').slice(0, 2).map(w => w[0]).join('');

  const handleSave = (e) => {
    e.stopPropagation();
    onToggleSave(job);
  };

  return (
    <div className="job-card" onClick={() => onSelect(job)} id={`job-card-${job.id}`}>
      <div className="job-card-header">
        <div
          className="job-card-avatar"
          style={{ background: getAvatarGradient(job.company) }}
        >
          {initials}
        </div>
        <div className="job-card-info">
          <div className="job-card-title">{job.title}</div>
          <div className="job-card-company">{job.company.replace(' (DEMO)', '')}</div>
        </div>
        <MatchCircle score={job.match_score} />
      </div>

      {/* Meta row */}
      <div className="job-card-meta">
        {job.location && (
          <span className="job-card-meta-item">
            <HiOutlineLocationMarker /> {job.location}
          </span>
        )}
        {job.remote_type && (
          <>
            <span className="job-card-meta-divider" />
            <span className="badge badge-primary" style={{ padding: '2px 8px', fontSize: 10 }}>
              {job.remote_type}
            </span>
          </>
        )}
        {job.employment_type && (
          <>
            <span className="job-card-meta-divider" />
            <span className="job-card-meta-item">
              <HiOutlineBriefcase /> {job.employment_type}
            </span>
          </>
        )}
      </div>

      {/* Salary */}
      {salary && (
        <div className="job-card-meta" style={{ marginTop: 0 }}>
          <span className="job-card-salary">
            <HiOutlineCurrencyRupee style={{ verticalAlign: 'middle', marginRight: 2 }} />
            {salary}
          </span>
          {job.salary_period !== 'yearly' && (
            <span className="text-xs text-muted">/{job.salary_period}</span>
          )}
          {job.experience_max !== null && job.experience_max !== undefined && (
            <>
              <span className="job-card-meta-divider" />
              <span className="job-card-meta-item">
                {job.experience_min === 0 && job.experience_max === 0
                  ? 'Fresher'
                  : `${job.experience_min || 0}–${job.experience_max} yrs`}
              </span>
            </>
          )}
        </div>
      )}

      {/* Skills */}
      {job.skills && job.skills.length > 0 && (
        <div className="job-card-skills">
          {job.skills.slice(0, 5).map((skill) => (
            <span
              key={skill.id || skill.name}
              className={`skill-tag skill-tag--default${skill.is_required ? ' skill-tag--required' : ''}`}
            >
              {skill.name}
            </span>
          ))}
          {job.skills.length > 5 && (
            <span className="skill-tag skill-tag--default">+{job.skills.length - 5}</span>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="job-card-footer">
        <span className="job-card-time">
          <HiOutlineClock style={{ verticalAlign: 'middle', marginRight: 4 }} />
          {timeAgo(job.posted_at)}
        </span>
        <button
          className={`job-card-save${job.is_saved ? ' saved' : ''}`}
          onClick={handleSave}
          aria-label={job.is_saved ? 'Unsave job' : 'Save job'}
        >
          {job.is_saved ? <HiHeart /> : <HiOutlineHeart />}
        </button>
      </div>
    </div>
  );
}

// ─── Main Jobs Screen ────────────────────────────────
export default function JobsScreen() {
  const [jobs, setJobs] = useState([]);
  const [total, setTotal] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  const [search, setSearch] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');
  const [selectedJob, setSelectedJob] = useState(null);

  const searchTimer = useRef(null);

  // ── Fetch jobs ────────
  const fetchJobs = useCallback(async (pageNum = 1, append = false) => {
    try {
      if (pageNum === 1) setLoading(true);
      else setLoadingMore(true);

      const filterChip = FILTER_CHIPS.find(f => f.key === activeFilter);
      const params = new URLSearchParams({
        page: String(pageNum),
        limit: '20',
        sort_by: 'posted_at',
        ...(search ? { search } : {}),
        ...(filterChip?.params || {}),
      });

      const data = await api.get(`/jobs?${params.toString()}`);

      if (append) {
        setJobs(prev => [...prev, ...data.jobs]);
      } else {
        setJobs(data.jobs);
      }
      setTotal(data.total);
      setHasMore(data.has_more);
    } catch (err) {
      console.error('Failed to fetch jobs:', err);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, [search, activeFilter]);

  // Initial load + search/filter changes
  useEffect(() => {
    setPage(1);
    fetchJobs(1, false);
  }, [fetchJobs]);

  // ── Debounced search ──
  const handleSearch = (val) => {
    setSearch(val);
    clearTimeout(searchTimer.current);
    searchTimer.current = setTimeout(() => {
      setPage(1);
    }, 350);
  };

  // ── Filter change ─────
  const handleFilter = (key) => {
    setActiveFilter(key);
    setPage(1);
  };

  // ── Load more ─────────
  const handleLoadMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    fetchJobs(nextPage, true);
  };

  // ── Toggle save ───────
  const handleToggleSave = async (job) => {
    try {
      if (job.is_saved) {
        await api.delete(`/jobs/${job.id}/save`);
      } else {
        await api.post(`/jobs/${job.id}/save`);
      }
      // Optimistic update
      setJobs(prev =>
        prev.map(j => j.id === job.id ? { ...j, is_saved: !j.is_saved } : j)
      );
      if (selectedJob?.id === job.id) {
        setSelectedJob(prev => ({ ...prev, is_saved: !prev.is_saved }));
      }
    } catch (err) {
      console.error('Failed to save/unsave job:', err);
    }
  };

  return (
    <div className="page">
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-lg)' }}>
        <h2 className="heading-2">Jobs</h2>
        {!loading && <span className="badge badge-primary">{total} found</span>}
      </div>

      {/* Search */}
      <div className="search-wrapper">
        <HiOutlineSearch />
        <input
          type="text"
          className="form-input"
          placeholder="Search jobs, companies..."
          value={search}
          onChange={(e) => handleSearch(e.target.value)}
          id="job-search-input"
        />
        {search && (
          <button className="search-clear" onClick={() => handleSearch('')} aria-label="Clear search">
            <HiOutlineX />
          </button>
        )}
      </div>

      {/* Filter Chips */}
      <div className="filter-bar">
        {FILTER_CHIPS.map((chip) => (
          <span
            key={chip.key}
            className={`chip${activeFilter === chip.key ? ' active' : ''}`}
            onClick={() => handleFilter(chip.key)}
            role="button"
            tabIndex={0}
            id={`filter-${chip.key}`}
          >
            {chip.label}
          </span>
        ))}
      </div>

      {/* Results Count */}
      {!loading && (
        <div className="results-count">
          Showing <strong>{jobs.length}</strong> of <strong>{total}</strong> jobs
          {search && <> matching "<strong>{search}</strong>"</>}
        </div>
      )}

      {/* Job Cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
        {loading ? (
          <>
            <JobSkeleton />
            <JobSkeleton />
            <JobSkeleton />
            <JobSkeleton />
          </>
        ) : jobs.length === 0 ? (
          <div className="empty-state">
            <HiOutlineBriefcase className="empty-state-icon" />
            <h3 style={{ marginBottom: 4, color: 'var(--text)' }}>No Jobs Found</h3>
            <p className="text-sm">
              {search
                ? `No jobs matching "${search}". Try adjusting your search.`
                : 'No jobs match your current filters.'}
            </p>
            {(search || activeFilter !== 'all') && (
              <button
                className="btn btn-secondary btn-sm"
                style={{ marginTop: 'var(--space-md)' }}
                onClick={() => { setSearch(''); setActiveFilter('all'); }}
              >
                Clear Filters
              </button>
            )}
          </div>
        ) : (
          <>
            {jobs.map((job) => (
              <JobCard
                key={job.id}
                job={job}
                onSelect={setSelectedJob}
                onToggleSave={handleToggleSave}
              />
            ))}

            {hasMore && (
              <button
                className="load-more-btn"
                onClick={handleLoadMore}
                disabled={loadingMore}
              >
                {loadingMore ? (
                  <span className="spinner" style={{ width: 18, height: 18, margin: '0 auto' }} />
                ) : (
                  `Load More (${jobs.length} of ${total})`
                )}
              </button>
            )}
          </>
        )}
      </div>

      {/* Job Detail Bottom Sheet */}
      {selectedJob && (
        <JobDetailSheet
          jobId={selectedJob.id}
          onClose={() => setSelectedJob(null)}
          onToggleSave={handleToggleSave}
        />
      )}
    </div>
  );
}
