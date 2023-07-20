
import React, { useEffect, useState } from 'react';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import Select from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';
import Typography from '@mui/material/Typography';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};


function GetCate({ key_category, value_category, form_Data, setFormData, resetSwitch }) {
    // const key = ["Treatment", "Time_Point"]
    // const value = [["eeve", "weev", "vvev"], [24, 48, 72, 96]]
    const [cateSelected, setCateSelected] = useState(() => {
        const initialMap = new Map();
        key_category.forEach(item => {
            initialMap.set(item, []);
        });
        return initialMap;
    });
    // console.log("map", cateSelected)
    // useEffect(()=>{
    //     const resetMap = new Map();
    //     key_category.forEach(item => {
    //         resetMap.set(item, []);
    //     });
    //     setCateSelected(resetMap)
    // },[resetSwitch])
    
    // const updatedFormData = {...form_Data}
    // updatedFormData.filter.categorical = Object.fromEntries(cateSelected)
    // setFormData(updatedFormData)
    form_Data.filter.categorical = Object.fromEntries(cateSelected)


    const handleChange = (event) => {
        console.log(event.target.name, event.target.value)
        const newMap = new Map(cateSelected);
        newMap.set(event.target.name, event.target.value);
        setCateSelected(newMap);
        // cateSelected.set(event.target.name,event.target.value)
        // console.log("map", cateSelected)


        // setContiSelected(event.target.value)
        // formData.filter.categorical = event.target.value
    };

    if (key_category !== undefined && value_category !== undefined) {

        return (

            // current like{"treatment" : ["weev","veev"]}
            // should be packed to "filter": {
            //     "categorical": {"<column_name>": [<value1>, <value2>], "<column_name>": [<value1>, <value2>]},
            //     "continuous": {"<column_name>": [<min>, <max>], "<column_name>": [<min>, <max>]}
            // }
            <div>
                {
                    key_category.map((k, ind) => (
                        <div key={k}>

                            {/* <Typography gutterBottom>
                                {k}
                            </Typography> */}
                            <br></br>
                            <FormControl required sx={{ m: 1, width: '95%' }}>
                                <InputLabel id="demo-multiple-checkbox-label">{k}</InputLabel>
                                <Select
                                    labelId="demo-multiple-checkbox-label"
                                    id="demo-multiple-checkbox"
                                    multiple
                                    defaultValue={[]}
                                    // value={cateSelected.get(k)===undefined?(
                                    //     ()=>{
                                    //         cateSelected.set(k,[])
                                    //         return cateSelected.get(k)
                                    //     }
                                    // ):(cateSelected.get(k))}
                                    onChange={handleChange}
                                    input={<OutlinedInput label="Tag" />}
                                    renderValue={(selected) => selected.join(', ')}
                                    MenuProps={MenuProps}
                                    name={k}
                                >
                                    {value_category[ind].map((name) => (
                                        <MenuItem key={name} value={name} >
                                            {/* <Checkbox checked={groupBySelected.indexOf(name) > -1} /> */}
                                            <ListItemText primary={name} />
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>


                        </div>
                    ))
                }


            </div>
        )
    }
}


// {/* <label for={k}>
//                                 {/* {console.log(k)} */}
//                                 <select id={k} name={k} size={3} multiple>
//                                     {value_category[ind].map((v) => (
//                                         <option value={v}>
//                                             {v}
//                                         </option>
//                                     ))}
//                                 </select>
//                             </label> */}


export default GetCate;