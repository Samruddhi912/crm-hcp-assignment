import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { store } from './store.js';
import App from './App.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* This Provider wrapper is what your app was missing! */}
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);