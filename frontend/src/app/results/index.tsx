import React from 'react';
import { View, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter } from 'expo-router';
import WaterRecommendation from '../../components/WaterRecommendation';
import Button from '../../components/ui/Button';

export default function ResultsScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const data = JSON.parse(params.data as string);

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <ScrollView className="flex-1 px-4 pt-4">
        <WaterRecommendation result={data} />
        
        <View className="mt-4 mb-8">
          <Button
            title="Volver a Calcular"
            onPress={() => router.back()}
            variant="secondary"
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}