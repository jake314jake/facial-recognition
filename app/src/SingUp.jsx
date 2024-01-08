import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import Box from '@mui/material/Box';
import axios from 'axios';

const SignUp = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    gender: '',
    dateOfBirth: '',
    profilePicture: null,
  });

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const handleFileChange = (event) => {
    setFormData({
      ...formData,
      profilePicture: event.target.files[0],
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const formDataToSend = new FormData();
    formDataToSend.append('first_name', formData.firstName);
    formDataToSend.append('last_name', formData.lastName);
    formDataToSend.append('gender', formData.gender);
    formDataToSend.append('date_of_birth', formData.dateOfBirth);
    formDataToSend.append('profile_picture', formData.profilePicture);

    axios({
      method: 'post',
      url: ' http://127.0.0.1:8000/add_user/', 
      data: formDataToSend,
      headers: { 'Content-Type': 'multipart/form-data' },
    })
      .then((response) => {
        console.log(response.data);
        // Handle success, e.g., show a success message to the user
      })
      .catch((error) => {
        console.error('Error submitting form:', error);
        // Handle errors, e.g., show an error message to the user
      });
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="First Name"
            variant="outlined"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="Last Name"
            variant="outlined"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
        </Grid>
        <Grid item xs={6}>
          <FormControl fullWidth variant="outlined" required>
            <InputLabel id="gender-label">Gender</InputLabel>
            <Select
              labelId="gender-label"
              id="gender"
              value={formData.gender}
              label="Gender"
              name="gender"
              onChange={handleChange}
            >
              <MenuItem value="Male">Male</MenuItem>
              <MenuItem value="Female">Female</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="Date of Birth"
            type="date"
            variant="outlined"
            InputLabelProps={{
              shrink: true,
            }}
            name="dateOfBirth"
            value={formData.dateOfBirth}
            onChange={handleChange}
            required
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            type="file"
            label="Profile Picture"
            variant="outlined"
            onChange={handleFileChange}
          />
        </Grid>
        <Grid item xs={12}>
          <Box mt={2}>
            <Button type="submit" variant="contained" color="primary">
              Sign Up
            </Button>
          </Box>
        </Grid>
      </Grid>
    </form>
  );
};

export default SignUp;
