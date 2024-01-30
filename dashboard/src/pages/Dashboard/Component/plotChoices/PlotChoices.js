
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import stackBarImg from '../asset/StackBar.png'
import groupBarImg from '../asset/GroupBar.png'
import boxImg from '../asset/Box.png'
import dotImg from '../asset/Scatter.png'
import pieImg from '../asset/Pie.png'
import lineImg from '../asset/Line.png'
import areaImg from '../asset/Area.png'
import cloudImg from '../asset/Cloud.png'
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import multi_layer from '../asset/Multi_layer.png';
import IconButton from '@mui/material/IconButton';
function plotChoice({ setPlotChoice, field_status,groupBy }) {
    // console.log(field_status)

    const buttons = [
        <Button key="stack_bar" onClick={() => { setPlotChoice("stack_bar") }} ><img src={stackBarImg} className="plotButton"></img></Button>,
        <Button key="stack_bar_pl" onClick={() => { setPlotChoice("stack_bar_pl") }} ><img src={stackBarImg} className="plotButton"></img></Button>,
        <Button key="bar" onClick={() => { setPlotChoice("group_bar") }}  disabled={groupBy.length !== 2 && groupBy.length !== 0}><img src={groupBarImg} className="plotButton"></img></Button>,
        <Button key="group_bar_pl" onClick={() => { setPlotChoice("group_bar_pl") }}  disabled={groupBy.length !== 2 && groupBy.length !== 0}><img src={groupBarImg} className="plotButton"></img></Button>,
        <Button key="box" onClick={() => { setPlotChoice("box") }} disabled={field_status==='keyword'?true:false}><img src={boxImg} className="plotButton" ></img></Button>,
        <Button key="pie" onClick={() => { setPlotChoice("pie") }} ><img src={pieImg} className="plotButton" ></img></Button>,
        <Button key="dot" onClick={() => { setPlotChoice("circle packing") }}><img src={dotImg} className="plotButton"></img></Button>,
        <Button key="cloud" onClick={() => { setPlotChoice("cloud") }} ><img src={cloudImg} className="plotButton"></img></Button>,
        // <Button key="line" onClick={() => { setPlotChoice("line") }}><img src={lineImg} className="plotButton"></img></Button>,
        <Button key="line" onClick={() => { setPlotChoice("line_pl") }}><img src={lineImg} className="plotButton"></img></Button>,
        // <Button key="area" onClick={() => { setPlotChoice("area") }}><img src={areaImg} className="plotButton"></img></Button>,
        <Button key="area" onClick={() => { setPlotChoice("area_pl") }}><img src={areaImg} className="plotButton"></img></Button>,
        // <Button key="multi-layer" onClick={() => { setPlotChoice("facet") }}><img src={multi_layer} className="plotButton"></img></Button> 
    ];
    return (
        <Grid container spacing={2} alignItems="center" justifyContent="center">
      <Grid item xs={12} md={11}>
            <ButtonGroup
                orientation="vertical"
                aria-label="vertical contained button group"
                variant='contained'
                color="inherit"
            >
                {buttons}
            </ButtonGroup>

            </Grid>
    </Grid>
    );
}

export default plotChoice;

