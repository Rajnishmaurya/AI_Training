import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="site-header">
      <div className="nav-inner">
        <NavLink to="/" className="brand">
          <span className="brand-mark">
            E
          </span>
          <span>
            Event
            <span className="brand-light">
              Hub
            </span>
          </span>
        </NavLink>
        <nav
          className="nav-links"
          aria-label="Main navigation"
        >
          <NavLink to="/" end>
            Events
          </NavLink>
          <NavLink to="/registrations">
            Registrations
          </NavLink>
        </nav>
      </div>
    </header>
  );
}