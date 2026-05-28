import "@testing-library/jest-dom";
import { server } from "./mocks/server";

// Start MSW before all tests
beforeAll(() => server.listen());

// Reset handlers after each test (important for integration tests)
afterEach(() => server.resetHandlers());

// Stop MSW after all tests
afterAll(() => server.close());
