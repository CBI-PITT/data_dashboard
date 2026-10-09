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
