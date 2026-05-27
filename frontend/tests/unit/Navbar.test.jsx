//frontend/ tests/unit/Navbar.test.jsx
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Navbar from "../../src/components/layout/Navbar";

// Mock for useAuth (contexts/useAuth.js)
vi.mock("../../src/contexts/useAuth", () => ({
  useAuth: vi.fn(),
}));

// Mock for useDarkMode (hooks/useDarkMode.js)
vi.mock("../../src/hooks/useDarkMode", () => ({
  useDarkMode: vi.fn(),
}));

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: vi.fn(),
  };
});

// Import the mocked hooks after mocking
import { useAuth } from "../../src/contexts/useAuth";
import { useDarkMode } from "../../src/hooks/useDarkMode";
import { useNavigate } from "react-router-dom";

describe("Navbar Component", () => {
  const mockNavigate = vi.fn();
  const mockLogout = vi.fn();
  const mockToggleDarkMode = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();

    // Setup default mocks
    useNavigate.mockReturnValue(mockNavigate);
    useDarkMode.mockReturnValue({
      isDarkMode: false,
      toggleDarkMode: mockToggleDarkMode,
    });
  });

  const renderNavbar = (authState = { user: null }) => {
    useAuth.mockReturnValue({
      user: authState.user,
      logout: mockLogout,
    });

    return render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>,
    );
  };

  describe("Unauthenticated User", () => {
    it("renders minimal navbar with login and register buttons when user is not authenticated", () => {
      renderNavbar({ user: null });

      expect(screen.getByText("Social Circles")).toBeInTheDocument();
      expect(
        screen.getByRole("button", { name: /login/i }),
      ).toBeInTheDocument();
      expect(
        screen.getByRole("button", { name: /register/i }),
      ).toBeInTheDocument();
      expect(
        screen.queryByPlaceholderText(/search circles/i),
      ).not.toBeInTheDocument();
    });

    it("navigates to login page when login button is clicked", () => {
      renderNavbar({ user: null });

      const loginButton = screen.getByRole("button", { name: /login/i });
      fireEvent.click(loginButton);

      expect(mockNavigate).toHaveBeenCalledWith("/login");
    });

    it("navigates to register page when register button is clicked", () => {
      renderNavbar({ user: null });

      const registerButton = screen.getByRole("button", { name: /register/i });
      fireEvent.click(registerButton);

      expect(mockNavigate).toHaveBeenCalledWith("/register");
    });

    it("navigates to home page when logo is clicked", () => {
      renderNavbar({ user: null });

      const logo = screen.getByText("Social Circles");
      fireEvent.click(logo);

      expect(mockNavigate).toHaveBeenCalledWith("/");
    });
  });

  describe("Authenticated User", () => {
    const mockUser = {
      username: "testuser",
      email: "test@example.com",
    };

    beforeEach(() => {
      renderNavbar({ user: mockUser });
    });

    it("renders navbar with user information and authenticated elements", () => {
      expect(screen.getByText("@testuser")).toBeInTheDocument();
      expect(screen.getByText("T")).toBeInTheDocument();
      expect(
        screen.getByPlaceholderText(/search circles, posts, people/i),
      ).toBeInTheDocument();
      expect(screen.getByTitle(/switch to dark mode/i)).toBeInTheDocument();
      expect(screen.getByTitle(/notifications/i)).toBeInTheDocument();
      expect(screen.getByTitle(/messages/i)).toBeInTheDocument();
      expect(screen.getByText("3")).toBeInTheDocument();
    });

    it("navigates to user dashboard when logo is clicked", () => {
      const logo = screen.getByText("Social Circles");
      fireEvent.click(logo);

      expect(mockNavigate).toHaveBeenCalledWith("/user-dashboard");
    });

    it("handles search form submission", () => {
      const searchInput = screen.getByPlaceholderText(
        /search circles, posts, people/i,
      );
      const searchButton = screen.getByRole("button", { name: "🔍" });

      fireEvent.change(searchInput, { target: { value: "test search" } });
      expect(searchInput.value).toBe("test search");

      fireEvent.click(searchButton);

      expect(mockNavigate).toHaveBeenCalledWith("/search?q=test%20search");
    });

    it("does not navigate on empty search submission", () => {
      const searchButton = screen.getByRole("button", { name: "🔍" });

      fireEvent.click(searchButton);

      expect(mockNavigate).not.toHaveBeenCalled();
    });

    it("toggles dark mode when dark mode button is clicked", () => {
      const darkModeButton = screen.getByTitle(/switch to dark mode/i);
      fireEvent.click(darkModeButton);

      expect(mockToggleDarkMode).toHaveBeenCalledTimes(1);
    });

    it("shows different dark mode icon based on state", () => {
      expect(screen.getByText("🌙")).toBeInTheDocument();

      // Re-render with dark mode on
      useDarkMode.mockReturnValue({
        isDarkMode: true,
        toggleDarkMode: mockToggleDarkMode,
      });

      renderNavbar({ user: mockUser });
      expect(screen.getByText("☀️")).toBeInTheDocument();
      expect(screen.getByTitle(/switch to light mode/i)).toBeInTheDocument();
    });
  });

  describe("User Dropdown Menu", () => {
    const mockUser = {
      username: "testuser",
    };

    it("opens dropdown when user section is clicked", () => {
      renderNavbar({ user: mockUser });

      expect(screen.queryByText("Profile")).not.toBeInTheDocument();

      const userSection = screen.getByText("@testuser").closest(".navbar-user");
      fireEvent.click(userSection);

      expect(screen.getByText("Profile")).toBeInTheDocument();
      expect(screen.getByText("Settings")).toBeInTheDocument();
      expect(screen.getByText("Logout")).toBeInTheDocument();
      expect(screen.getByText("▲")).toBeInTheDocument();
    });

    it("closes dropdown when clicked again", () => {
      renderNavbar({ user: mockUser });

      const userSection = screen.getByText("@testuser").closest(".navbar-user");

      fireEvent.click(userSection);
      expect(screen.getByText("Profile")).toBeInTheDocument();

      fireEvent.click(userSection);
      expect(screen.queryByText("Profile")).not.toBeInTheDocument();
    });

    it("navigates to profile page when Profile is clicked", () => {
      renderNavbar({ user: mockUser });

      const userSection = screen.getByText("@testuser").closest(".navbar-user");
      fireEvent.click(userSection);

      const profileButton = screen.getByText("Profile");
      fireEvent.click(profileButton);

      expect(mockNavigate).toHaveBeenCalledWith("/profile");
      expect(screen.queryByText("Profile")).not.toBeInTheDocument();
    });

    it("navigates to settings page when Settings is clicked", () => {
      renderNavbar({ user: mockUser });

      const userSection = screen.getByText("@testuser").closest(".navbar-user");
      fireEvent.click(userSection);

      const settingsButton = screen.getByText("Settings");
      fireEvent.click(settingsButton);

      expect(mockNavigate).toHaveBeenCalledWith("/settings");
    });

    describe("Logout Functionality", () => {
      beforeEach(() => {
        vi.spyOn(window, "confirm").mockImplementation(() => true);
      });

      it("handles successful logout", async () => {
        mockLogout.mockResolvedValueOnce();

        renderNavbar({ user: mockUser });

        const userSection = screen
          .getByText("@testuser")
          .closest(".navbar-user");
        fireEvent.click(userSection);

        const logoutButton = screen.getByText("Logout");
        fireEvent.click(logoutButton);

        expect(window.confirm).toHaveBeenCalledWith(
          "Are you sure you want to logout?",
        );

        await waitFor(() => {
          expect(mockLogout).toHaveBeenCalledTimes(1);
          expect(mockNavigate).toHaveBeenCalledWith("/login");
        });
      });

      it("handles logout failure", async () => {
        const consoleErrorSpy = vi
          .spyOn(console, "error")
          .mockImplementation(() => {});
        const alertSpy = vi.spyOn(window, "alert").mockImplementation(() => {});

        mockLogout.mockRejectedValueOnce(new Error("Logout failed"));

        renderNavbar({ user: mockUser });

        const userSection = screen
          .getByText("@testuser")
          .closest(".navbar-user");
        fireEvent.click(userSection);

        const logoutButton = screen.getByText("Logout");
        fireEvent.click(logoutButton);

        await waitFor(() => {
          expect(mockLogout).toHaveBeenCalledTimes(1);
          expect(consoleErrorSpy).toHaveBeenCalled();
          expect(alertSpy).toHaveBeenCalledWith(
            "Logout failed. Please try again.",
          );
          expect(mockNavigate).not.toHaveBeenCalled();
        });

        consoleErrorSpy.mockRestore();
        alertSpy.mockRestore();
      });

      it("cancels logout when confirm is false", () => {
        vi.spyOn(window, "confirm").mockImplementation(() => false);

        renderNavbar({ user: mockUser });

        const userSection = screen
          .getByText("@testuser")
          .closest(".navbar-user");
        fireEvent.click(userSection);

        const logoutButton = screen.getByText("Logout");
        fireEvent.click(logoutButton);

        expect(window.confirm).toHaveBeenCalledWith(
          "Are you sure you want to logout?",
        );
        expect(mockLogout).not.toHaveBeenCalled();
        expect(mockNavigate).not.toHaveBeenCalled();
      });
    });
  });

  describe("Accessibility and Edge Cases", () => {
    it("handles user with no username", () => {
      const userWithNoName = {
        email: "test@example.com",
      };

      renderNavbar({ user: userWithNoName });

      expect(screen.getByText("U")).toBeInTheDocument();
    });

    it("handles keyboard navigation for search", () => {
      renderNavbar({ user: { username: "testuser" } });

      const searchInput = screen.getByPlaceholderText(/search circles/i);

      fireEvent.change(searchInput, { target: { value: "keyboard search" } });
      fireEvent.submit(searchInput.closest("form"));

      expect(mockNavigate).toHaveBeenCalledWith("/search?q=keyboard%20search");
    });

    it("has proper ARIA labels and semantic structure", () => {
      renderNavbar({ user: { username: "testuser" } });

      const header = document.querySelector("header.navbar");
      expect(header).toBeInTheDocument();

      const searchForm = document.querySelector("form.navbar-search");
      expect(searchForm).toBeInTheDocument();

      expect(screen.getByTitle(/notifications/i)).toBeInTheDocument();
      expect(screen.getByTitle(/messages/i)).toBeInTheDocument();

      expect(screen.getByRole("banner")).toBeInTheDocument();
    });
  });
});
