import React, { useState, useEffect } from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';

const Users = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    
    fetch('http://127.0.0.1:8000/get_users_with_logs/')
      .then(response => response.json())
      .then(data => setUsers(data.users))
      .catch(error => console.error('Error fetching users:', error));
  }, []);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Gender</TableCell>
            <TableCell>Date of Birth</TableCell>
            <TableCell>Active</TableCell>
            {/* Add more table headers as needed */}
          </TableRow>
        </TableHead>
        <TableBody>
          {users.length > 0 ? (
            users.map(user => (
              <TableRow key={user.UserID}>
                <TableCell>{`${user.FirstName} ${user.LastName}`}</TableCell>
                <TableCell>{user.Gender}</TableCell>
                <TableCell>{user.DateOfBirth}</TableCell>
                <TableCell>{user.IsActive ? 'Yes' : 'No'}</TableCell>
                {/* Add more table cells as needed */}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={4} align="center">
                No users for this project yet
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Users;
