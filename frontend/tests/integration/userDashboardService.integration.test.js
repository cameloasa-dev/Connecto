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
describe("userDashboardService", () => {
  it("returns dashboard data", async () => {
    server.use(
      http.get("*/dashboard", () =>
        HttpResponse.json({
          user: userFixture,
          circles: circlesFixture,
          feed: postsFixture,
          stats: {
            total_circles: circlesFixture.length,
            total_posts_in_feed: postsFixture.length,
          },
        }),
      ),
    );

    const result = await userDashboardService.getUserDashboardData();

    expect(result.user).toEqual(userFixture);
    expect(result.circles).toEqual(circlesFixture);
    expect(result.feed).toEqual(postsFixture);
    expect(result.stats.total_circles).toBe(circlesFixture.length);
  });
});

// 🧪 EMPTY CASE
server.use(
  http.get("*/dashboard", () =>
    HttpResponse.json({
      user: userFixture,
      circles: [],
      feed: [],
      stats: {
        total_circles: 0,
        total_posts_in_feed: 0,
      },
    }),
  ),
);

// 🧪 FAILURE CASE
server.use(
  http.get("*/dashboard", () => new HttpResponse(null, { status: 500 })),
);

await expect(userDashboardService.getUserDashboardData()).rejects.toThrow();
