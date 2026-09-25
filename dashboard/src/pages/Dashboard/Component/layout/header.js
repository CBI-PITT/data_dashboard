import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import HOST from "../../../../config/path";

const styles = {
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: "12px",
    padding: "8px 16px",
  },
  brand: { fontWeight: 600, margin: 0 },
  links: { display: "flex", alignItems: "center", gap: "12px" },
  link: { color: "inherit", textDecoration: "none" },
  user: {
    display: "flex",
    alignItems: "center",
    gap: "6px",
    fontWeight: 500,
  },
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
              {isAdmin ? "(admin) " : ""}
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
