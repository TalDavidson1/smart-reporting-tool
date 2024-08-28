import React from 'react';
import ReactDOM from 'react-dom/client';
import SmartReportingApp from './App';
import { ChakraProvider } from '@chakra-ui/react';

// Export SmartReportingApp, ReactDOM, React, and ChakraProvider to the window object for use in test-embed.html
window.SmartReportingTool = {
  App: SmartReportingApp,
  ReactDOM: ReactDOM,
  React: React,
  ChakraProvider: ChakraProvider
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ChakraProvider>
      <SmartReportingApp />
    </ChakraProvider>
  </React.StrictMode>
);
