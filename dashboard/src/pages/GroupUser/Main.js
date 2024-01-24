// GroupUserMain.js
import React, { useState } from 'react';
import Sidebar from './Sidebar';
import TableList from './TableList';
import { Box } from '@mui/material';

const GroupUserAdmin = () => {
  const [selectedOption, setSelectedOption] = useState('user');

  const handleSelect = (option) => {
    setSelectedOption(option);
  };

  return (
    <Box display="flex" height="100vh">
      <Sidebar onSelect={handleSelect} />
      <Box flexGrow={1} height="100%">
        <TableList selectedOption={selectedOption} />
      </Box>
    </Box>
  );
};

export default GroupUserAdmin;
