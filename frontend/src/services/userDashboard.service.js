// frontend/src/services/userDashboard.service.js
import api from "./api";
import { circleService } from "./circle.service";
import { postService } from "./post.service";

export const userDashboardService = {
  async getUserDashboardData() {
    const [userResponse, circles, posts] = await Promise.all([
      api.get("/auth/me"),
      circleService.getMyCircles(),
      postService.getFeed(10),
    ]);

    const user = userResponse.data;

    return {
      user,
      circles,
      posts,
      circlesCount: circles?.length ?? 0,
      postsCount: posts?.length ?? 0,
      notificationsCount: 0,
    };
  },
};
