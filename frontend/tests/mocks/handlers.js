import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("*/auth/me", () => {
    return HttpResponse.json({
      id: 1,
      username: "default-user",
    });
  }),

  http.get("*/circles/my", () => {
    return HttpResponse.json([]);
  }),

  http.get("*/posts/feed", () => {
    return HttpResponse.json([]);
  }),
];
