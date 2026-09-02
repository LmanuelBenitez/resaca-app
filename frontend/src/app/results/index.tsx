import React from 'react';
import { View, ScrollView, Text } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { CalculationResult } from '../../types';
import WaterRecommendation from '../../components/WaterRecommendation';
import Button from '../../components/ui/Button';

export default function ResultsScreen() {
  const params = useLocalSearchParams();
  const router = useRouter();

  const result: CalculationResult = {
    grams: parseFloat(params.grams as string) || 0,
    bac: parseFloat(params.bac as string) || 0,
    waterMl: parseFloat(params.waterMl as string) || 0,
    glasses: parseFloat(params.glasses as string) || 0,
    hydrationLevel: (params.hydrationLevel as 'Bajo' | 'Moderado' | 'Alto') || 'Bajo',
  };

  const handleGoBack = () => {
    router.back();
  };

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <ScrollView className="flex-1 px-4 pt-4">
        <View className="mb-4">
          <Text className="text-2xl font-bold text-gray-800">
            Resultados de Hidratación
          </Text>
          <Text className="text-gray-600 mt-1">
            Basado en tu consumo de alcohol
          </Text>
        </View>

        <WaterRecommendation result={result} />

        <View className="mt-6 mb-8">
          <Button
            title="Volver a Calcular"
            onPress={handleGoBack}
            variant="primary"
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
