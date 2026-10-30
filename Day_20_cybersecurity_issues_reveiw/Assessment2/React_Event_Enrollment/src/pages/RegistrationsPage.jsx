import { useEnrollment } from "../context/EnrollmentContext";

function formatDate(dateString) {

  return new Date(
    `${dateString}T00:00:00`
  ).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric"
  });
}

export default function RegistrationsPage() {
  const {
    registrations,
    events,
    cancelRegistration
  } = useEnrollment();

  function handleCancel(
    registrationId,
    attendeeName
  ) {

    const confirmed = window.confirm(
      `Cancel the registration for ${attendeeName}? ` +
      "This will restore one available seat."
    );
    if (confirmed) {
      cancelRegistration(registrationId);
    }
  }
  return (
    <section className="registrations-section">
      <div className="page-hero compact-hero">
        <span className="eyebrow">
          ATTENDEE MANAGEMENT
        </span>
        <h1>
          Your <span>registrations.</span>
        </h1>
        <p>
          View active event bookings and cancel
          a registration when plans change.
        </p>
      </div>
      <div className="section-heading registration-heading">
        <div>
          <span className="eyebrow">
            BOOKING OVERVIEW
          </span>
          <h2>
            Active registrations{" "}
            <span className="count-badge">
              {registrations.length}
            </span>
          </h2>
        </div>
      </div>
      {registrations.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">
          </div>
          <h3>No registrations yet</h3>
          <p>When you register for an event,your booking will appear here.</p>
          <a
            className="button button-primary link-button"
            href="/"
          >
            Explore events
          </a>
        </div>
      ) : (
        <div className="registration-list">
          {registrations.map((registration) => {
            const event = events.find(
              (item) =>
                item.id === registration.eventId
            );
            if (!event) return null;
            return (
              <article
                className="registration-card"
                key={registration.id}
              >
                <div className="registration-avatar">
                  {registration.fullName
                    .trim()
                    .charAt(0)
                    .toUpperCase()}
                </div>
                <div className="registration-info">
                  <h3>{registration.fullName}</h3>
                  <p>{registration.email}</p>
                  <div className="registration-event">
                    <strong>{event.title}</strong>
                    <span>
                      {formatDate(event.date)}
                      {" · "}
                      {event.time}
                    </span>
                  </div>
                </div>
                <button
                  className="button button-danger"
                  onClick={() =>
                    handleCancel(
                      registration.id,
                      registration.fullName
                    )
                  }
                >
                  Cancel registration
                </button>
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}