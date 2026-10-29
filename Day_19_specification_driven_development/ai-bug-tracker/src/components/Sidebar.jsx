
import React from "react";
import "./Sidebar.css";

const navigationItems = [
  { label: "Dashboard", icon: "▦" },
  { label: "All Bugs", icon: "◈" },
  { label: "My Bugs", icon: "♙" },
  { label: "Reports", icon: "▥" },
];

function Sidebar() {
  const [activeItem, setActiveItem] = React.useState("Dashboard");

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">B</div>
        <div>
          <h2>BugPilot</h2>
          <span>AI Issue Tracker</span>
        </div>
      </div>

      <div className="sidebar-label">WORKSPACE</div>

      <nav className="sidebar-nav">
        {navigationItems.map((item) => (
          <button
            key={item.label}
            className={`nav-item ${
              activeItem === item.label ? "active" : ""
            }`}
            onClick={() => setActiveItem(item.label)}
            type="button"
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <div className="ai-card">
          <div className="ai-card-icon">✦</div>
          <strong>AI Assistant</strong>
          <p>Smarter bug triage starts here.</p>
          <span className="ai-status">
            <span className="status-dot" />
            Ready to assist
          </span>
        </div>

        <div className="profile">
          <div className="avatar">DM</div>
          <div className="profile-info">
            <strong>Demo User</strong>
            <span>Developer</span>
          </div>
          <span className="profile-menu">···</span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
