import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, Modal, FlatList } from 'react-native';
import Input from './ui/Input';
import Button from './ui/Button';
import Card from './ui/Card';
import { alcoholTypes } from '../constants/alcoholTypes';
import { AlcoholType, User } from '../types';

interface AlcoholFormProps {
  onCalculate: (alcohol: AlcoholType, volumeMl: number, user: User) => void;
}

const AlcoholForm: React.FC<AlcoholFormProps> = ({ onCalculate }) => {
  const [selectedAlcohol, setSelectedAlcohol] = useState<AlcoholType>(alcoholTypes[0]);
  const [volume, setVolume] = useState<string>('');
  const [weight, setWeight] = useState<string>('');
  const [gender, setGender] = useState<'male' | 'female'>('male');
  const [errors, setErrors] = useState<{ volume?: string; weight?: string }>({});
  const [modalVisible, setModalVisible] = useState<boolean>(false);

  const validate = (): boolean => {
    const newErrors: { volume?: string; weight?: string } = {};

    if (!volume || parseFloat(volume) <= 0) {
      newErrors.volume = 'Ingresa un volumen válido';
    }

    if (!weight || parseFloat(weight) <= 0) {
      newErrors.weight = 'Ingresa un peso válido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleCalculate = () => {
    if (!validate()) return;

    const volumeNum = parseFloat(volume);
    const weightNum = parseFloat(weight);

    const user: User = {
      weight: weightNum,
      gender: gender,
    };

    onCalculate(selectedAlcohol, volumeNum, user);
  };

  const renderAlcoholSelector = () => {
    return (
      <>
        <TouchableOpacity
          className="bg-gray-100 rounded-lg px-4 py-3 border border-gray-200"
          onPress={() => setModalVisible(true)}
        >
          <Text className="text-gray-800">
            {selectedAlcohol.name} ({selectedAlcohol.percentage}%)
          </Text>
        </TouchableOpacity>

        <Modal
          visible={modalVisible}
          transparent={true}
          animationType="slide"
        >
          <View className="flex-1 justify-end bg-black/50">
            <View className="bg-white rounded-t-2xl p-4">
              <Text className="text-lg font-bold text-gray-800 mb-4 text-center">
                Selecciona el tipo de alcohol
              </Text>
              <FlatList
                data={alcoholTypes}
                keyExtractor={(item) => item.id}
                renderItem={({ item }) => (
                  <TouchableOpacity
                    className={`px-4 py-3 border-b border-gray-100 ${
                      selectedAlcohol.id === item.id ? 'bg-blue-50' : ''
                    }`}
                    onPress={() => {
                      setSelectedAlcohol(item);
                      setModalVisible(false);
                    }}
                  >
                    <Text
                      className={`text-base ${
                        selectedAlcohol.id === item.id
                          ? 'text-blue-600 font-bold'
                          : 'text-gray-800'
                      }`}
                    >
                      {item.name} ({item.percentage}%)
                    </Text>
                  </TouchableOpacity>
                )}
              />
              <Button
                title="Cancelar"
                onPress={() => setModalVisible(false)}
                variant="secondary"
                className="mt-4"
              />
            </View>
          </View>
        </Modal>
      </>
    );
  };

  return (
    <ScrollView className="flex-1">
      <Card className="mb-4">
        <Text className="text-xl font-bold text-gray-800 mb-4">
          Calculadora de hidratación
        </Text>

        <View className="mb-4">
          <Text className="text-gray-700 font-medium mb-2 text-sm">
            Tipo de Alcohol
          </Text>
          {renderAlcoholSelector()}
        </View>

        <Input
          label="Cantidad (ml)"
          value={volume}
          onChangeText={setVolume}
          placeholder="Ej: 330"
          keyboardType="numeric"
          error={errors.volume}
        />

        <Input
          label="Peso (kg)"
          value={weight}
          onChangeText={setWeight}
          placeholder="Ej: 70"
          keyboardType="numeric"
          error={errors.weight}
        />

        <View className="mb-4">
          <Text className="text-gray-700 font-medium mb-2 text-sm">
            Género
          </Text>
          <View className="flex-row gap-2">
            <Button
              title="Hombre"
              variant={gender === 'male' ? 'primary' : 'secondary'}
              onPress={() => setGender('male')}
              className="flex-1"
            />
            <Button
              title="Mujer"
              variant={gender === 'female' ? 'primary' : 'secondary'}
              onPress={() => setGender('female')}
              className="flex-1"
            />
          </View>
        </View>

        <Button
          title="Calcular"
          onPress={handleCalculate}
          variant="primary"
          className="mt-2 bg-blue-700"
        />
      </Card>
    </ScrollView>
  );
};

export default AlcoholForm;
