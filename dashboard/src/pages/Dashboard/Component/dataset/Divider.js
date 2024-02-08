import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import SnippetFolderIcon from '@mui/icons-material/SnippetFolder';
import AssignmentIcon from '@mui/icons-material/Assignment';
import StorageIcon from '@mui/icons-material/Storage';
import Divider from '@mui/material/Divider';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import Skeleton from '@mui/material/Skeleton';
import Grid from '@mui/material/Grid';
const wave_animation = (value) => {
    return value === 'Retrieving' ? <Skeleton animation='wave'></Skeleton> : value
}


export default function Dividers({ index_status }) {
    return (
        <Grid container spacing={0}>
          {/* <Grid item xs={12} md={12} lg={4}>
            <List sx={{  bgcolor: 'rgb(245, 246, 246)' }}>
              <ListItem>
                <ListItemAvatar>
                  <Avatar>
                    <HealthAndSafetyIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText primary="Health" secondary={wave_animation(index_status['health'])} />
              </ListItem>
            </List>
          </Grid> */}
    
          <Grid item xs={12} sm={12} md={12} lg={12} xl={6}>
            <List sx={{  bgcolor: 'rgb(245, 246, 246)' }}>
              <ListItem>
                <ListItemAvatar>
                  <Avatar>
                    <StorageIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText primary="Storage" secondary={wave_animation(index_status['storageSize'])} />
              </ListItem>
            </List>
          </Grid>
    
          <Grid  item xs={12} sm={12} md={12} lg={12} xl={6}>
            <List sx={{  bgcolor: 'rgb(245, 246, 246)' }}>
              <ListItem>
                <ListItemAvatar>
                  <Avatar>
                    <SnippetFolderIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText primary="Document" secondary={wave_animation(index_status['docCount'])} />
              </ListItem>
            </List>
          </Grid>
        </Grid>
      );
}
