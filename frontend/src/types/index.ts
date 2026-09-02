export interface AlcoholType {
  id: string;
  name: string;
  percentage: number;
}

export interface User {
  weight: number; // in kg
  gender: 'male' | 'female';
}

export interface CalculationResult {
  grams: number;
  bac: number;
  waterMl: number;
  glasses: number;
  hydrationLevel: 'Bajo' | 'Moderado' | 'Alto';
}
