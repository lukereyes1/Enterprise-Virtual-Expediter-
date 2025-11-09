/**
 * Theme tile showing score, trend, and count
 */

import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import type { ThemeSummary } from '../types';

interface Props {
  theme: ThemeSummary;
  onPress: () => void;
}

const ThemeTile: React.FC<Props> = ({ theme, onPress }) => {
  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return '↗️';
      case 'down':
        return '↘️';
      default:
        return '→';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 75) return '#EF4444'; // High - Red
    if (score >= 50) return '#F59E0B'; // Medium - Orange
    return '#10B981'; // Low - Green
  };

  return (
    <TouchableOpacity
      style={styles.container}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <View style={styles.header}>
        <Text style={styles.title} numberOfLines={2}>
          {theme.display_name}
        </Text>
      </View>

      <View style={styles.scoreContainer}>
        <Text style={[styles.score, { color: getScoreColor(theme.score) }]}>
          {theme.score.toFixed(0)}
        </Text>
        <Text style={styles.trend}>{getTrendIcon(theme.trend)}</Text>
      </View>

      <Text style={styles.count}>{theme.top_decile_count} names</Text>

      {theme.score_change_24h !== 0 && (
        <View style={styles.changeContainer}>
          <Text
            style={[
              styles.change,
              {
                color: theme.score_change_24h > 0 ? '#EF4444' : '#10B981',
              },
            ]}
          >
            {theme.score_change_24h > 0 ? '+' : ''}
            {theme.score_change_24h.toFixed(0)} (24h)
          </Text>
        </View>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginRight: 12,
    width: 160,
    borderWidth: 1,
    borderColor: '#E5E7EB',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  header: {
    marginBottom: 12,
    height: 40,
  },
  title: {
    fontSize: 14,
    fontWeight: '600',
    color: '#111827',
    lineHeight: 18,
  },
  scoreContainer: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginBottom: 8,
  },
  score: {
    fontSize: 32,
    fontWeight: '700',
    marginRight: 6,
  },
  trend: {
    fontSize: 20,
  },
  count: {
    fontSize: 13,
    color: '#6B7280',
    marginBottom: 4,
  },
  changeContainer: {
    marginTop: 4,
  },
  change: {
    fontSize: 12,
    fontWeight: '600',
  },
});

export default ThemeTile;
