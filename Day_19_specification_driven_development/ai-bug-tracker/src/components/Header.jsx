
import React from "react";
import "./Header.css";

function Header({ onCreateBug, searchText, onSearchChange }) {
  return (
    <header className="header">
      <div className="header-title">
        <h1>Dashboard</h1>
        <p>Track, manage, and resolve bugs efficiently.</p>
      </div>

      <div className="header-actions">
        <div className="search-box">
          <span className="search-icon">⌕</span>

          <input
            type="search"
            placeholder="Search bugs..."
            value={searchText}
            onChange={(event) => onSearchChange(event.target.value)}
            aria-label="Search bugs"
          />

          {searchText && (
            <button
              type="button"
              className="clear-search"
              onClick={() => onSearchChange("")}
              aria-label="Clear search"
            >
              ×
            </button>
          )}

          <span className="search-shortcut">⌘ K</span>
        </div>

        <button
          className="notification-button"
          type="button"
          aria-label="Notifications"
          onClick={() => alert("Notifications will be added later.")}
        >
          ♧
          <span className="notification-dot" />
        </button>

        <button
          className="create-bug-button"
          type="button"
          onClick={onCreateBug}
        >
          <span>＋</span> Create Bug
        </button>
      </div>
    </header>
  );
}

export default Header;
