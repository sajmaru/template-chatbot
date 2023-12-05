import './App.css';
import {
    createBrowserRouter,
    RouterProvider,
} from "react-router-dom";
import SideBar from "./components/SideBar/SideBar";
import ErrorPage from "./components/Error/Error";
import DataFinder from "./components/Data Finder/DataFinder";

import { GoogleOAuthProvider } from '@react-oauth/google';

const router = createBrowserRouter([
    {
        element: <SideBar />,
        errorElement: <ErrorPage />,
        children: [
              {
                path: "/",
                element: <DataFinder />,
              }
        ]
    }
]);

function App() {
    return (
        <GoogleOAuthProvider clientId="1013659242341-3n6hqkdiqep805g7tbe4t0ngo2h2qpg6.apps.googleusercontent.com">
            <RouterProvider router={router} />
        </GoogleOAuthProvider>
    );
}

export default App;
