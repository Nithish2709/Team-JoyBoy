import { useQuery } from '@tanstack/react-query';
import { fetchFPSDetails, type FPSDetails } from '../api/fpsApi';

export const useFPSData = (shopId: string) => {
  return useQuery<FPSDetails, Error>({
    queryKey: ['fps', shopId],
    queryFn: () => fetchFPSDetails(shopId),
    staleTime: 5 * 60 * 1000, // Consider data fresh for 5 minutes
  });
};
