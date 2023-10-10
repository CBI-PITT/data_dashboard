
import Box from '@mui/material/Box';
import barImg from '../asset/Bar.png'
import boxImg from '../asset/Box.png'
import dotImg from '../asset/Scatter.png'
import pieImg from '../asset/Pie.png'
import lineImg from '../asset/Line.png'
import areaImg from '../asset/Area.png'
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
function plotChoice({ setPlotChoice, field_status }) {
    // console.log(field_status)

    const buttons = [
        <Button key="bar" onClick={() => { setPlotChoice("bar") }} ><img src={barImg} className="plotButton"></img></Button>,
        <Button key="box" onClick={() => { setPlotChoice("box") }} disabled={field_status=='keyword'?true:false}><img src={boxImg} className="plotButton"></img></Button>,
        <Button key="dot" onClick={() => { setPlotChoice("circle packing") }}><img src={dotImg} className="plotButton"></img></Button>,
        <Button key="pie" onClick={() => { setPlotChoice("pie") }} ><img src={pieImg} className="plotButton"></img></Button>,
        <Button key="line" onClick={() => { setPlotChoice("line") }}><img src={lineImg} className="plotButton"></img></Button>,
        <Button key="area" onClick={() => { setPlotChoice("area") }}><img src={areaImg} className="plotButton"></img></Button>
    ];
    return (
        <Box
            sx={{
                display: 'flex',
                '& > *': {
                    m: 1,
                },
            }}
        >
            <ButtonGroup
                orientation="vertical"
                aria-label="vertical contained button group"
                variant='contained'
                color="inherit"
            >
                {buttons}
            </ButtonGroup>

        </Box>
    );
}

export default plotChoice;