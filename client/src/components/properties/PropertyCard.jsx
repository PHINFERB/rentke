import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getProperties } from '../../services/propertyService';
import PropertyCard from './PropertyCard';

const PropertyList = () => {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchParams, setSearchParams] = useState({
    city: '',
    min_price: '',
    max_price: '',
    property_type: ''
  });

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        // Convert empty strings to undefined to avoid sending empty params
        const params = Object.fromEntries(
          Object.entries(searchParams).filter(([_, v]) => v !== '')
        );
        const data = await getProperties(params);
        setProperties(data.results || data); // Handle both paginated and non-paginated responses
      } catch (err) {
        setError(err.message || 'Failed to fetch properties');
      } finally {
        setLoading(false);
      }
    };
    fetchProperties();
  }, [searchParams]);

  const handleSearchChange = (e) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };

  if (loading) return (
    <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
  );

  if (error) return (
    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
      {error}
    </div>
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6 bg-white p-4 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Search Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
            <input
              type="text"
              name="city"
              value={searchParams.city}
              onChange={handleSearchChange}
              className="w-full p-2 border rounded"
              placeholder="Nairobi, Mombasa..."
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Min Price</label>
            <input
              type="number"
              name="min_price"
              value={searchParams.min_price}
              onChange={handleSearchChange}
              className="w-full p-2 border rounded"
              placeholder="KSh min"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Max Price</label>
            <input
              type="number"
              name="max_price"
              value={searchParams.max_price}
              onChange={handleSearchChange}
              className="w-full p-2 border rounded"
              placeholder="KSh max"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
            <select
              name="property_type"
              value={searchParams.property_type}
              onChange={handleSearchChange}
              className="w-full p-2 border rounded"
            >
              <option value="">All Types</option>
              <option value="apartment">Apartment</option>
              <option value="house">House</option>
              <option value="studio">Studio</option>
              <option value="land">Land</option>
            </select>
          </div>
        </div>
      </div>

      {properties.length === 0 ? (
        <div className="text-center py-12">
          <h3 className="text-lg font-medium text-gray-600">No properties found</h3>
          <p className="text-gray-500">Try adjusting your search filters</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {properties.map((property) => (
            <PropertyCard key={property.id} property={property} />
          ))}
        </div>
      )}
    </div>
  );
};

export default PropertyList;