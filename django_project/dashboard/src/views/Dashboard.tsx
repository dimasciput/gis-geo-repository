import React from 'react';
import '../styles/App.scss';
import NavBar from "../components/NavBar";
import SideNavigation from "../components/SideNavigation";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  matchPath, useLocation
} from "react-router-dom";
import {routes} from "./routes";


function Dashboard() {
  return (
    <div className="App">
      <NavBar/>
      <main>
        <Router>
          <SideNavigation/>
          <div className='AdminContent'>
            <Header/>
            <Routes>
              {routes.map((route, key) => (
                <Route key={key} path={route.path} element={<route.element/>}/>
              ))}
            </Routes>
          </div>
        </Router>
      </main>
    </div>
  );
}

function useMatchedRoute() {
  const { pathname } = useLocation();
  for (const route of routes) {
    if (matchPath({ path: route.path }, pathname)) {
      return route;
    }
  }
}

export function Header() {
  const route = useMatchedRoute();
  return (
    <div className='AdminContentHeader'>
      <div className='AdminContentHeader-Left'>
        <b className='light'>{ route ? route.name : '' }</b>
      </div>
    </div>
  )
}

export function Home() {
  return (
    <div>
      <h2>Home</h2>
    </div>
  )
}

export default Dashboard;
