import { useMemo, useState } from "react";
import EventCard from "../components/EventCard";
import RegistrationModal from "../components/RegistrationModal";
import { useEnrollment } from "../context/EnrollmentContext";

const categories = [
  "All",
  "Technology",
  "Arts",
  "Life Skills"
];

export default function EventsPage() {

  const {
    events,
    registerAttendee
  } = useEnrollment();

  const [search, setSearch] =
    useState("");

  const [category, setCategory] =
    useState("All");

  const [selectedEvent, setSelectedEvent] =
    useState(null);

  // Search and category filtering
  const filteredEvents = useMemo(() => {

    return events.filter((event) => {

      const matchesSearch =
        event.title
          .toLowerCase()
          .includes(search.trim().toLowerCase());

      const matchesCategory =
        category === "All" ||
        event.category === category;

      return matchesSearch && matchesCategory;

    });

  }, [events, search, category]);

  return (

    <>

      <section className="page-hero">

        <span className="eyebrow">
          LEARN · CREATE · CONNECT
        </span>

        <h1>
          Discover your next{" "}
          <span>
            learning experience.
          </span>
        </h1>

        <p>
          Explore practical workshops and reserve
          your place in our upcoming community events.
        </p>

      </section>

      <section className="events-section">

        <div className="section-heading">

          <div>

            <span className="eyebrow">
              WHAT'S COMING UP
            </span>

            <h2>
              Upcoming events{" "}
              <span className="count-badge">
                {events.length}
              </span>
            </h2>

          </div>

          <p>
            {filteredEvents.length} events found
          </p>

        </div>

        {/* Search and category filters */}

        <div className="filters">

          <div className="search-wrap">

            <span aria-hidden="true">
              ⌕
            </span>

            <input
              aria-label="Search event title"
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
              placeholder="Search events by title..."
            />

            {search && (

              <button
                onClick={() => setSearch("")}
                aria-label="Clear search"
              >
                ×
              </button>

            )}

          </div>

          <div
            className="category-filters"
            aria-label="Filter by category"
          >

            {categories.map((item) => (

              <button
                key={item}
                className={
                  `filter-chip ${
                    category === item ? "active" : ""
                  }`
                }
                onClick={() =>
                  setCategory(item)
                }
              >
                {item}
              </button>

            ))}

          </div>

        </div>

        {/* Event listing */}

        {filteredEvents.length > 0 ? (

          <div className="event-grid">

            {filteredEvents.map((event) => (

              <EventCard
                key={event.id}
                event={event}
                onRegister={setSelectedEvent}
              />

            ))}

          </div>

        ) : (

          <div className="empty-state">

            <div className="empty-icon">
              ⌕
            </div>

            <h3>
              No events found
            </h3>

            <p>
              Try another search term or choose
              a different category.
            </p>

            <button
              className="button button-secondary"
              onClick={() => {

                setSearch("");

                setCategory("All");

              }}
            >
              Clear filters
            </button>

          </div>

        )}

      </section>

      {/* Registration form */}

      {selectedEvent && (

        <RegistrationModal

          event={selectedEvent}

          onClose={() =>
            setSelectedEvent(null)
          }

          onSubmit={registerAttendee}

        />

      )}

    </>

  );

}