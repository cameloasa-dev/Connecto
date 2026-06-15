// frontend/src/App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";
import UserDashboardPage from "./pages/UserDashboardPage.jsx";
import CirclePage from "./pages/CirclePage.jsx";
import SearchPage from "./pages/SearchPage.jsx";
//import SettingsPage from './pages/SettingsPage.jsx';
//import HelpPage from './pages/HelpPage.jsx';
import ProtectedRoute from "./routes/ProtectedRoute.jsx";
import AuthProvider from "./contexts/AuthProvider";
import { DarkModeProvider } from "./contexts/DarkModeProvider";
import Layout from "./components/layout/Layout.jsx";
//import "./App.css";
import { APP_BASE_PATH } from "./config";

function App() {
  return (
    <AuthProvider>
      <DarkModeProvider>
        <Router basename={APP_BASE_PATH}>
          <Routes>
            {/* Public routes */}
            <Route index element={<LoginPage />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="register" element={<RegisterPage />} />

            {/* Protected routes */}
            <Route
              path="user-dashboard"
              element={
                <ProtectedRoute>
                  <Layout>
                    <UserDashboardPage />
                  </Layout>
                </ProtectedRoute>
              }
            />

            <Route
              path="circles/:circleId"
              element={
                <ProtectedRoute>
                  <Layout>
                    <CirclePage />
                  </Layout>
                </ProtectedRoute>
              }
            />

            <Route
              path="search"
              element={
                <ProtectedRoute>
                  <Layout>
                    <SearchPage />
                  </Layout>
                </ProtectedRoute>
              }
            />

            {/* Commented out until pages are created */}
            {/* 
          <Route path="settings" element={
            <ProtectedRoute>
              <SettingsPage />
            </ProtectedRoute>
          } />
          
          <Route path="help" element={
            <ProtectedRoute>
              <HelpPage />
            </ProtectedRoute>
          } />
            */}
          </Routes>
        </Router>
      </DarkModeProvider>
    </AuthProvider>
  );
}

export default App;
