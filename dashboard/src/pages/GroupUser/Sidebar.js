// Sidebar.js
import React from 'react';
import { List, ListItem, ListItemIcon, ListItemText, Paper } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import InsertChartIcon from '@mui/icons-material/InsertChart';
import WorkIcon from '@mui/icons-material/Work';

const sidebarStyle = {
  width: '250px',
  backgroundColor: '#f5f5f5',
  height: '100vh',
  padding: '20px',
};

const listItemStyle = {
  marginBottom: '10px',
  borderRadius: '5px',
  cursor: 'pointer',
  transition: 'background-color 0.3s',
};

const iconStyle = {
  marginRight: '10px',
};

const Sidebar = ({ onSelect }) => {
  const handleSelect = (option) => {
    onSelect(option);
  };

  return (
    <Paper elevation={3} style={sidebarStyle}>
      <List component="nav">
        <ListItem button style={listItemStyle} onClick={() => handleSelect('user')}>
          <ListItemIcon style={iconStyle}>
            <AccountCircleIcon />
          </ListItemIcon>
          <ListItemText primary="User Name" />
        </ListItem>
        <ListItem button style={listItemStyle} onClick={() => handleSelect('mydata')}>
          <ListItemIcon style={iconStyle}>
            <InsertChartIcon />
          </ListItemIcon>
          <ListItemText primary="My Data" />
        </ListItem>
        <ListItem button style={listItemStyle} onClick={() => handleSelect('myjob')}>
          <ListItemIcon style={iconStyle}>
            <WorkIcon />
          </ListItemIcon>
          <ListItemText primary="My Jobs" />
        </ListItem>
      </List>
    </Paper>
  );
};

export default Sidebar;
