import React from 'react';
import { Outlet } from 'react-router-dom';
import Navigation from './common/Navigation';

/**
 * Layout component that wraps the application content with common elements like navigation
 */
const Layout = () => {
  return (
    <div className="app-container">
      <Navigation />
      <main className="container mx-auto p-4">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;