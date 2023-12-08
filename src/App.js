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
        <GoogleOAuthProvider clientId="484642080236-5mqjaglq1i61v76vttcprlocdsl4e2bi.apps.googleusercontent.com">
            <RouterProvider router={router} />
        </GoogleOAuthProvider>
    );
}

export default App;
