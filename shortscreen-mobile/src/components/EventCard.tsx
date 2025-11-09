/**
 * Event/alert card for activity feed
 */

import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { formatDistanceToNow } from 'date-fns';
import type { Event } from '../types';

interface Props {
  event: Event;
  onPress: () => void;
}

const EventCard: React.FC<Props> = ({ event, onPress }) => {
  const getIcon = (type: string) => {
    switch (type) {
      case 'regime_change':
        return '🔴';
      case 'theme_spike':
        return '🔵';
      case 'ticker_alert':
        return '⭐';
      case 'system_alert':
        return '⚠️';
      default:
        return '🔔';
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'regime_change':
        return 'REGIME';
      case 'theme_spike':
        return 'THEME';
      case 'ticker_alert':
        return 'TICKER';
      case 'system_alert':
        return 'SYSTEM';
      default:
        return 'EVENT';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'regime_change':
        return '#EF4444';
      case 'theme_spike':
        return '#3B82F6';
      case 'ticker_alert':
        return '#F59E0B';
      case 'system_alert':
        return '#DC2626';
      default:
        return '#6B7280';
    }
  };

  const timeAgo = formatDistanceToNow(new Date(event.created_at), {
    addSuffix: true,
  });

  return (
    <TouchableOpacity
      style={[
        styles.container,
        !event.read && styles.unread,
      ]}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <View style={styles.iconContainer}>
        <Text style={styles.icon}>{getIcon(event.type)}</Text>
      </View>

      <View style={styles.content}>
        <View style={styles.header}>
          <View
            style={[
              styles.typeTag,
              { backgroundColor: getTypeColor(event.type) + '20' },
            ]}
          >
            <Text
              style={[styles.typeText, { color: getTypeColor(event.type) }]}
            >
              {getTypeLabel(event.type)}
            </Text>
          </View>
          <Text style={styles.time}>{timeAgo}</Text>
        </View>

        <Text style={styles.title} numberOfLines={2}>
          {event.title}
        </Text>

        <Text style={styles.body} numberOfLines={2}>
          {event.body}
        </Text>
      </View>

      {!event.read && <View style={styles.unreadIndicator} />}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: '#FFFFFF',
    padding: 16,
    marginHorizontal: 16,
    marginBottom: 8,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E5E7EB',
  },
  unread: {
    backgroundColor: '#F0F9FF',
    borderColor: '#3B82F6',
  },
  iconContainer: {
    marginRight: 12,
  },
  icon: {
    fontSize: 24,
  },
  content: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 6,
  },
  typeTag: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    marginRight: 8,
  },
  typeText: {
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  time: {
    fontSize: 12,
    color: '#9CA3AF',
  },
  title: {
    fontSize: 15,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 4,
  },
  body: {
    fontSize: 14,
    color: '#6B7280',
    lineHeight: 18,
  },
  unreadIndicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#3B82F6',
    position: 'absolute',
    right: 16,
    top: 20,
  },
});

export default EventCard;
