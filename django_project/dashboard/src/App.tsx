import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { store } from './app/store';
import './styles/index.scss';
import Dashboard from './views/Dashboard';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('app')!)
root.render(
    <Provider store={store}>
        <Dashboard />
    </Provider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
