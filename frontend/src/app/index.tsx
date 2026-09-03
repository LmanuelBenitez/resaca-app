import React from 'react';
import { View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import AlcoholForm from '../components/AlcoholForm';
import { useAlcoholCalculation } from '../hooks/useAlcoholCalculation';
import { AlcoholType, User } from '../types';

export default function HomeScreen() {
  const router = useRouter();
  const { calculate, loading, error } = useAlcoholCalculation();

  const handleCalculate = async (alcohol: AlcoholType, volumeMl: number, user: User) => {
    try {
      const result = await calculate(alcohol.id, volumeMl, user.weight, user.gender);
      
      router.push({
        pathname: '/results',
        params: { data: JSON.stringify(result) },
      });
    } catch (err) {
      // El error ya está manejado en el hook
    }
  };

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <View className="flex-1 px-4 pt-4">
        <AlcoholForm 
          onCalculate={handleCalculate}
          loading={loading}
          error={error}
        />
      </View>
    </SafeAreaView>
  );
}