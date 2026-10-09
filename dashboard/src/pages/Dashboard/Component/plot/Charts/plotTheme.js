import { peaceTokens } from "../../../../../config/tokens";

// Shared Plotly layout: transparent backgrounds so the card surfaces show
// through, PEACE font stack, soft gridlines, tidy margins. Per-chart layout
// values passed via `extra` win over these defaults.
export function plotLayout(extra = {}) {
  const { xaxis = {}, yaxis = {}, ...rest } = extra;
  return {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { family: peaceTokens.font, size: 14, color: peaceTokens.ink },
    margin: { l: 70, r: 30, t: 40, b: 60 },
    xaxis: {
      gridcolor: "rgba(100, 116, 139, .15)",
      zerolinecolor: "rgba(100, 116, 139, .25)",
      automargin: true,
      ...xaxis,
    },
    yaxis: {
      gridcolor: "rgba(100, 116, 139, .15)",
      zerolinecolor: "rgba(100, 116, 139, .25)",
      automargin: true,
      ...yaxis,
    },
    ...rest,
  };
}
