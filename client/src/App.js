import React, { useEffect, useState } from 'react';

function App() {
  const [listings, setListings] = useState([]); // State to store fetched data
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    fetch('http://localhost:8000/api/listings/')  // Django API endpoint
      .then(res => {
        if (!res.ok) {
          throw new Error('Network response was not ok');
        }
        return res.json();
      })
      .then(data => {
        const listingsArry = Array.isArray(data) ? data : data.listings || [];
        setListings(data.listings || []);
        setError(null);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setError(error.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []); // Empty dependency array = runs once on mount

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!listings.length) return <div>No listings found</div>;

  return (
    <div>
      <h1>Listings</h1>
      {listings.map(listing => (
        <div key={listing.id}>
          <h2>{listing.title}</h2>
          <p>{listing.description || 'No description available'}</p>
        </div>
      ))}
    </div>
  );
}

export default App;