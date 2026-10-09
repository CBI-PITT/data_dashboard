import stackBarImg from "../asset/StackBar.png";
import groupBarImg from "../asset/GroupBar.png";
import boxImg from "../asset/Box.png";
import dotImg from "../asset/Scatter.png";
import pieImg from "../asset/Pie.png";
import lineImg from "../asset/Line.png";
import areaImg from "../asset/Area.png";
import cloudImg from "../asset/Cloud.png";
import multi_layer from "../asset/Multi_layer.png";
import Button from "@mui/material/Button";
import ButtonGroup from "@mui/material/ButtonGroup";

function plotChoice({ setPlotChoice, plotChoice, field_status, groupBy }) {
  const buttons = [
    { key: "stack_bar_pl", img: stackBarImg, alt: "Stacked bar chart", disabled: false },
    {
      key: "group_bar_pl",
      img: groupBarImg,
      alt: "Grouped bar chart",
      disabled: groupBy.length !== 2 && groupBy.length !== 0,
    },
    { key: "box", img: boxImg, alt: "Box plot", disabled: field_status === "keyword" },
    { key: "pie", img: pieImg, alt: "Pie chart", disabled: false },
    { key: "circle packing", img: dotImg, alt: "Circle packing", disabled: false },
    { key: "cloud", img: cloudImg, alt: "Word cloud", disabled: false },
    { key: "line_pl", img: lineImg, alt: "Line chart", disabled: false },
    { key: "area_pl", img: areaImg, alt: "Area chart", disabled: false },
    { key: "facet", img: multi_layer, alt: "Facet charts", disabled: false },
  ];
  return (
    <ButtonGroup
      orientation="vertical"
      aria-label="vertical plot type selector"
      variant="outlined"
      color="inherit"
      fullWidth
    >
      {buttons.map((item) => {
        const selected = plotChoice === item.key;
        return (
          <Button
            key={item.key}
            onClick={() => setPlotChoice(item.key)}
            disabled={item.disabled}
            aria-pressed={selected}
            sx={
              selected
                ? {
                    borderColor: "var(--peace-accent)",
                    backgroundColor: "var(--peace-accent-soft)",
                    "&:hover": { backgroundColor: "var(--peace-accent-soft)" },
                  }
                : undefined
            }
          >
            <img src={item.img} className="plotButton" alt={item.alt}></img>
          </Button>
        );
      })}
    </ButtonGroup>
  );
}

export default plotChoice;
