// frontend/tests/mocks/handlers.js
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/users/search", ({ request }) => {
    return HttpResponse.json([]); // default fallback
  }),
];
