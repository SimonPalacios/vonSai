// Add crete browser router and routes to App.tsx

import Home from "@components/Home";
import Layout from "@components/Layout";
import NotFound from "@components/NotFound";
import Repositorios from "@components/Respositorios";
import UsersList from "@components/UsersList";
import { createBrowserRouter } from "react-router-dom";


const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    errorElement: <NotFound />,
    children: [
      {
        path: "/",
        element: <Home />,
      },{
        path: "/users",
        element: <UsersList />,
      },{
        path: "/Repositorios",
        element: <Repositorios/>,
      }
    ],
  },
]);

export default router;