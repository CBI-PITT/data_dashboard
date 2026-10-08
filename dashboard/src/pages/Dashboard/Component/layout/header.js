import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import HOST from "../../../../config/path";

const styles = {
  header: {
    position: "sticky",
    top: 0,
    zIndex: 1020,
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: "12px",
    padding: "12px 20px",
    backgroundColor: "#1b2129",
    color: "#e8edf4",
  },
  brand: {
    fontWeight: 600,
    fontSize: "1.1rem",
    margin: 0,
    whiteSpace: "nowrap",
  },
  links: { display: "flex", alignItems: "center", gap: "16px" },
  link: {
    color: "#e8edf4",
    textDecoration: "none",
    fontSize: "0.95rem",
    whiteSpace: "nowrap",
  },
  user: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    fontWeight: 500,
    fontSize: "0.95rem",
    whiteSpace: "nowrap",
  },
  admin: { color: "#9aa7b8", fontWeight: 400 },
};

export default function Header() {
  const [user, setUser] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    axios
      .get(HOST + "/api/whoami")
      .then((response) => {
        setUser(response.data.user);
        setIsAdmin(response.data.is_admin);
      })
      .catch((error) => {
        console.error("whoami failed:", error);
      });
  }, []);

  return (
    <header className="App-header" style={styles.header}>
      <div style={styles.brand}>Dashboard</div>
      <div style={styles.links}>
        <a href="/" style={styles.link}>
          Home
        </a>
        <Link to="/indexInfo" style={styles.link}>
          IndexInfo
        </Link>
      </div>
      <div style={styles.user}>
        {user ? (
          <>
            <span>
              {isAdmin ? <span style={styles.admin}>(admin) </span> : null}
              {user}
            </span>
            <a href="/logout" style={styles.link}>
              Logout
            </a>
          </>
        ) : null}
      </div>
    </header>
  );
}
