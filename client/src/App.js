import React, { useEffect, useState } from 'react';

function App() {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/properties/');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('API Response:', data);
        
        // Extract listings from the paginated response
        const receivedListings = data.results || [];
        
        setListings(receivedListings);
      } catch (error) {
        console.error('Fetch error:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchListings();
  }, []);

  if (loading) return <div>Loading listings...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="App">
      <h1>PROPERTIES</h1>
      {listings.length > 0 ? (
        <div className="listings-container">
          {listings.map(listing => (
            <div key={listing.id} className="listing-card">
              <h2>{listing.title}</h2>
              {listing.main_image && (
                <img 
                  src={listing.main_image} 
                  alt={listing.title}
                  style={{ maxWidth: '100%', height: 'auto' }}
                />
              )}
              <p>Price: KSh {listing.price}</p>
              <p>Location: {listing.city}</p>
              <p>Type: {listing.property_type}</p>
              <p>Bedrooms: {listing.bedrooms}</p>
              <p>Bathrooms: {listing.bathrooms}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-listings">
          <p>No listings found in our system</p>
        </div>
      )}
    </div>
  );
}

export default App;