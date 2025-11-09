/**
 * Home/Dashboard Screen
 * One-glance view of model state
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  RefreshControl,
  TouchableOpacity,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import api from '../api/client';
import ThemeTile from '../components/ThemeTile';
import EventCard from '../components/EventCard';
import type { StatusResponse, Event } from '../types';

const HomeScreen: React.FC = () => {
  const navigation = useNavigation();
  const [status, setStatus] = useState<StatusResponse | null>(null);
  const [recentEvents, setRecentEvents] = useState<Event[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [statusData, eventsData] = await Promise.all([
        api.getStatus(),
        api.getEvents({ limit: 5, type: 'recent' }),
      ]);

      setStatus(statusData);
      setRecentEvents(eventsData.events);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  const getRegimeColor = (status: string) => {
    switch (status) {
      case 'risk_off':
        return '#EF4444';
      case 'neutral':
        return '#F59E0B';
      case 'risk_on':
        return '#10B981';
      default:
        return '#6B7280';
    }
  };

  const getRegimeLabel = (status: string) => {
    switch (status) {
      case 'risk_off':
        return 'Risk-Off';
      case 'neutral':
        return 'Neutral';
      case 'risk_on':
        return 'Risk-On';
      default:
        return 'Unknown';
    }
  };

  if (loading || !status) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>ShortScreen Command</Text>
      </View>

      {/* Global Regime Card */}
      <View style={styles.regimeCard}>
        <Text style={styles.sectionLabel}>GLOBAL REGIME</Text>
        <View style={styles.regimeContent}>
          <View style={styles.regimeStatus}>
            <View
              style={[
                styles.regimeIndicator,
                { backgroundColor: getRegimeColor(status.regime.status) },
              ]}
            />
            <Text style={styles.regimeLabel}>
              {getRegimeLabel(status.regime.status)}
            </Text>
          </View>
          <Text style={styles.regimeSubtext}>
            Based on beta, leverage, stress scores
          </Text>

          {/* Score Bar */}
          <View style={styles.scoreBarContainer}>
            <View
              style={[
                styles.scoreBar,
                {
                  width: `${status.regime.risk_off_score * 100}%`,
                  backgroundColor: getRegimeColor(status.regime.status),
                },
              ]}
            />
          </View>
          <Text style={styles.scoreValue}>
            {(status.regime.risk_off_score * 100).toFixed(0)}
          </Text>
        </View>
      </View>

      {/* Theme Heatmap */}
      <View style={styles.section}>
        <Text style={styles.sectionLabel}>THEME HEATMAP</Text>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.themesScroll}
          contentContainerStyle={styles.themesContent}
        >
          {status.themes.map((theme) => (
            <ThemeTile
              key={theme.name}
              theme={theme}
              onPress={() =>
                navigation.navigate('ThemeDetail', { themeName: theme.name })
              }
            />
          ))}
        </ScrollView>
      </View>

      {/* Top Signals */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionLabel}>TOP SIGNALS</Text>
          <TouchableOpacity
            onPress={() => navigation.navigate('Alerts')}
          >
            <Text style={styles.viewAll}>View All →</Text>
          </TouchableOpacity>
        </View>

        {recentEvents.map((event) => (
          <EventCard
            key={event.id}
            event={event}
            onPress={() =>
              navigation.navigate('EventDetail', { eventId: event.id })
            }
          />
        ))}
      </View>

      {/* View Report Button */}
      <TouchableOpacity style={styles.reportButton}>
        <Text style={styles.reportButtonText}>View Full Report</Text>
      </TouchableOpacity>

      <View style={styles.footer} />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F9FAFB',
  },
  header: {
    backgroundColor: '#FFFFFF',
    padding: 20,
    paddingTop: 60,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: '#111827',
  },
  section: {
    marginTop: 24,
    marginBottom: 8,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    marginBottom: 12,
  },
  sectionLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: '#6B7280',
    letterSpacing: 1,
    marginBottom: 12,
    paddingHorizontal: 16,
  },
  viewAll: {
    fontSize: 14,
    fontWeight: '600',
    color: '#3B82F6',
  },
  regimeCard: {
    backgroundColor: '#FFFFFF',
    margin: 16,
    marginTop: 0,
    padding: 20,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E5E7EB',
  },
  regimeContent: {
    marginTop: 8,
  },
  regimeStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  regimeIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  regimeLabel: {
    fontSize: 20,
    fontWeight: '700',
    color: '#111827',
  },
  regimeSubtext: {
    fontSize: 13,
    color: '#6B7280',
    marginBottom: 16,
  },
  scoreBarContainer: {
    height: 24,
    backgroundColor: '#E5E7EB',
    borderRadius: 12,
    overflow: 'hidden',
    marginBottom: 8,
  },
  scoreBar: {
    height: '100%',
    borderRadius: 12,
  },
  scoreValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    textAlign: 'right',
  },
  themesScroll: {
    paddingLeft: 16,
  },
  themesContent: {
    paddingRight: 16,
  },
  reportButton: {
    backgroundColor: '#3B82F6',
    marginHorizontal: 16,
    marginTop: 24,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  reportButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  footer: {
    height: 40,
  },
});

export default HomeScreen;
