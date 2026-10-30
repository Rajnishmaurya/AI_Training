const STORAGE_KEY =
  "event-enrollment-registrations";

export function loadRegistrations() {
  try {
    const saved =
      localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  } catch (error) {
    console.error(
      "Could not read saved registrations:",
      error
    );
    return [];
  }
}

export function saveRegistrations(registrations) {

  try {

    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(registrations)
    );

  } catch (error) {

    console.error(
      "Could not save registrations:",
      error
    );

  }

}