import React from "react";
import Typography from "@mui/material/Typography";

export default function N_number({ N }) {
  return (
    <Typography
      sx={{
        fontSize: 14,
        fontWeight: 600,
        color: "var(--peace-ink)",
        backgroundColor: "var(--peace-accent-soft)",
        border: "1px solid var(--peace-border)",
        borderRadius: 999,
        px: 1.5,
        py: 0.25,
        whiteSpace: "nowrap",
      }}
    >
      N = {N}
    </Typography>
  );
}
