import { NavLink } from 'react-router-dom';
import {
  HiOutlineHome, HiOutlineBriefcase,
  HiOutlineClipboardList, HiOutlineLightningBolt,
  HiOutlineUser,
} from 'react-icons/hi';

const navItems = [
  { to: '/', icon: <HiOutlineHome />, label: 'Home' },
  { to: '/jobs', icon: <HiOutlineBriefcase />, label: 'Jobs' },
  { to: '/applications', icon: <HiOutlineClipboardList />, label: 'Applications' },
  { to: '/automation', icon: <HiOutlineLightningBolt />, label: 'Automation' },
  { to: '/profile', icon: <HiOutlineUser />, label: 'Profile' },
];

export default function BottomNav() {
  return (
    <nav className="bottom-nav" role="navigation" aria-label="Main navigation">
      {navItems.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
          end={item.to === '/'}
          id={`nav-${item.label.toLowerCase()}`}
        >
          {item.icon}
          <span>{item.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}
