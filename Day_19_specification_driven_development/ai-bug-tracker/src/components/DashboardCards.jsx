
import "./DashboardCards.css";

const cards = [
  {
    key: "total_bugs",
    label: "Total Bugs",
    color: "blue",
    description: "All reported bugs",
  },
  {
    key: "open_bugs",
    label: "Open Bugs",
    color: "red",
    description: "Awaiting action",
  },
  {
    key: "in_progress_bugs",
    label: "In Progress",
    color: "orange",
    description: "Currently being worked on",
  },
  {
    key: "resolved_bugs",
    label: "Resolved",
    color: "green",
    description: "Successfully resolved",
  },
];

export default function DashboardCards({
  stats,
  loading = false,
}) {
  return (
    <section className="dashboard-cards">
      {cards.map((card) => (
        <article
          className="dashboard-card"
          key={card.key}
        >
          <div className="dashboard-card-top">
            <span className="dashboard-card-label">
              {card.label}
            </span>

            <span
              className={`dashboard-card-icon ${card.color}`}
              aria-hidden="true"
            >
              {card.color === "blue" && "Σ"}
              {card.color === "red" && "!"}
              {card.color === "orange" && "↻"}
              {card.color === "green" && "✓"}
            </span>
          </div>

          <div className="dashboard-card-value">
            {loading ? "..." : (stats?.[card.key] ?? 0)}
          </div>

          <div className="dashboard-card-description">
            {card.description}
          </div>
        </article>
      ))}
    </section>
  );
}
