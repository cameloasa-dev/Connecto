// frontend/src/services/userDashboard.service.js
import api from "./api";
import { circleService } from "./circle.service";
import { postService } from "./post.service";

export const userDashboardService = {
  async getUserDashboardData() {
    try {
      // 3 parallel API calls
      const [userResponse, circles, posts] = await Promise.all([
        api.get("/auth/me"),          // user info
        circleService.getMyCircles(), // circles with badges
        postService.getFeed(10),      // recent posts
      ]);

      return {
        user: userResponse.data,
        circles,
        posts,
        circlesCount: circles?.length || 0,
        postsCount: posts?.length || 0,
        notificationsCount: 0,
      };
    } catch (err) {
      const message = err.message || "Failed to load dashboard data";
      console.error("User Dashboard service error:", message);
      throw new Error(message);
    }
  },
};
