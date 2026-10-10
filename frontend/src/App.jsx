import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Settings from "./pages/Settings";
import ProjectLayout from "./pages/project/ProjectLayout";
import Overview from "./pages/project/Overview";
import Notes from "./pages/project/Notes";
import Files from "./pages/project/Files";
import AI from "./pages/project/AI";
import Chat from "./pages/project/Chat";
import Tasks from "./pages/project/Tasks";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/projects/:id" element={<ProjectLayout />}>
            <Route index element={<Overview />} />
            <Route path="notes" element={<Notes />} />
            <Route path="files" element={<Files />} />
            <Route path="ai" element={<AI />} />
            <Route path="chat" element={<Chat />} />
            <Route path="tasks" element={<Tasks />} />
          </Route>
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
