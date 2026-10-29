
import React from "react";
import "./CreateBugForm.css";

const initialForm = {
  title: "",
  description: "",
  category: "Other",
  priority: "Medium",
  assignee: "",
};

function CreateBugForm({ onCreate, onCancel }) {
  const [form, setForm] = React.useState(initialForm);
  const [error, setError] = React.useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));

    setError("");
  }

  function handleSubmit(event) {
    event.preventDefault();

    if (!form.title.trim()) {
      setError("Please enter a bug title.");
      return;
    }

    if (!form.description.trim()) {
      setError("Please enter a description.");
      return;
    }

    onCreate({
      ...form,
      title: form.title.trim(),
      description: form.description.trim(),
      assignee: form.assignee.trim() || "Unassigned",
    });

    setForm(initialForm);
    setError("");
  }

  return (
    <div className="bug-form-overlay">
      <section
        className="bug-form-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="create-bug-title"
      >
        <div className="bug-form-heading">
          <div>
            <h2 id="create-bug-title">Create New Bug</h2>
            <p>Provide details about the issue you found.</p>
          </div>

          <button
            className="form-close-button"
            type="button"
            onClick={onCancel}
            aria-label="Close form"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-field">
            <label htmlFor="bug-title">Bug title *</label>
            <input
              id="bug-title"
              name="title"
              value={form.title}
              onChange={handleChange}
              placeholder="e.g. Login fails after password reset"
              maxLength={150}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="bug-description">Description *</label>
            <textarea
              id="bug-description"
              name="description"
              value={form.description}
              onChange={handleChange}
              placeholder="Describe the issue and steps to reproduce it..."
              rows={4}
              maxLength={5000}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-field">
              <label htmlFor="bug-category">Category</label>
              <select
                id="bug-category"
                name="category"
                value={form.category}
                onChange={handleChange}
              >
                <option>Other</option>
                <option>Authentication</option>
                <option>Dashboard</option>
                <option>Reporting</option>
                <option>User Profile</option>
                <option>Search</option>
                <option>Performance</option>
                <option>API</option>
              </select>
            </div>

            <div className="form-field">
              <label htmlFor="bug-priority">Priority</label>
              <select
                id="bug-priority"
                name="priority"
                value={form.priority}
                onChange={handleChange}
              >
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
                <option>Critical</option>
              </select>
            </div>
          </div>

          <div className="form-field">
            <label htmlFor="bug-assignee">Assignee</label>
            <input
              id="bug-assignee"
              name="assignee"
              value={form.assignee}
              onChange={handleChange}
              placeholder="Enter a name (optional)"
              maxLength={100}
            />
          </div>

          {error && (
            <p className="form-error" role="alert">
              {error}
            </p>
          )}

          <div className="bug-form-actions">
            <button
              className="form-cancel-button"
              type="button"
              onClick={onCancel}
            >
              Cancel
            </button>

            <button className="form-submit-button" type="submit">
              Create Bug
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}

export default CreateBugForm;
