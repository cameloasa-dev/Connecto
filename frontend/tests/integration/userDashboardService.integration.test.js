import { describe, it, expect, vi, beforeEach } from "vitest";
import { server } from "../mocks/server";
import { http, HttpResponse } from "msw";

import { userDashboardService } from "../../src/services/userDashboard.service";

import { userFixture } from "../mocks/fixtures/user.fixture";
import { circlesFixture } from "../mocks/fixtures/circles.fixture";
import { postsFixture } from "../mocks/fixtures/posts.fixture";

// global setup for all tests in this file
beforeEach(() => {
  vi.clearAllMocks();
});

// 🧪 INTEGRATION TESTS FOR userDashboardService
describe("userDashboardService (integration)", () => {
  it("returns aggregated dashboard data", async () => {
    // ARRANGE (override MSW default handlers)
    server.use(
      http.get("*/auth/me", () => HttpResponse.json(userFixture)),

      http.get("*/circles/my", () => HttpResponse.json(circlesFixture)),

      http.get("*/posts/feed", ({ request }) => {
        const url = new URL(request.url);

        expect(url.searchParams.get("limit")).toBe("10");

        return HttpResponse.json(postsFixture);
      }),
    );

    // ACT
    const result = await userDashboardService.getUserDashboardData();

    // ASSERT
    expect(result).toEqual({
      user: userFixture,
      circles: circlesFixture,
      posts: postsFixture,
      circlesCount: circlesFixture.length,
      postsCount: postsFixture.length,
      notificationsCount: 0,
    });
  });

  // 🧪 EMPTY CASE
  it("handles empty responses safely", async () => {
    server.use(
      http.get("*/auth/me", () => HttpResponse.json(userFixture)),

      http.get("*/circles/my", () => HttpResponse.json([])),

      http.get("*/posts/feed", () => HttpResponse.json([])),
    );

    const result = await userDashboardService.getUserDashboardData();

    expect(result.circlesCount).toBe(0);
    expect(result.postsCount).toBe(0);
  });

  // 🧪 FAILURE CASE
  it("throws error when one request fails", async () => {
    server.use(
      http.get("*/auth/me", () => HttpResponse.json(userFixture)),

      http.get("*/circles/my", () => new HttpResponse(null, { status: 500 })),

      http.get("*/posts/feed", () => HttpResponse.json([])),
    );

    await expect(userDashboardService.getUserDashboardData()).rejects.toThrow();
  });
});
