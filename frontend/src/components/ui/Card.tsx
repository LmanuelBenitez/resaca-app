import React from 'react';
import { View, ViewStyle } from 'react-native';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  style?: ViewStyle;
}

const Card: React.FC<CardProps> = ({ children, className = '', style }) => {
  return (
    <View
      className={`bg-white rounded-xl shadow-md p-4 ${className}`}
      style={style}
    >
      {children}
    </View>
  );
};

export default Card;
