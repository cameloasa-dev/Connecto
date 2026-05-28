// frontend/tests/integration/AddMemberModal.integration.test.jsx

import { describe, it, expect } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AddMemberModal from "../../src/components/circles/AddMemberModal";
import { server } from "../mocks/server";
import { http, HttpResponse } from "msw";

describe("AddMemberModal (integration)", () => {
  it("fetches and displays users from API", async () => {
    // MSW must intercept the REAL endpoint used by the service
    server.use(
      http.get("/users/search", ({ request }) => {
        const url = new URL(request.url);
        const query = url.searchParams.get("query");
        const circleId = url.searchParams.get("circle_id");

        if (query === "Bob" && circleId === "5") {
          return HttpResponse.json([
            {
              id: 4,
              username: "Bob",
              email: "bob@test.com",
              is_already_member: false,
            },
          ]);
        }

        return HttpResponse.json([]);
      }),
    );

    render(
      <AddMemberModal
        isOpen={true}
        onClose={() => {}}
        circleId={5}
        onMemberAdded={() => {}}
      />,
    );

    await userEvent.type(
      screen.getByPlaceholderText(/search by username/i),
      "Bob",
    );

    fireEvent.click(screen.getByRole("button", { name: /search/i }));

    await waitFor(() => {
      expect(screen.getByText("Bob")).toBeInTheDocument();
      expect(screen.getByText("bob@test.com")).toBeInTheDocument();
    });
  });
});
