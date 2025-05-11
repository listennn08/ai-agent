import { createBrowserRouter } from "react-router";
import Home from "./pages/home";
import Assistant from "./pages/assistant";
import App from "./App";

const router = createBrowserRouter([
  {
    path: '/',
    Component: App,
    children: [
      {
        path: '',
        index: true,
        Component: Home,
      },
      {
        path: '/assistant',
        Component: Assistant,
      },
    ],
  },
])

export default router
