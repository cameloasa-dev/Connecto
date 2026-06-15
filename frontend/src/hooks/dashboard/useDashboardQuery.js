// frontend/src/hooks/dashboard/useDashboardQuery.js
import { useQuery } from "@tanstack/react-query";
import { userDashboardService } from "../../services/userDashboard.service";

export const useDashboardQuery = () => {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: userDashboardService.getUserDashboardData,
  });
};
