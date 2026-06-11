import { renderHook } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { useCirclePermissions } from "../../src/hooks/useCirclePermissions";

// mock context
vi.mock("../../src/contexts/useAuth", () => ({
  useAuth: vi.fn(),
}));

import { useAuth } from "../../src/contexts/useAuth";

describe("useCirclePermissions (unit)", () => {
  it("returns owner permissions correctly", () => {
    // ARRANGE
    useAuth.mockReturnValue({
      user: { id: 1 },
    });

    const circle = {
      members: [{ user_id: 1, role: "owner" }],
    };

    // ACT
    const { result } = renderHook(() =>
      useCirclePermissions(circle)
    );

    // ASSERT
    expect(result.current.isOwner).toBe(true);
    expect(result.current.canDeleteCircle).toBe(true);
    expect(result.current.canChangeRoles).toBe(true);
  });

  it("returns all false when no user", () => {
    // ARRANGE
    useAuth.mockReturnValue({
      user: null,
    });

    const { result } = renderHook(() =>
      useCirclePermissions({
        members: [{ user_id: 1, role: "owner" }],
      })
    );

    expect(result.current.isOwner).toBe(false);
    expect(result.current.canModerate).toBe(false);
  });

  it("returns member permissions correctly", () => {
    useAuth.mockReturnValue({
      user: { id: 1 },
    });

    const circle = {
      members: [{ user_id: 1, role: "moderator" }],
    };

    const { result } = renderHook(() =>
      useCirclePermissions(circle)
    );

    expect(result.current.isModerator).toBe(true);
    expect(result.current.canModerate).toBe(true);
    expect(result.current.canChangeRoles).toBe(false);
  });
});