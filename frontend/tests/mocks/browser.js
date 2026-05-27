// frontend/tests/mocks/handlers.js
import { http, HttpResponse } from "msw";

export const handlers = [
  // Default handler 
  http.get("/api/circles/:circleId/search-users", ({ params }) => {
    return HttpResponse.json([]);
  }),
];
