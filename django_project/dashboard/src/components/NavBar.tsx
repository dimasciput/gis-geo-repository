import React, {useEffect, useState} from "react";
import '../styles/NavBar.scss';


export default function NavBar() {
  const [siteTitle, setSiteTitle] = useState('');
  const [siteIcon, setSiteIcon] = useState(null);
  useEffect(() => {
    let preferences: any = (
      // @ts-ignore
      window['preferences'] !== undefined ? window['preferences'] : null
    )
    if (preferences) {
      if ('site_title' in preferences) {
        setSiteTitle(preferences['site_title'])
      }
      if ('icon' in preferences) {
        setSiteIcon(preferences['icon'])
      }
    }
  }, [])

  return (
    <header>
      <div className='NavHeader'>
        <ul className='NavHeader Menu'>
          <li className='NavHeaderLogo'>
            <a
              href='/'
              title={'Homepage'}
              className='nav-header-link'
            >
              <img src={siteIcon} alt="Logo"/>
            </a>
          </li>
          <li className='NavHeaderTitle'>
            <button type='button'>
              <a
                href='/'
                title='Homepage'
                className='NavHeaderLink'
              >
                { siteTitle }
              </a>
            </button>
          </li>
        </ul>
      </div>
    </header>
  )
}
