import React, { useEffect, useState } from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <PropertyList />
      </header>
    </div>
  );
}

function PropertyList() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Use the CORRECT endpoint
        const response = await fetch('http://localhost:8000/rentke/listings/');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        // The data comes in {message, listings, count} format
        setProperties(data.listings || []);
        
      } catch (error) {
        console.error("Fetch error:", error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData(); // Call the correct function name
  }, []);

  if (loading) return <div>Loading properties...</div>;
  if (error) return <div>Error loading properties: {error}</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>Available Properties</h1>
      
      {properties.length > 0 ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '20px' }}>
          {properties.map(property => (
            <div key={property.id} style={{ 
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '20px',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
              transition: 'transform 0.2s',
              ':hover': {
                transform: 'translateY(-5px)',
                boxShadow: '0 4px 8px rgba(0,0,0,0.15)'
              }
            }}>
              <h2 style={{ marginTop: 0 }}>{property.title}</h2>
              
              {/* Image display - using image_url from serializer */}
              {property.main_image && (
                <img 
                  src={property.main_image} 
                  alt={property.title}
                  style={{
                    width: '100%',
                    height: '200px',
                    objectFit: 'cover',
                    border: '1px solid red',
                    borderRadius: '4px',
                    margin: '10px 0'
                  }}
                   onError={(e) => {
                    console.error('Image failed to load:', property.main_image);
                    e.target.style.display = 'none';
                  }}
                />
              )}
              
              {/* Property details */}
              <div style={{ marginTop: '15px' }}>
                <div style={{ fontSize: '12px', color: '#666' }}>
                  Image URL: {property.main_image}
                </div>
                <p><strong>Price:</strong> KSh {property.price?.toLocaleString()}</p>
                <p><strong>Address:</strong> {property.address || 'Not specified'}</p>
                {property.city && <p><strong>City:</strong> {property.city}</p>}
                <p>
                  <strong>Type:</strong> {property.property_type?.charAt(0).toUpperCase() + property.property_type?.slice(1)}
                </p>
                <p><strong>Bedrooms:</strong> {property.bedrooms}</p>
                <p><strong>Bathrooms:</strong> {property.bathrooms}</p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        !loading && <p style={{ textAlign: 'center' }}>No properties available at the moment.</p>
      )}
    </div>
  );
}

export default App;