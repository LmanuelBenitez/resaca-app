import React from 'react';
import { View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import AlcoholForm from '../components/AlcoholForm';
import { useAlcoholCalculation } from '../hooks/useAlcoholCalculation';
import { AlcoholType, User } from '../types';

export default function HomeScreen() {
  const router = useRouter();
  const { calculate } = useAlcoholCalculation();

  const handleCalculate = (alcohol: AlcoholType, volumeMl: number, user: User) => {
    const result = calculate(alcohol, volumeMl, user);
    router.push({
      pathname: '/results' as any,
      params: { data: JSON.stringify(result) }
    });
  };

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <View className="flex-1 px-4 pt-4">
        <AlcoholForm onCalculate={handleCalculate} />
      </View>
    </SafeAreaView>
  );
}