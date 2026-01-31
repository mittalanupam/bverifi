import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [connected, setConnected] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [formData, setFormData] = useState({ title: '', description: '' });

  // Check API health
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await axios.get(`${API_URL}/health/`);
        setConnected(true);
      } catch (err) {
        setConnected(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Fetch items
  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/items/`);
      setItems(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch items. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await axios.patch(`${API_URL}/items/${editingItem.id}/`, formData);
      } else {
        await axios.post(`${API_URL}/items/`, formData);
      }
      setShowModal(false);
      setEditingItem(null);
      setFormData({ title: '', description: '' });
      fetchItems();
    } catch (err) {
      setError('Failed to save item.');
    }
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setFormData({ title: item.title, description: item.description });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      try {
        await axios.delete(`${API_URL}/items/${id}/`);
        fetchItems();
      } catch (err) {
        setError('Failed to delete item.');
      }
    }
  };

  const toggleComplete = async (item) => {
    try {
      await axios.patch(`${API_URL}/items/${item.id}/`, {
        completed: !item.completed
      });
      fetchItems();
    } catch (err) {
      setError('Failed to update item.');
    }
  };

  const openNewItemModal = () => {
    setEditingItem(null);
    setFormData({ title: '', description: '' });
    setShowModal(true);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">A</div>
            <h1>Ankur</h1>
          </div>
          <div className={`status-badge ${connected ? 'connected' : ''}`}>
            <span className="status-dot"></span>
            {connected ? 'API Connected' : 'Connecting...'}
          </div>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <h2>Full Stack Application</h2>
          <p>
            Django REST Framework backend with React frontend, 
            powered by PostgreSQL and containerized with Docker.
          </p>
        </section>

        <div className="cards-grid">
          <div className="card">
            <div className="card-icon">🐍</div>
            <h3>Django Backend</h3>
            <p>
              RESTful API built with Django REST Framework. 
              Handles authentication, data validation, and database operations.
            </p>
          </div>
          <div className="card">
            <div className="card-icon">⚛️</div>
            <h3>React Frontend</h3>
            <p>
              Modern React application with hooks and functional components. 
              Responsive design with smooth animations.
            </p>
          </div>
          <div className="card">
            <div className="card-icon">🐘</div>
            <h3>PostgreSQL</h3>
            <p>
              Robust PostgreSQL database for reliable data persistence. 
              Fully containerized for easy deployment.
            </p>
          </div>
        </div>

        <section className="items-section">
          <div className="section-header">
            <h3>Items</h3>
            <button className="btn btn-primary" onClick={openNewItemModal}>
              + Add Item
            </button>
          </div>

          {error && <div className="error">{error}</div>}

          <div className="items-container">
            {loading ? (
              <div className="loading">
                <div className="spinner"></div>
              </div>
            ) : items.length === 0 ? (
              <div className="items-empty">
                <div className="items-empty-icon">📝</div>
                <p>No items yet. Create your first item!</p>
              </div>
            ) : (
              items.map((item) => (
                <div key={item.id} className={`item ${item.completed ? 'completed' : ''}`}>
                  <div
                    className={`item-checkbox ${item.completed ? 'checked' : ''}`}
                    onClick={() => toggleComplete(item)}
                  />
                  <div className="item-content">
                    <div className="item-title">{item.title}</div>
                    {item.description && (
                      <div className="item-description">{item.description}</div>
                    )}
                  </div>
                  <div className="item-actions">
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => handleEdit(item)}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDelete(item.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>
      </main>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>{editingItem ? 'Edit Item' : 'New Item'}</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="title">Title</label>
                <input
                  type="text"
                  id="title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Enter item title..."
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="description">Description (optional)</label>
                <textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Enter item description..."
                />
              </div>
              <div className="modal-actions">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingItem ? 'Save Changes' : 'Create Item'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

