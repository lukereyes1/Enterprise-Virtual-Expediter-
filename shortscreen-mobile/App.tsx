/**
 * ShortScreen Command - Mobile App Entry Point
 */

import React from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Ionicons } from '@expo/vector-icons';

// Screens
import HomeScreen from './src/screens/HomeScreen';
// Import other screens as they're created
// import AlertsScreen from './src/screens/AlertsScreen';
// import ThemesScreen from './src/screens/ThemesScreen';
// import WatchlistsScreen from './src/screens/WatchlistsScreen';
// import SettingsScreen from './src/screens/SettingsScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          switch (route.name) {
            case 'Home':
              iconName = focused ? 'home' : 'home-outline';
              break;
            case 'Alerts':
              iconName = focused ? 'notifications' : 'notifications-outline';
              break;
            case 'Themes':
              iconName = focused ? 'stats-chart' : 'stats-chart-outline';
              break;
            case 'Watchlists':
              iconName = focused ? 'star' : 'star-outline';
              break;
            case 'Settings':
              iconName = focused ? 'settings' : 'settings-outline';
              break;
            default:
              iconName = 'help-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#3B82F6',
        tabBarInactiveTintColor: '#9CA3AF',
        headerShown: false,
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      {/* Uncomment as screens are created */}
      {/* <Tab.Screen name="Alerts" component={AlertsScreen} /> */}
      {/* <Tab.Screen name="Themes" component={ThemesScreen} /> */}
      {/* <Tab.Screen name="Watchlists" component={WatchlistsScreen} /> */}
      {/* <Tab.Screen name="Settings" component={SettingsScreen} /> */}
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen name="Main" component={MainTabs} />
          {/* Add modal screens as created */}
          {/* <Stack.Screen name="TickerDetail" component={TickerDetailScreen} /> */}
          {/* <Stack.Screen name="ThemeDetail" component={ThemeDetailScreen} /> */}
        </Stack.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
