import React from 'react';
import '../styles/App.scss';
import NavBar from "../components/NavBar";
import SideNavigation from "../components/SideNavigation";

function Dashboard() {
  return (
    <div className="App">
      <NavBar/>
      <SideNavigation pageName={"Home"} />
    </div>
  );
}

export default Dashboard;
