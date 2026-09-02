import React from 'react';
import { TouchableOpacity, Text, ActivityIndicator, ViewStyle, TextStyle } from 'react-native';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  loading?: boolean;
  className?: string;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  disabled = false,
  loading = false,
  className = '',
  style,
  textStyle,
}) => {
  const getVariantStyles = (): string => {
    const base = 'px-6 py-3 rounded-lg items-center justify-center';
    const disabledStyle = disabled ? 'opacity-50' : '';

    let variantStyle = '';
    switch (variant) {
      case 'primary':
        variantStyle = 'bg-blue-600';
        break;
      case 'secondary':
        variantStyle = 'bg-gray-600';
        break;
      case 'danger':
        variantStyle = 'bg-red-600';
        break;
      default:
        variantStyle = 'bg-blue-600';
    }

    return `${base} ${variantStyle} ${disabledStyle} ${className}`.trim();
  };

  const getTextStyles = (): string => {
    const base = 'text-white font-semibold text-center';
    return `${base}`;
  };

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled || loading}
      className={getVariantStyles()}
      style={style}
      activeOpacity={0.7}
    >
      {loading ? (
        <ActivityIndicator color="#ffffff" />
      ) : (
        <Text className={getTextStyles()} style={textStyle}>
          {title}
        </Text>
      )}
    </TouchableOpacity>
  );
};

export default Button;
