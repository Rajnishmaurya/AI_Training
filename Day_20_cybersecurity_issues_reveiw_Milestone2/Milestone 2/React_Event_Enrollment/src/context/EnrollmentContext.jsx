import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState
} from "react";

import { initialEvents } from "../data/events";
import {
  loadRegistrations,
  saveRegistrations
} from "../utils/storage";
const EnrollmentContext = createContext(null);
export function EnrollmentProvider({ children }) {
  const [registrations, setRegistrations] =
    useState(loadRegistrations);
  // Save registrations whenever state changes
  useEffect(() => {
    saveRegistrations(registrations);
  }, [registrations]);
  // Calculate available seats
  const events = useMemo(() => {
    return initialEvents.map((event) => {
      const activeRegistrations =
        registrations.filter(
          (registration) =>
            registration.eventId === event.id &&
            registration.status === "active"
        ).length;
      return {
        ...event,
        availableSeats:
          event.capacity - activeRegistrations
      };
    });
  }, [registrations]);
  // Register attendee
  function registerAttendee(
    eventId,
    fullName,
    email
  ) {
    const normalizedEmail =
      email.trim().toLowerCase();
    const event = events.find(
      (item) => item.id === eventId
    );
    if (!event) {
      return {
        success: false,
        message: "Event not found."
      };
    }
    if (event.availableSeats <= 0) {
      return {
        success: false,
        message: "Sorry, this event is fully booked."
      };
    }
    // Check duplicate email for same event
    const duplicate = registrations.some(
      (registration) =>
        registration.eventId === eventId &&
        registration.email.trim().toLowerCase() === normalizedEmail);
    if (duplicate) {
      return {
        success: false,
        message:
          "This email is already registered for this event."
      };
    }
    const newRegistration = {
      id:
        `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      eventId,
      fullName: fullName.trim(),
      email: normalizedEmail,
      status: "active",
      createdAt: new Date().toISOString()
    };
    setRegistrations((current) => [
      ...current,
      newRegistration
    ]);
    return {
      success: true,
      message:
        "Registration completed successfully!"
    };
  }

  // Cancel registration
  function cancelRegistration(registrationId) {
    setRegistrations((current) =>
      current.map((registration) =>
        registration.id === registrationId
          ? {
              ...registration,
              status: "cancelled"
            }
          : registration
      )
    );
  }

  const value = {
    events,
    registrations: registrations.filter(
      (item) => item.status === "active"
    ),

    registerAttendee,

    cancelRegistration

  };

  return (
    <EnrollmentContext.Provider value={value}>

      {children}

    </EnrollmentContext.Provider>

  );

}

// Custom hook
export function useEnrollment() {

  const context = useContext(EnrollmentContext);

  if (!context) {

    throw new Error(
      "useEnrollment must be used inside EnrollmentProvider"
    );

  }

  return context;

}