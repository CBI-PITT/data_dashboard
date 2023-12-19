import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';

import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import OutlinedInput from '@mui/material/OutlinedInput';
import ListItemText from '@mui/material/ListItemText';
import Checkbox from '@mui/material/Checkbox';
import { useEffect } from 'react';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
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
// function GetAggregation({ list, form_Data, set_FormData, field_status }) {
//     const [aggregationSelected, setAggregationSelected] = useState([])
//     // console.log(field_status)
//     // if(field_status === 'keyword')
//     // {
//     //     setAggregationSelected([])
//     // }
//     useEffect(() => {
//         if (field_status === 'keyword') {
//           setAggregationSelected([]);
//         }
//       }, [field_status]);
//     const handleChange = (event) => {
//         // console.log(event.target.value)
//         setAggregationSelected(event.target.value)
//         // let newFormData = form_Data
//         // newFormData.aggregate = event.target.value

//         const updatedFormData = { ...form_Data }
//         updatedFormData.aggregate = event.target.value
//         set_FormData(updatedFormData)
//         // formData.aggregate = event.target.value

//     };
//     // console.log(list)
//     if (list !== undefined) {

//         return (
//             // <div>
//             //     {
//             //         list.map((item) => (
//             //             <span>
//             //                 {item} /
//             //             </span>
//             //         ))
//             //     }
//             // </div>
//             // <label for="aggregation">Aggregation:
//             //     <select id='aggregation' name="aggregate" >
//             //         {
//             //             list.map((item) => (
//             //                 <option value={item}>{item}</option>
//             //             ))
//             //         }
//             //     </select>
//             // </label>
//             // <FormControl required sx={{ m: 1, minWidth: 120 }}>
//             //     <InputLabel id="aggregation-required-label">Aggregation</InputLabel>
//             //     <Select
//             //         labelId="aggregation-required-label"
//             //         id="aggregation-required"
//             //         // value=''
//             //         defaultValue={''}
//             //         label="aggregation *"
//             //         name='aggregation'
//             //         onChange={(event) => {
//             //             console.log("component", event.target)
//             //             // formData.aggregate.push(event.target.value)
//             //             formData.aggregate = event.target.value
//             //         }}
//             //     >
//             //         {
//             //             list.map((item) => (
//             //                 <MenuItem value={item} key={item}>{item}</MenuItem>
//             //             ))
//             //         }
//             //     </Select>
//             // </FormControl>
//             <FormControl required sx={{ m: 1, width: '95%' }}>
//                 <InputLabel id="aggregation-multiple-checkbox-label">Aggregation</InputLabel>
//                 <Select
//                     labelId="aggregation-multiple-checkbox-label"
//                     id="aggregation-multiple-checkbox"
//                     multiple
//                     value={aggregationSelected}
//                     onChange={handleChange}
//                     input={<OutlinedInput label="Tag" />}
//                     renderValue={(selected) => {
//                         // console.log("selected",selected)
//                         return selected.join(', ')
//                     }
//                     }
//                     MenuProps={MenuProps}
//                 >
//                     {list.map((name) => (
//                         <MenuItem key={name} value={name} disabled={(name !== 'value_count'&&name!=='cardinality') && field_status === 'keyword' ? true : false}>
//                             <Checkbox checked={aggregationSelected.indexOf(name) > -1} />
//                             <ListItemText primary={name} />
//                         </MenuItem>
//                     ))}
//                 </Select>
//             </FormControl>
//         )
//     }
// }

// export default GetAggregation;
function GetAggregation({ list, form_Data, set_FormData, field_status }) {
    
    // console.log(field_status)
    // if(field_status === 'keyword')
    // {
    //     setAggregationSelected([])
    // }
    useEffect(() => {
        if (field_status === 'keyword') {
            set_FormData((prevFormData) => ({
                ...prevFormData,
                aggregate: [],
            }));
        }
      }, [field_status]);
    const handleChange = (event) => {
        const { name, value } = event.target;
        set_FormData((prevFormData) => ({
            ...prevFormData,
            [name]: value,
        }));
    };
    // console.log(list)
    if (list !== undefined) {

        return (
            
            <FormControl required sx={{ m: 1, width: '95%' }}>
                <InputLabel id="aggregation-multiple-checkbox-label">Aggregation</InputLabel>
                <Select
                    labelId="aggregation-multiple-checkbox-label"
                    id="aggregation-multiple-checkbox"
                    multiple
                    value={form_Data.aggregate}
                    onChange={handleChange}
                    input={<OutlinedInput label="Tag" />}
                    renderValue={(selected) => (
                        selected.map((value) => (
                          <Chip key={value} label={value} />
                        ))
                    )}
                    MenuProps={MenuProps}
                    name='aggregate'
                >
                    {list.map((agg) => (
                        <MenuItem key={agg} value={agg} disabled={( field_status === 'keyword' && agg !== 'value_count'&&agg!=='cardinality')  ? true : false}>
                            <Checkbox checked={form_Data.aggregate.indexOf(agg) > -1} />
                            <ListItemText primary={agg} />
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        )
    }
}

export default GetAggregation;