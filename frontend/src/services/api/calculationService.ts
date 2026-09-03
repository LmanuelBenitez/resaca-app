import { apiClient } from './client';

export interface CalculationRequest {
  alcohol_type: string;
  volume_ml: number;
  weight_kg: number;
  gender: 'male' | 'female';
}

export interface CalculationResponse {
  grams: number;
  bac: number;
  water_ml: number;
  glasses: number;
  hydration_level: 'Bajo' | 'Moderado' | 'Alto';
}

export const calculationService = {
  async calculate(data: CalculationRequest): Promise<CalculationResponse> {
    const response = await apiClient.post('/api/v1/calculate', data);
    return response.data;
  },
};