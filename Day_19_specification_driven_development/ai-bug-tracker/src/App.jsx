
import React from "react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import DashboardCards from "./components/DashboardCards";
import BugTable from "./components/BugTable";
import CreateBugForm from "./components/CreateBugForm";
import BugDetails from "./components/BugDetails";

import {
  getBugs,
  getBugStats,
  createBug as createBugRequest,
  updateBug as updateBugRequest,
} from "./services/bugService";

import "./App.css";

function App() {
  const [bugs, setBugs] = React.useState([]);
  const [searchText, setSearchText] = React.useState("");
  const [showCreateForm, setShowCreateForm] = React.useState(false);
  const [selectedBug, setSelectedBug] = React.useState(null);
  const [isLoading, setIsLoading] = React.useState(true);
  const [apiError, setApiError] = React.useState("");

  const [stats, setStats] = React.useState(null);
  const [statsLoading, setStatsLoading] = React.useState(true);
  const [statsError, setStatsError] = React.useState("");

  async function refreshStats() {
    setStatsLoading(true);
    setStatsError("");

    try {
      const data = await getBugStats();
      setStats(data);
    } catch (error) {
      setStatsError(
        error.message || "Failed to load dashboard statistics"
      );
    } finally {
      setStatsLoading(false);
    }
  }

  React.useEffect(() => {
    let cancelled = false;

    async function loadInitialData() {
      try {
        const [bugsData, statsData] = await Promise.all([
          getBugs(),
          getBugStats(),
        ]);

        if (!cancelled) {
          setBugs(bugsData);
          setStats(statsData);
          setApiError("");
          setStatsError("");
        }
      } catch (error) {
        if (!cancelled) {
          setApiError(error.message || "Failed to load bugs");
          setStatsError(
            error.message || "Failed to load dashboard statistics"
          );
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
          setStatsLoading(false);
        }
      }
    }

    loadInitialData();

    return () => {
      cancelled = true;
    };
  }, []);

  async function handleCreateBug(formData) {
    try {
      const newBug = await createBugRequest(formData);

      setBugs((previousBugs) => [newBug, ...previousBugs]);
      setApiError("");
      setShowCreateForm(false);

      await refreshStats();
    } catch (error) {
      setApiError(`Could not create bug: ${error.message}`);
      window.alert(`Could not create bug: ${error.message}`);
    }
  }

  async function handleUpdateBug(updatedBug) {
    try {
      const savedBug = await updateBugRequest(updatedBug.id, {
        status: updatedBug.status,
        assignee: updatedBug.assignee,
      });

      setBugs((previousBugs) =>
        previousBugs.map((bug) =>
          bug.id === savedBug.id ? savedBug : bug
        )
      );

      setSelectedBug(savedBug);
      setApiError("");

      await refreshStats();
    } catch (error) {
      setApiError(`Could not update bug: ${error.message}`);
      window.alert(`Could not update bug: ${error.message}`);
    }
  }

  return (
    <div className="app">
      <Sidebar />

      <main className="main-content">
        <Header
          onCreateBug={() => setShowCreateForm(true)}
          searchText={searchText}
          onSearchChange={setSearchText}
        />

        {apiError && (
          <div className="api-error" role="alert">
            <span>{apiError}</span>
            <button
              type="button"
              onClick={() => setApiError("")}
              aria-label="Dismiss error"
            >
              ×
            </button>
          </div>
        )}

        {isLoading ? (
          <p className="api-loading">Loading bugs from the API...</p>
        ) : (
          <>
            <DashboardCards
              stats={stats}
              loading={statsLoading}
            />

            {statsError && (
              <p className="api-error" role="alert">
                Dashboard statistics unavailable: {statsError}
              </p>
            )}

            <BugTable
              bugs={bugs}
              searchText={searchText}
              onSelectBug={setSelectedBug}
            />
          </>
        )}
      </main>

      {showCreateForm && (
        <CreateBugForm
          onCreate={handleCreateBug}
          onCancel={() => setShowCreateForm(false)}
        />
      )}

      {selectedBug && (
        <BugDetails
          bug={selectedBug}
          onClose={() => setSelectedBug(null)}
          onUpdate={handleUpdateBug}
        />
      )}
    </div>
  );
}

export default App;
