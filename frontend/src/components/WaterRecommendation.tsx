import React from 'react';
import { View, Text } from 'react-native';
import Card from './ui/Card';
import { CalculationResult } from '../types';

interface WaterRecommendationProps {
  result: CalculationResult;
}

const WaterRecommendation: React.FC<WaterRecommendationProps> = ({ result }) => {
  const getHydrationColor = (level: string): string => {
    switch (level) {
      case 'Bajo':
        return 'bg-green-100 border-green-500 text-green-700';
      case 'Moderado':
        return 'bg-yellow-100 border-yellow-500 text-yellow-700';
      case 'Alto':
        return 'bg-red-100 border-red-500 text-red-700';
      default:
        return 'bg-gray-100 border-gray-500 text-gray-700';
    }
  };

  const getBACColor = (bac: number): string => {
    if (bac < 0.05) return 'text-green-600';
    if (bac < 0.08) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getHydrationEmoji = (level: string): string => {
    switch (level) {
      case 'Bajo':
        return '💧';
      case 'Moderado':
        return '💦';
      case 'Alto':
        return '🌊';
      default:
        return '💧';
    }
  };

  return (
    <View className="space-y-4">
      <Card>
        <Text className="text-lg font-bold text-gray-800 mb-2">
          Resultados del Cálculo
        </Text>

        <View className="space-y-3">
          <View className="flex-row justify-between items-center py-2 border-b border-gray-100">
            <Text className="text-gray-600">Gramos de Alcohol:</Text>
            <Text className="font-bold text-gray-800">
              {result.grams.toFixed(2)} g
            </Text>
          </View>

          <View className="flex-row justify-between items-center py-2 border-b border-gray-100">
            <Text className="text-gray-600">BAC (Alcohol en Sangre):</Text>
            <Text className={`font-bold ${getBACColor(result.bac)}`}>
              {(result.bac * 100).toFixed(2)}%
            </Text>
          </View>

          <View className="flex-row justify-between items-center py-2 border-b border-gray-100">
            <Text className="text-gray-600">Agua Recomendada:</Text>
            <Text className="font-bold text-blue-600">
              {result.waterMl.toFixed(0)} ml
            </Text>
          </View>

          <View className="flex-row justify-between items-center py-2 border-b border-gray-100">
            <Text className="text-gray-600">Vasos de Agua (250ml):</Text>
            <Text className="font-bold text-blue-600">
              {result.glasses.toFixed(1)} vasos
            </Text>
          </View>

          <View className="flex-row justify-between items-center py-2">
            <Text className="text-gray-600">Nivel de Hidratación:</Text>
            <View
              className={`px-3 py-1 rounded-full border ${getHydrationColor(
                result.hydrationLevel
              )}`}
            >
              <Text className={`font-bold ${getHydrationColor(result.hydrationLevel)}`}>
                {getHydrationEmoji(result.hydrationLevel)} {result.hydrationLevel}
              </Text>
            </View>
          </View>
        </View>
      </Card>

      <Card>
        <Text className="text-lg font-bold text-gray-800 mb-2">
          Recomendación
        </Text>
        <Text className="text-gray-600 leading-6">
          {result.hydrationLevel === 'Bajo' &&
            'Tu nivel de hidratación es bueno. Mantén una ingesta regular de agua para mantenerte hidratado.'}
          {result.hydrationLevel === 'Moderado' &&
            'Necesitas aumentar tu ingesta de agua. Bebe al menos ' +
            result.glasses.toFixed(1) +
            ' vasos de agua para mantener una buena hidratación.'}
          {result.hydrationLevel === 'Alto' &&
            'Es crucial que aumentes significativamente tu hidratación. Bebe al menos ' +
            result.glasses.toFixed(1) +
            ' vasos de agua y considera bebidas con electrolitos.'}
        </Text>
      </Card>
    </View>
  );
};

export default WaterRecommendation;
