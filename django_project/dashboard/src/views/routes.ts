import {Home} from "./Dashboard";
import Uploader from "./Upload";
import HomeIcon from '@mui/icons-material/Home';
import UploadIcon from '@mui/icons-material/Upload';
import {OverridableComponent} from "@mui/material/OverridableComponent";
import {SvgIconTypeMap} from "@mui/material/SvgIcon/SvgIcon";

interface RouteInterface {
  name: string,
  path: string,
  element: any,
  icon: OverridableComponent<SvgIconTypeMap> | null
}

export const routes: Array<RouteInterface> = [
  {
    name: 'Home', path: '/', element: Home, icon: HomeIcon
  },
  {
    name: 'Uploader', path: '/uploader', element: Uploader, icon: UploadIcon
  }
]
