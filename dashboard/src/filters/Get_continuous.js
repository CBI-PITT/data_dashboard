import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import { useState } from 'react';
import Typography from '@mui/material/Typography';
import * as React from 'react';




function GetConti({ key_Continuous, value_Continuous, formData }) {
    // const key = ["Treatment", "Time_Point"]
    // const value = [["eeve", "weev", "vvev"], [24, 48, 72, 96]]
    // const [valueSlider,setValueSlider] = useState([])

    // const onChangeValue = (event,newValue) =>{
    //     setValueSlider(newValue)
    // }
    // const [contiSelected,setContiSelected] = useState(() => {
    //     const initialMap = new Map();
    //     for (let i = 0; i < key_Continuous.length; i++) {
    //         initialMap.set(key_Continuous[i], [value_Continuous[i].min, value_Continuous[i].max])
    //     }
    //     return initialMap;
    //   });
    // console.log("contiselected", contiSelected)

    const [contiSelected,setContiSelected] = useState(new Map())
    formData.filter.continuous = Object.fromEntries(contiSelected)
    // if(key_Continuous.length!=0)
    // {
    //     const firstMap = new Map()
    //     for (let i = 0; i < key_Continuous.length; i++) {
    //         firstMap.set(key_Continuous[i], [value_Continuous[i].min, value_Continuous[i].max])
    //     }
    //     setContiSelected(firstMap)
    // }
    // for (let i = 0; i < key_Continuous.length; i++) {
    //     contiSelected.set(key_Continuous[i], [value_Continuous[i].min, value_Continuous[i].max])
    // }
    // formData.filter.continuous = Object.fromEntries(contiSelected)
    // console.log(formData.filter.continuous)
    // console.log(contiSelected)
    const handleChange = (event) => {
        contiSelected.set(event.target.name, event.target.value)

        const newMap = new Map(contiSelected);
        newMap.set(event.target.name, event.target.value);
        setContiSelected(newMap);
        
    }


    if (key_Continuous !== undefined && value_Continuous !== undefined) {
        
        return (
            // <div>
            //     {
            //         key.map((k, ind) => (
            //             <div>
            //                 <h2>{k}</h2>
            //                 {/* {value[ind].map((v) => (
            //                     <label>
            //                         <input type="checkbox" />
            //                         {v}
            //                     </label>
            //                 ))} */}
            //                 <span>Min: {value[ind].min}</span>
            //                 <span>Max: {value[ind].max}</span>
            //             </div>
            //         ))
            //     }
            // </div>
            <div>
                <center>

                    {key_Continuous.map((k, ind) => (

                        <div key={k}>

                            <br></br>

                            <Typography gutterBottom>
                                {k}
                            </Typography>
                            <div className='eachContinuousVar'>
                                {/* <div className='min'>{value[ind].min}</div> */}

                                <Box className='slider'>


                                    <Slider id={k} min={value_Continuous[ind].min} max={value_Continuous[ind].max} name={k} defaultValue={[value_Continuous[ind].min, value_Continuous[ind].max]} onChange={handleChange} key={k}
                                        valueLabelDisplay="auto" size='small' marks={[{ value: value_Continuous[ind].min, label: value_Continuous[ind].min }, { value: value_Continuous[ind].max, label: value_Continuous[ind].max }]}></Slider>
                                    {/* <Slider id={k} min={value[ind].min} max={value[ind].max} name={k} defaultValue={[value[ind].min, value[ind].max]}
                                        valueLabelDisplay="auto" size='small' ></Slider> */}
                                </Box>
                                {/* <div className='max'>{value[ind].max}</div> */}

                            </div>

                        </div>
                    ))}


                </center>
            </div>
        )
    }
}

export default GetConti;