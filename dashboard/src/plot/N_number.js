import React from "react"
import Typography from '@mui/material/Typography';

export default function N_number({N}){
    return (
          <Typography sx={{ fontSize: 16 ,float:'right'}} color="unset">
            N = {N}
          </Typography>
          )
    return (<h4 style={{fontFamily:'initial', display:'flex'}}>N = {N}</h4>)
}