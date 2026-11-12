function formatDate(dateString) {

  return new Date(
    `${dateString}T00:00:00`
  ).toLocaleDateString("en-IN", {

    day: "numeric",
    month: "short",
    year: "numeric"

  });

}

export default function EventCard({
  event,
  onRegister
}) {

  const isFull = event.availableSeats <= 0;

  return (
    <article className="event-card">
      <div className="card-topline">
        <span className="category-pill">
          {event.category}
        </span>
        <span className="event-id">
          {event.id}
        </span>
      </div>
      <h2>
        {event.title}
      </h2>
      <div className="event-meta">
        <span>
          ▦ {formatDate(event.date)}
        </span>
        <span>
          ◷ {event.time}
        </span>
      </div>
      <div className="seat-row">
        <span>
          Available seats
        </span>
        <strong className={
          isFull ? "seats-full" : ""
        }>
          {event.availableSeats} / {event.capacity}
        </strong>
      </div>
      <div className="seat-track">
        <div
          className="seat-fill"
          style={{
            width:
              `${(event.availableSeats / event.capacity) * 100}%`
          }}
        />
      </div>
      <button
        className="button button-primary full-width"
        disabled={isFull}
        onClick={() => onRegister(event)}
      >
        {isFull
          ? "Fully booked"
          : "Register now"
        }
      </button>
    </article>
  );
}