// App.js
import React from 'react';
import Sidebar from './components/SideBar';
import ChatInterface from './components/ChatInterface';

const App = () => {
  return (
    <div className="flex h-screen bg-gray-50 font-sans">
      <Sidebar />
      <ChatInterface />
    </div>
  );
};

export default App;