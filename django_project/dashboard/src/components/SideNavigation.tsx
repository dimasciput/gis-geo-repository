import React from 'react';
import HomeIcon from '@mui/icons-material/Home';
import UploadIcon from '@mui/icons-material/Upload';
import '../styles/SideNavigation.scss';

interface SideNavigationProps {
  pageName: string;
}

export default function SideNavigation(props: SideNavigationProps) {
  return (
    <div className='SideNavigation'>
      <a href='/' className='SideNavigation-Row'>
        <HomeIcon className='SideNavigation-Row-Icon'/>
        <span className='SideNavigation-Row-Name'>Home</span>
      </a>
      <a href='/' className='SideNavigation-Row'>
        <UploadIcon className='SideNavigation-Row-Icon'/>
        <span className='SideNavigation-Row-Name'>Upload</span>
      </a>
    </div>
  )
}
