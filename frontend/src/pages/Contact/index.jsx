import Menu from "../../components/Menu";
import "./styles.css";
import React, { useState, useEffect } from 'react';

function ContactPage() {
  const [contacts, setContacts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');

    if (!token) {
      console.error('Token not found. User must be logged in to view contacts.');
      setError('Authentication error. Please log in.');
      setIsLoading(false);
      return;
    }

    const headers = new Headers({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    });

    fetch('http://localhost:8000/contacts/', { method: 'GET', headers })
      .then(response => {
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
      return response.json();
    })
      .then(data => {
        setContacts(data);
        setIsLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setIsLoading(false);
      });
  }, []);

  if (isLoading) return <p> Loading contacts...</p>;
  if (error) return <p> {error} </p>;
  return (
    <>
      <Menu activeIndex={2} />

    </>
  );
}

export default ContactPage;
