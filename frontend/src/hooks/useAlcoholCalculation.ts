import { useState } from 'react';
import { AlcoholType, User, CalculationResult } from '../types';

export const useAlcoholCalculation = () => {
  const [result, setResult] = useState<CalculationResult | null>(null);

  const calculate = (alcohol: AlcoholType, volumeMl: number, user: User) => {
    // Calculate grams of alcohol
    const grams = volumeMl * (alcohol.percentage / 100) * 0.789;

    // Calculate BAC
    const factor = user.gender === 'male' ? 0.73 : 0.66;
    const bac = grams / (user.weight * factor);

    // Calculate water needed (simplified formula)
    const waterMl = bac * 5000;
    const glasses = waterMl / 250;

    // Determine hydration level
    let hydrationLevel: 'Bajo' | 'Moderado' | 'Alto';
    if (bac < 0.05) {
      hydrationLevel = 'Bajo';
    } else if (bac < 0.08) {
      hydrationLevel = 'Moderado';
    } else {
      hydrationLevel = 'Alto';
    }

    const calculationResult: CalculationResult = {
      grams,
      bac,
      waterMl,
      glasses,
      hydrationLevel,
    };

    setResult(calculationResult);
    return calculationResult;
  };

  return { result, calculate };
};
