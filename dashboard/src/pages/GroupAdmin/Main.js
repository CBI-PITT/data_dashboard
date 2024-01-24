// GroupUserMain.js
import React, { useState } from 'react';
import Sidebar from './Sidebar';
import TableList from './TableList';
import { Box } from '@mui/material';

const GroupUserMain = () => {
  const [selectedOption, setSelectedOption] = useState('user');

  const handleSelect = (option) => {
    setSelectedOption(option);
  };

  return (
    <Box display="flex" >
      <Sidebar onSelect={handleSelect} />
      <Box flexGrow={1} >
        <TableList selectedOption={selectedOption} />
      </Box>
    </Box>
  );
};

export default GroupUserMain;
