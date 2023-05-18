import React from 'react';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import Box from '@mui/material/Box';
import barImg from '../asset/bar.png'
import boxImg from '../asset/box.png'
import dotImg from '../asset/dot.png'
import pieImg from '../asset/pie.png'
import lineImg from '../asset/line.png'
import areaImg from '../asset/area.png'

export default function PlotButton() {
    const buttons = [
    
        <Button key="bar"><img src={barImg} className="plotButton"></img></Button>,
        <Button key="box"><img src={boxImg} className="plotButton"></img></Button>,
        <Button key="dot"><img src={dotImg} className="plotButton"></img></Button>,
        <Button key="pie"><img src={pieImg} className="plotButton"></img></Button>,
        <Button key="line"><img src={lineImg} className="plotButton"></img></Button>,
        <Button key="area"><img src={areaImg} className="plotButton"></img></Button>
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
                variant="outlined"
                color='inherit'
            >
                {buttons}
            </ButtonGroup>

        </Box>

    );
}