/**
 * Type-safe API client for ShortScreen backend
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type {
  StatusResponse,
  EventsResponse,
  ThemeDetail,
  ThemeNamesResponse,
  ThemeHistoryResponse,
  TickerDetail,
  TickerHistoryResponse,
  WatchlistsResponse,
  Watchlist,
  UserPreferences,
  User,
} from '../types';

const API_BASE_URL = __DEV__
  ? 'http://localhost:8000/api/v1'
  : 'https://api.shortscreen.com/v1';

class APIClient {
  private client: AxiosInstance;
  private authToken: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      async (config) => {
        if (!this.authToken) {
          this.authToken = await AsyncStorage.getItem('auth_token');
        }

        if (this.authToken) {
          config.headers.Authorization = `Bearer ${this.authToken}`;
        }

        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Token expired, clear and redirect to login
          await this.clearAuth();
          // Navigate to login screen (implement based on navigation)
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication

  async setAuthToken(token: string): Promise<void> {
    this.authToken = token;
    await AsyncStorage.setItem('auth_token', token);
  }

  async clearAuth(): Promise<void> {
    this.authToken = null;
    await AsyncStorage.removeItem('auth_token');
  }

  // Status & Dashboard

  async getStatus(): Promise<StatusResponse> {
    const response = await this.client.get<StatusResponse>('/status');
    return response.data;
  }

  // Events

  async getEvents(params?: {
    days?: number;
    type?: string;
    unread?: boolean;
    page?: number;
  }): Promise<EventsResponse> {
    const response = await this.client.get<EventsResponse>('/events', {
      params,
    });
    return response.data;
  }

  async getEvent(eventId: string): Promise<Event> {
    const response = await this.client.get<Event>(`/events/${eventId}`);
    return response.data;
  }

  async markEventRead(eventId: string): Promise<void> {
    await this.client.post(`/events/${eventId}/read`);
  }

  // Themes

  async getThemes(): Promise<ThemeDetail[]> {
    const response = await this.client.get<ThemeDetail[]>('/themes');
    return response.data;
  }

  async getTheme(themeName: string): Promise<ThemeDetail> {
    const response = await this.client.get<ThemeDetail>(`/themes/${themeName}`);
    return response.data;
  }

  async getThemeNames(
    themeName: string,
    params?: { sort?: string; limit?: number }
  ): Promise<ThemeNamesResponse> {
    const response = await this.client.get<ThemeNamesResponse>(
      `/themes/${themeName}/names`,
      { params }
    );
    return response.data;
  }

  async getThemeHistory(
    themeName: string,
    days: number = 30
  ): Promise<ThemeHistoryResponse> {
    const response = await this.client.get<ThemeHistoryResponse>(
      `/themes/${themeName}/history`,
      { params: { days } }
    );
    return response.data;
  }

  // Tickers

  async getTicker(ticker: string): Promise<TickerDetail> {
    const response = await this.client.get<TickerDetail>(`/tickers/${ticker}`);
    return response.data;
  }

  async getTickerHistory(
    ticker: string,
    days: number = 30
  ): Promise<TickerHistoryResponse> {
    const response = await this.client.get<TickerHistoryResponse>(
      `/tickers/${ticker}/history`,
      { params: { days } }
    );
    return response.data;
  }

  // Watchlists

  async getWatchlists(): Promise<WatchlistsResponse> {
    const response = await this.client.get<WatchlistsResponse>('/watchlists');
    return response.data;
  }

  async createWatchlist(data: {
    name: string;
    description?: string;
    alert_settings?: Partial<AlertSettings>;
  }): Promise<Watchlist> {
    const response = await this.client.post<Watchlist>('/watchlists', data);
    return response.data;
  }

  async getWatchlist(watchlistId: string): Promise<Watchlist> {
    const response = await this.client.get<Watchlist>(
      `/watchlists/${watchlistId}`
    );
    return response.data;
  }

  async updateWatchlistSettings(
    watchlistId: string,
    settings: Partial<AlertSettings>
  ): Promise<void> {
    await this.client.put(`/watchlists/${watchlistId}/settings`, settings);
  }

  async addTickerToWatchlist(
    watchlistId: string,
    ticker: string
  ): Promise<void> {
    await this.client.post(`/watchlists/${watchlistId}/tickers`, { ticker });
  }

  async removeTickerFromWatchlist(
    watchlistId: string,
    ticker: string
  ): Promise<void> {
    await this.client.delete(`/watchlists/${watchlistId}/tickers/${ticker}`);
  }

  async deleteWatchlist(watchlistId: string): Promise<void> {
    await this.client.delete(`/watchlists/${watchlistId}`);
  }

  // User & Preferences

  async getUser(): Promise<User> {
    const response = await this.client.get<User>('/users/me');
    return response.data;
  }

  async getPreferences(): Promise<UserPreferences> {
    const response = await this.client.get<UserPreferences>(
      '/users/me/preferences'
    );
    return response.data;
  }

  async updatePreferences(
    preferences: Partial<UserPreferences>
  ): Promise<void> {
    await this.client.put('/users/me/preferences', preferences);
  }

  // Push Notifications

  async registerPushToken(token: string, platform: 'ios' | 'android'): Promise<void> {
    await this.client.post('/users/me/push-token', {
      token,
      platform,
    });
  }
}

// Export singleton instance
export const api = new APIClient();
export default api;
