import React, { useEffect, useState } from 'react';

function App() {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/public/', {
      headers: {
        'Content-Type': 'application/json',
        // Add if using authentication:
        // 'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    .then(res => {
      if (!res.ok) throw new Error('Network response was not ok');
      return res.json();
    })
    .then(data => {
      // Handle both array and object responses
      const receivedListings = Array.isArray(data) ? data : data.listings || [];
      setListings(receivedListings);
    })
    .catch(error => {
      console.error('Error:', error);
      setError(error.message);
    })
    .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Listings</h1>
      {listings.length > 0 ? (
        listings.map(listing => (
          <div key={listing.id}>
            <h2>{listing.title}</h2>
            <p>{listing.description || 'No description available'}</p>
          </div>
        ))
      ) : (
        <div>No listings found</div>
      )}
    </div>
  );
}

export default App;