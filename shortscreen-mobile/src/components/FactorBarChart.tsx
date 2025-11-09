/**
 * Factor scores displayed as horizontal bar chart
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import type { FactorScores } from '../types';

interface Props {
  scores: FactorScores;
  height?: number;
}

interface FactorBar {
  label: string;
  value: number;
  color: string;
}

const FactorBarChart: React.FC<Props> = ({ scores, height = 200 }) => {
  const factors: FactorBar[] = [
    { label: 'Leverage', value: scores.leverage, color: '#EF4444' },
    { label: 'Valuation', value: scores.valuation, color: '#F59E0B' },
    { label: 'Beta', value: scores.beta, color: '#10B981' },
    { label: 'Quality', value: scores.quality, color: '#3B82F6' },
    { label: 'Growth', value: scores.growth, color: '#6366F1' },
    { label: 'Duration', value: scores.duration, color: '#8B5CF6' },
  ];

  return (
    <View style={styles.container}>
      {factors.map((factor) => (
        <View key={factor.label} style={styles.row}>
          <Text style={styles.label}>{factor.label}</Text>
          <View style={styles.barContainer}>
            <View
              style={[
                styles.bar,
                {
                  width: `${factor.value}%`,
                  backgroundColor: factor.color,
                },
              ]}
            />
          </View>
          <Text style={styles.value}>{factor.value.toFixed(0)}</Text>
        </View>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingVertical: 8,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  label: {
    width: 90,
    fontSize: 14,
    fontWeight: '500',
    color: '#374151',
  },
  barContainer: {
    flex: 1,
    height: 20,
    backgroundColor: '#E5E7EB',
    borderRadius: 10,
    overflow: 'hidden',
    marginHorizontal: 8,
  },
  bar: {
    height: '100%',
    borderRadius: 10,
  },
  value: {
    width: 35,
    fontSize: 14,
    fontWeight: '600',
    color: '#111827',
    textAlign: 'right',
  },
});

export default FactorBarChart;
