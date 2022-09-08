import {Home} from "./Dashboard";
import Uploader from "./Upload";

interface RouteInterface {
  name: string,
  path: string,
  element: any
}

export const routes: Array<RouteInterface> = [
  {
    name: 'Home', path: '/', element: Home,
  },
  {
    name: 'Uploader', path: '/uploader', element: Uploader
  }
]
