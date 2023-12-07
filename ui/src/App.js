import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import SideBar from "./components/SideBar/SideBar";
import ErrorPage from "./components/Error/Error";
import DataFinder from "./components/Data Finder/DataFinder";

import { GoogleOAuthProvider } from "@react-oauth/google";

const router = createBrowserRouter([
  {
    element: <SideBar />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <DataFinder />,
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
