export interface AlcoholType {
  id: string;
  name: string;
  percentage: number;
}

export const alcoholTypes: AlcoholType[] = [
  { id: 'beer', name: 'Cerveza', percentage: 5 },
  { id: 'wine', name: 'Vino', percentage: 12 },
  { id: 'whisky', name: 'Whisky', percentage: 40 },
  { id: 'vodka', name: 'Vodka', percentage: 40 },
  { id: 'rum', name: 'Ron', percentage: 40 },
  { id: 'tequila', name: 'Tequila', percentage: 38 },
];
