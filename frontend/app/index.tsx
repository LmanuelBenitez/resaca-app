import "./global.css";
import { StatusBar } from "expo-status-bar";
import { Linking, Text, View } from "react-native";

export default function HomeScreen() {
  return (
    <View className="flex-1 bg-black px-6">
      <View className="flex-1 items-center justify-center">
        <View className="mb-8 rounded-full border border-cyan-400/20 bg-cyan-400/10 px-4 py-2">
          <Text className="text-xs font-semibold uppercase tracking-[0.35em] text-cyan-300">
            Powered by Expo + NativeWind
          </Text>
        </View>

        <Text className="text-center text-4xl font-black tracking-tight text-white">
          create-expo-nativewind
        </Text>

        <Text className="mt-4 max-w-md text-center text-base leading-6 text-zinc-400">
          A professional Expo starter with NativeWind, TypeScript, and a clean
          launch experience designed to help you start fast.
        </Text>
      </View>

      <View className="pb-8">
        <Text className="text-center text-sm text-zinc-500">
          Developed by{" "}
          <Text
            onPress={() => Linking.openURL("https://github.com/imprince26")}
            className="font-semibold text-white underline"
          >
            Prince Patel
          </Text>
        </Text>
      </View>

      <StatusBar style="light" />
    </View>
  );
}
