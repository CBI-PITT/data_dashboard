import { createTheme } from "@mui/material/styles";
import { peaceTokens } from "./tokens";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: peaceTokens.accent },
    background: { default: peaceTokens.bg, paper: peaceTokens.surface },
    text: { primary: peaceTokens.ink, secondary: peaceTokens.muted },
  },
  shape: { borderRadius: 10 },
  typography: {
    fontFamily: peaceTokens.font,
    button: { fontWeight: 500, textTransform: "none" },
  },
  components: {
    MuiButton: {
      defaultProps: { disableElevation: true },
    },
    MuiChip: {
      styleOverrides: { root: { fontWeight: 500 } },
    },
    MuiTooltip: {
      defaultProps: { arrow: true },
    },
  },
});

export default theme;

// Shared filled-alert style (accent blue, white text) used by the dataset
// picker placeholder alerts and the central cover alert so they stay
// identical by construction.
export const accentAlertSx = {
  borderRadius: "10px",
  backgroundColor: "var(--peace-accent)",
  color: "#ffffff",
  fontWeight: 500,
  fontSize: "1rem",
};
