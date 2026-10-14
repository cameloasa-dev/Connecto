import { useSearchParams, useNavigate } from "react-router-dom";
import { useSearchQuery } from "../hooks/search/useSearchQuery";
import { useState, useEffect } from "react";
import "./SearchPage.css";

function SearchPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const query = searchParams.get("q") ?? "";
  const activeTab = searchParams.get("tab") ?? "users";

  const [inputValue, setInputValue] = useState(query);

  const { data, isLoading, error } = useSearchQuery(query);

  const results = data ?? { users: [], circles: [], posts: [] };

  // Sync input when URL changes
  useEffect(() => {
    setInputValue(query);
  }, [query]);

  const updateQuery = (newQuery) => {
    const params = new URLSearchParams(searchParams);
    params.set("q", newQuery);
    params.set("tab", "users"); // reset tab on new search
    navigate(`/search?${params.toString()}`);
  };

  const setTab = (tab) => {
    const params = new URLSearchParams(searchParams);
    params.set("tab", tab);
    navigate(`/search?${params.toString()}`);
  };

  const onSearchSubmit = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    updateQuery(inputValue.trim());
  };

  return (
    <main className="dashboard-main">
      {/* SEARCH INPUT */}
      <form onSubmit={onSearchSubmit} className="search-bar">
        <input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Search users, circles, posts..."
        />
        <button type="submit">Search</button>
      </form>

      {/* EMPTY STATE */}
      {!query && (
        <p className="empty-state">Start by searching something above 👆</p>
      )}

      {/* ERROR */}
      {error && <p className="error">Search failed. Try again later.</p>}

      {/* HEADER */}
      {query && (
        <div className="search-header">
          <h1>{`Results for "${query}"`}</h1>

          <p className="results-count">
            Found {results.users.length} users, {results.circles.length}{" "}
            circles, {results.posts.length} posts
          </p>
        </div>
      )}

      {/* TABS */}
      {query && (
        <div className="search-tabs">
          <button
            className={activeTab === "users" ? "tab active" : "tab"}
            onClick={() => setTab("users")}
          >
            Users ({results.users.length})
          </button>

          <button
            className={activeTab === "circles" ? "tab active" : "tab"}
            onClick={() => setTab("circles")}
          >
            Circles ({results.circles.length})
          </button>

          <button
            className={activeTab === "posts" ? "tab active" : "tab"}
            onClick={() => setTab("posts")}
          >
            Posts ({results.posts.length})
          </button>
        </div>
      )}

      {/* RESULTS */}
      <div className="search-results">
        {isLoading && query && (
          <div className="loading-spinner">Searching...</div>
        )}

        {/* USERS */}
        {query && activeTab === "users" && (
          <div className="users-grid">
            {results.users.map((user) => (
              <div key={user.id} className="user-card">
                <div className="user-avatar">
                  {user.username?.charAt(0).toUpperCase()}
                </div>

                <div className="user-info">
                  <h3>{user.username}</h3>
                  <p>{user.email}</p>
                </div>

                <button
                  className="view-btn"
                  onClick={() => navigate(`/profile/${user.id}`)}
                >
                  View Profile
                </button>
              </div>
            ))}
          </div>
        )}

        {/* CIRCLES */}
        {query && activeTab === "circles" && (
          <div className="circles-grid">
            {results.circles.map((circle) => (
              <div key={circle.id} className="circle-card">
                <h3>{circle.name}</h3>
                <p>{circle.description}</p>

                <button
                  className="view-btn"
                  onClick={() => navigate(`/circles/${circle.id}`)}
                >
                  View Circle
                </button>
              </div>
            ))}
          </div>
        )}

        {/* POSTS */}
        {query && activeTab === "posts" && (
          <div className="posts-feed">
            {results.posts.map((post) => (
              <div
                key={post.id}
                className="post-card"
                onClick={() => navigate(`/posts/${post.id}`)}
              >
                <h4>{post.title}</h4>
                <p>{post.content}</p>

                <div className="post-meta">
                  <span>Posted by {post.author_name}</span>
                  <span>{new Date(post.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* DEBUG */}
      {import.meta.env.DEV && (
        <details className="debug-info">
          <summary>Debug Search State</summary>
          <pre>
            {JSON.stringify(
              { query, activeTab, data, isLoading, error },
              null,
              2,
            )}
          </pre>
        </details>
      )}
    </main>
  );
}

export default SearchPage;
