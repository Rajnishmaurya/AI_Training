import { useState } from "react";

export default function RegistrationModal({
  event,
  onClose,
  onSubmit
}) {

  const [fullName, setFullName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [error, setError] =
    useState("");

  const [submitting, setSubmitting] =
    useState(false);

  function handleSubmit(eventObject) {

    eventObject.preventDefault();

    setError("");

    if (!fullName.trim() || !email.trim()) {

      setError(
        "Please enter your full name and email address."
      );

      return;

    }

    const emailPattern =
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email.trim())) {

      setError(
        "Please enter a valid email address."
      );

      return;

    }

    setSubmitting(true);

    const result = onSubmit(
      event.id,
      fullName,
      email
    );

    setSubmitting(false);

    if (!result.success) {

      setError(result.message);

      return;

    }

    onClose();

    window.alert(result.message);

  }

  if (!event) return null;

  return (

    <div
      className="modal-backdrop"
      onMouseDown={onClose}
    >

      <section
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        onMouseDown={(eventObject) =>
          eventObject.stopPropagation()
        }
      >

        <button
          className="modal-close"
          onClick={onClose}
          aria-label="Close"
        >
          ×
        </button>

        <span className="eyebrow">
          EVENT REGISTRATION
        </span>

        <h2 id="modal-title">
          Reserve your seat
        </h2>

        <p className="modal-event-name">
          {event.title}
        </p>

        <form
          onSubmit={handleSubmit}
          noValidate
        >

          <label htmlFor="fullName">
            Full name
          </label>

          <input
            id="fullName"
            value={fullName}
            onChange={(e) =>
              setFullName(e.target.value)
            }
            placeholder="Enter your full name"
            autoComplete="name"
          />

          <label htmlFor="email">
            Email address
          </label>

          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            placeholder="you@example.com"
            autoComplete="email"
          />

          {error && (

            <p
              className="form-error"
              role="alert"
            >
              {error}
            </p>

          )}

          <div className="modal-actions">

            <button
              type="button"
              className="button button-secondary"
              onClick={onClose}
            >
              Cancel
            </button>

            <button
              type="submit"
              className="button button-primary"
              disabled={submitting}
            >
              Confirm registration
            </button>

          </div>

        </form>

      </section>

    </div>

  );

}