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

const wave_animation = (value) => {
    return value === 'Retrieving' ? <Skeleton animation='wave'></Skeleton> : value
}


export default function Dividers({ index_status }) {
    return (
        <div className='divider'>
            <List
                sx={{
                    width: '33.3%',
                    // height:'40%',
                    bgcolor: 'rgb(245, 246, 246)',
                }}
            >
                <ListItem >
                    <ListItemAvatar>
                        <Avatar>
                            <HealthAndSafetyIcon />
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText primary="Health" secondary={wave_animation(index_status['health'])} />
                </ListItem>
                {/* <Divider variant='middle' component="li" /> */}
                {/* <ListItem x={
                   {height : '40%'}
                }>
                    <ListItemAvatar>
                        <Avatar>
                            <StorageIcon />
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText primary="Storage" secondary={wave_animation(index_status['storageSize'])} />
                </ListItem> */}

            </List>
            <List sx={{
                width: '33.3%',
                // height:'20%',
                bgcolor: 'rgb(245, 246, 246)',
            }}>
                <ListItem >
                    <ListItemAvatar>
                        <Avatar>
                            <StorageIcon />
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText primary="Storage" secondary={wave_animation(index_status['storageSize'])} />
                </ListItem>
            </List>
            {/* <List
                sx={{
                    width: '25%',
                    // height:'20%',
                    bgcolor: 'rgb(245, 246, 246)',
                }}
            >
                <ListItem>
                    <ListItemAvatar>
                        <Avatar>
                            <AssignmentIcon />
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText primary="Status" secondary={wave_animation(index_status['status'])} />
                </ListItem>
                <Divider variant='middle' component="li" />
                </List> */}
            <List sx={{
                width: '33.3%',
                // height:'20%',
                bgcolor: 'rgb(245, 246, 246)',
            }}>
                <ListItem>
                    <ListItemAvatar>
                        <Avatar>
                            <SnippetFolderIcon />
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText primary="Document" secondary={wave_animation(index_status['docCount'])} />
                </ListItem>

            </List>
        </div>
    );
}
