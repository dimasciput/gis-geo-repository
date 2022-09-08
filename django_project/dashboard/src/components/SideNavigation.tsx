import React from 'react';
import '../styles/SideNavigation.scss';
import {routes} from "../views/routes";
import {
  NavLink
} from "react-router-dom";

interface SideNavigationProps {}

export default function SideNavigation(props: SideNavigationProps) {
  return (
    <div className='SideNavigation'>
      { routes.map((route, key)=> (
        <NavLink to={route.path} className='SideNavigation-Row' key={key}>
          <route.icon className='SideNavigation-Row-Icon'/>
          <span className='SideNavigation-Row-Name'>{route.name}</span>
        </NavLink>
      ))}
    </div>
  )
}
