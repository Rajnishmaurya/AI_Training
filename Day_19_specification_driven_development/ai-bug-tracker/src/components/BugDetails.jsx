
import React from "react";
import "./BugDetails.css";

function BugDetails({ bug, onClose, onUpdate }) {
  const [isEditing, setIsEditing] = React.useState(false);
  const [status, setStatus] = React.useState(bug?.status ?? "Open");
  const [assignee, setAssignee] = React.useState(
    bug?.assignee === "Unassigned" ? "" : bug?.assignee ?? ""
  );

  React.useEffect(() => {
    setStatus(bug?.status ?? "Open");
    setAssignee(
      bug?.assignee === "Unassigned" ? "" : bug?.assignee ?? ""
    );
    setIsEditing(false);
  }, [bug]);

  if (!bug) {
    return null;
  }

  function handleBackdropClick(event) {
    if (event.target === event.currentTarget) {
      onClose();
    }
  }

  function handleSave() {
    const cleanAssignee = assignee.trim() || "Unassigned";

    const initials =
      cleanAssignee === "Unassigned"
        ? "UN"
        : cleanAssignee
            .split(/\s+/)
            .map((part) => part[0])
            .join("")
            .slice(0, 2)
            .toUpperCase();

    onUpdate({
      ...bug,
      status,
      assignee: cleanAssignee,
      initials,
    });

    setIsEditing(false);
  }

  return (
    <div
      className="bug-details-backdrop"
      onMouseDown={handleBackdropClick}
    >
      <aside
        className="bug-details-panel"
        role="dialog"
        aria-modal="true"
        aria-labelledby="bug-details-heading"
      >
        <div className="bug-details-header">
          <div>
            <span className="bug-details-id">{bug.id}</span>
            <h2 id="bug-details-heading">Bug Details</h2>
          </div>

          <button
            className="bug-details-close"
            type="button"
            onClick={onClose}
            aria-label="Close bug details"
          >
            ×
          </button>
        </div>

        <div className="bug-details-content">
          <div className="bug-details-title-section">
            <span
              className={`priority-badge ${bug.priority.toLowerCase()}`}
            >
              <span className="badge-dot" />
              {bug.priority} Priority
            </span>

            <h3>{bug.title}</h3>

            <span
              className={`status-badge ${
                (isEditing ? status : bug.status)
                  .toLowerCase()
                  .replace(" ", "-")
              }`}
            >
              {isEditing ? status : bug.status}
            </span>
          </div>

          <section className="bug-details-section">
            <h4>Description</h4>
            <p className="bug-details-description">
              {bug.description ||
                "No description was provided for this bug yet."}
            </p>
          </section>

          <section className="bug-details-section">
            <h4>Issue Information</h4>

            <div className="bug-detail-row">
              <span>Category</span>
              <strong>{bug.category || "Other"}</strong>
            </div>

            <div className="bug-detail-row">
              <span>Priority</span>
              <strong>{bug.priority}</strong>
            </div>

            <div className="bug-detail-row">
              <span>Status</span>
              {isEditing ? (
                <select
                  className="bug-edit-select"
                  value={status}
                  onChange={(event) => setStatus(event.target.value)}
                  aria-label="Bug status"
                >
                  <option value="Open">Open</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Resolved">Resolved</option>
                </select>
              ) : (
                <strong>{bug.status}</strong>
              )}
            </div>

            <div className="bug-detail-row">
              <span>Reported</span>
              <strong>{bug.date || "Not available"}</strong>
            </div>
          </section>

          <section className="bug-details-section">
            <h4>Assigned To</h4>

            {isEditing ? (
              <div className="bug-edit-field">
                <label htmlFor="bug-assignee-edit">Assignee name</label>
                <input
                  id="bug-assignee-edit"
                  type="text"
                  value={assignee}
                  onChange={(event) => setAssignee(event.target.value)}
                  placeholder="Enter assignee name"
                  maxLength={100}
                />
                <p className="bug-edit-hint">
                  Leave blank to mark this bug as unassigned.
                </p>
              </div>
            ) : (
              <div className="bug-details-assignee">
                <span className="assignee-avatar">
                  {bug.initials || "UN"}
                </span>

                <div>
                  <strong>{bug.assignee || "Unassigned"}</strong>
                  <p>Bug assignee</p>
                </div>
              </div>
            )}
          </section>

          <div className="bug-details-note">
            <span>✦</span>
            <div>
              <strong>AI Assistant</strong>
              <p>
                AI-powered triage and suggested fixes can be added
                when we connect the backend.
              </p>
            </div>
          </div>
        </div>

        <div className="bug-details-footer">
          {isEditing ? (
            <div className="bug-edit-actions">
              <button
                className="bug-edit-cancel"
                type="button"
                onClick={() => {
                  setStatus(bug.status);
                  setAssignee(
                    bug.assignee === "Unassigned" ? "" : bug.assignee
                  );
                  setIsEditing(false);
                }}
              >
                Cancel
              </button>

              <button
                className="bug-details-done"
                type="button"
                onClick={handleSave}
              >
                Save Changes
              </button>
            </div>
          ) : (
            <div className="bug-edit-actions">
              <button
                className="bug-edit-button"
                type="button"
                onClick={() => setIsEditing(true)}
              >
                Edit Bug
              </button>

              <button
                className="bug-details-done"
                type="button"
                onClick={onClose}
              >
                Close Details
              </button>
            </div>
          )}
        </div>
      </aside>
    </div>
  );
}

export default BugDetails;
