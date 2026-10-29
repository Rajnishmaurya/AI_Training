
import React from "react";
import "./BugTable.css";

export const sampleBugs = [
  {
    id: "BUG-1042",
    title: "Login fails after password reset",
    category: "Authentication",
    priority: "Critical",
    status: "Open",
    assignee: "A. Sharma",
    initials: "AS",
    date: "Oct 29, 2026",
  },
  {
    id: "BUG-1041",
    title: "Dashboard charts not loading",
    category: "Dashboard",
    priority: "High",
    status: "In Progress",
    assignee: "R. Kumar",
    initials: "RK",
    date: "Oct 28, 2026",
  },
  {
    id: "BUG-1040",
    title: "Incorrect date in export report",
    category: "Reporting",
    priority: "Medium",
    status: "Open",
    assignee: "P. Singh",
    initials: "PS",
    date: "Oct 28, 2026",
  },
  {
    id: "BUG-1039",
    title: "Profile image upload timeout",
    category: "User Profile",
    priority: "Low",
    status: "Resolved",
    assignee: "A. Sharma",
    initials: "AS",
    date: "Oct 27, 2026",
  },
  {
    id: "BUG-1038",
    title: "Search returns duplicate results",
    category: "Search",
    priority: "High",
    status: "In Progress",
    assignee: "R. Kumar",
    initials: "RK",
    date: "Oct 26, 2026",
  },
];

function BugTable({ bugs, searchText, onSelectBug }) {
  const [statusFilter, setStatusFilter] = React.useState("All");
  const [priorityFilter, setPriorityFilter] = React.useState("All");

  const filteredBugs = bugs.filter((bug) => {
  const matchesStatus =
    statusFilter === "All" || bug.status === statusFilter;

  const matchesPriority =
    priorityFilter === "All" || bug.priority === priorityFilter;

  const query = searchText.trim().toLowerCase();

  const matchesSearch =
    !query ||
    [
      bug.id,
      bug.title,
      bug.category,
      bug.assignee,
      bug.status,
      bug.priority,
    ].some((value) =>
      String(value ?? "").toLowerCase().includes(query)
    );

  return matchesStatus && matchesPriority && matchesSearch;
});

  return (
    <section className="bug-table-section">
      <div className="bug-table-heading">
        <div>
          <h2>Recent Bugs</h2>
          <p>Track and manage the latest reported issues.</p>
        </div>

        <button className="view-all-button" type="button">
          View all →
        </button>
      </div>

      <div className="bug-filters">
        <label>
          Status:
          <select
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="All">All statuses</option>
            <option value="Open">Open</option>
            <option value="In Progress">In Progress</option>
            <option value="Resolved">Resolved</option>
          </select>
        </label>

        <label>
          Priority:
          <select
            value={priorityFilter}
            onChange={(event) => setPriorityFilter(event.target.value)}
          >
            <option value="All">All priorities</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </label>
      </div>

      <div className="bug-table-scroll">
        <table className="bug-table">
          <thead>
            <tr>
              <th>BUG ID / TITLE</th>
              <th>PRIORITY</th>
              <th>STATUS</th>
              <th>ASSIGNEE</th>
              <th>REPORTED</th>
            </tr>
          </thead>

          <tbody>
            {filteredBugs.map((bug) => (
              
<tr
  key={bug.id}
  className="bug-table-row"
  onClick={() => onSelectBug(bug)}
  onKeyDown={(event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onSelectBug(bug);
    }
  }}
  tabIndex={0}
  aria-label={`View details for ${bug.id}: ${bug.title}`}
>

                <td>
                  <div className="bug-title-cell">
                    <span className="bug-id">{bug.id}</span>
                    <strong>{bug.title}</strong>
                    <span className="bug-category">{bug.category}</span>
                  </div>
                </td>

                <td>
                  <span
                    className={`priority-badge ${bug.priority.toLowerCase()}`}
                  >
                    <span className="badge-dot" />
                    {bug.priority}
                  </span>
                </td>

                <td>
                  <span
                    className={`status-badge ${
                      bug.status.toLowerCase().replace(" ", "-")
                    }`}
                  >
                    {bug.status}
                  </span>
                </td>

                <td>
                  <div className="assignee-cell">
                    <span className="assignee-avatar">{bug.initials}</span>
                    <span>{bug.assignee}</span>
                  </div>
                </td>

                <td className="bug-date">{bug.date}</td>
              </tr>
            ))}

            {filteredBugs.length === 0 && (
              <tr>
                <td colSpan="5" className="empty-state">
                  No bugs match these filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="bug-table-footer">
        Showing {filteredBugs.length} of {bugs.length} bugs
      </div>
    </section>
  );
}

export default BugTable;
