import React from 'react';
import { TextInput, View, Text, TextInputProps, TextStyle } from 'react-native';

interface InputProps extends TextInputProps {
  label?: string;
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
  keyboardType?: 'default' | 'numeric' | 'email-address' | 'phone-pad';
  error?: string;
  className?: string;
  style?: TextStyle;  // ← Cambiar de ViewStyle a TextStyle
}

const Input: React.FC<InputProps> = ({
  label,
  value,
  onChangeText,
  placeholder = '',
  keyboardType = 'default',
  error,
  className = '',
  style,
  ...props
}) => {
  return (
    <View className={`mb-4 ${className}`} style={style as any}>
      {label && (
        <Text className="text-gray-700 font-medium mb-2 text-sm">
          {label}
        </Text>
      )}
      <TextInput
        className={`bg-gray-100 rounded-lg px-4 py-3 text-gray-800 border ${
          error ? 'border-red-500' : 'border-gray-200'
        } focus:border-blue-500`}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor="#9CA3AF"
        keyboardType={keyboardType}
        {...props}
      />
      {error && (
        <Text className="text-red-500 text-sm mt-1">{error}</Text>
      )}
    </View>
  );
};

export default Input;