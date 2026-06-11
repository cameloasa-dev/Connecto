import "@testing-library/jest-dom";
import { server } from "../../mocks/server";

beforeAll(() => {
  server.listen({
    onUnhandledRequest: "error", // Throw an error for any unhandled request to ensure all API calls are mocked
  });
});

afterEach(() => {
  server.resetHandlers();
});

afterAll(() => {
  server.close();
});
