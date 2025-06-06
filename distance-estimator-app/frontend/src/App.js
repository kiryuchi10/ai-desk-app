// App.jsx
import React, { useState } from 'react';
import DistanceForm from './DistanceForm';

function App() {
  const [distance, setDistance] = useState(null);

  return (
    <div>
      <h1>📏 거리 추정기</h1>
      <DistanceForm onResult={setDistance} />
      {distance && <h2>추정 거리: {distance} m</h2>}
    </div>
  );
}

export default App;
