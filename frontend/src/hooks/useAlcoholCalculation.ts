import { useState } from 'react';
import { calculationService } from '../services/api/calculationService';

export const useAlcoholCalculation = () => {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const calculate = async (
    alcoholType: string,
    volumeMl: number,
    weightKg: number,
    gender: 'male' | 'female'
  ) => {
    setLoading(true);
    setError(null);

    try {
      const response = await calculationService.calculate({
        alcohol_type: alcoholType,
        volume_ml: volumeMl,
        weight_kg: weightKg,
        gender: gender,
      });

      setResult(response);
      return response;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error al calcular';
      setError(message);
      throw new Error(message);
    } finally {
      setLoading(false);
    }
  };

  return { result, loading, error, calculate };
};