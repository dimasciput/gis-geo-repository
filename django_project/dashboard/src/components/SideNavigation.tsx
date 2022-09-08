import React from 'react';
import HomeIcon from '@mui/icons-material/Home';
import UploadIcon from '@mui/icons-material/Upload';
import '../styles/SideNavigation.scss';
import {routes} from "../views/routes";
import {
  NavLink
} from "react-router-dom";

interface SideNavigationProps {
  pageName: string;
}

export default function SideNavigation(props: SideNavigationProps) {
  return (
    <div className='SideNavigation'>
      { routes.map((route, key)=> (
        <NavLink to={route.path} className='SideNavigation-Row' key={key}>
          <HomeIcon className='SideNavigation-Row-Icon'/>
          <span className='SideNavigation-Row-Name'>{route.name}</span>
        </NavLink>
      ))}
    </div>
  )
}
