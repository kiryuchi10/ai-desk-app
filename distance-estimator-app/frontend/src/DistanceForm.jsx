// DistanceForm.jsx
import React, { useState } from 'react';
import axios from 'axios';

function DistanceForm({ onResult }) {
  const [form, setForm] = useState({
    objectWidth: '',
    fingerWidth: '',
    armLength: '',
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await axios.post('http://localhost:5000/api/distance', form);
    onResult(res.data.distance);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="objectWidth" placeholder="Object Width (m)" onChange={handleChange} />
      <input name="fingerWidth" placeholder="Finger Width (m)" onChange={handleChange} />
      <input name="armLength" placeholder="Arm Length (m)" onChange={handleChange} />
      <button type="submit">Estimate</button>
    </form>
  );
}

export default DistanceForm;
