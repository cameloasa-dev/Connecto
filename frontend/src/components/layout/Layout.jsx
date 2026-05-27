// frontend/src/components/layout/Layout.jsx
import Navbar from "./Navbar";
import UserSidebar from "./UserSidebar";

const Layout = ({ children }) => {
  return (
    <div className="dashboard-layout">
      <Navbar />
      <div className="dashboard-content">
        <UserSidebar />
        <main className="dashboard-main">{children}</main>
      </div>
    </div>
  );
};

export default Layout;
