# MRF103 Mobile App - Design Document

## Overview
MRF103 is a full-stack mobile application built with React Native, Expo, and integrated with Supabase for backend services. The app is designed for iOS and Android platforms with a focus on clean, intuitive user experience following Apple's Human Interface Guidelines.

## Screen List

1. **Home Screen** - Main dashboard showing app overview and quick actions
2. **Profile Screen** - User profile management and settings
3. **Settings Screen** - App configuration and preferences
4. **Auth Screen** - User authentication (login/signup)
5. **Loading Screen** - Initial app load state

## Primary Content and Functionality

### Home Screen
- **Content**: Welcome message, quick action buttons, recent activity feed
- **Functionality**: 
  - Display user's name if authenticated
  - Quick navigation to main features
  - Pull-to-refresh capability
  - Real-time data sync from Supabase

### Profile Screen
- **Content**: User avatar, name, email, bio, preferences
- **Functionality**:
  - View and edit profile information
  - Upload profile picture
  - Manage account settings
  - Logout option

### Settings Screen
- **Content**: App preferences, notification settings, theme toggle
- **Functionality**:
  - Toggle dark/light mode
  - Notification preferences
  - App version information
  - Clear cache option

### Auth Screen
- **Content**: Login form with email/password fields, signup link
- **Functionality**:
  - Email/password authentication via Supabase
  - OAuth integration (optional)
  - Password reset flow
  - Form validation

### Loading Screen
- **Content**: App logo, loading indicator
- **Functionality**:
  - Check authentication status on app startup
  - Load initial data from Supabase
  - Route to appropriate screen based on auth state

## Key User Flows

### New User Flow
1. User opens app → Loading Screen
2. Loading Screen detects no auth token → Auth Screen
3. User enters email/password → Supabase signup
4. Success → Home Screen
5. User can navigate to Profile or Settings

### Returning User Flow
1. User opens app → Loading Screen
2. Loading Screen detects valid auth token → Home Screen
3. User can access Profile, Settings, or main features
4. User can logout → Auth Screen

### Profile Update Flow
1. User taps Profile tab → Profile Screen
2. User edits name/bio → Saves to Supabase
3. Success notification → Profile updated
4. Changes sync across devices

## Color Choices

### Primary Brand Colors
- **Primary Accent**: #0a7ea4 (Teal blue - main interactive elements)
- **Background**: #ffffff (Light mode), #151718 (Dark mode)
- **Surface**: #f5f5f5 (Light mode), #1e2022 (Dark mode)
- **Text Primary**: #11181C (Light mode), #ECEDEE (Dark mode)
- **Text Secondary**: #687076 (Light mode), #9BA1A6 (Dark mode)

### Status Colors
- **Success**: #22C55E (Green - confirmations, success states)
- **Warning**: #F59E0B (Amber - warnings, cautions)
- **Error**: #EF4444 (Red - errors, destructive actions)

### Borders & Dividers
- **Border**: #E5E7EB (Light mode), #334155 (Dark mode)

## Typography

- **Display**: 32px, bold (app title, main headings)
- **Heading**: 24px, semibold (screen titles)
- **Subheading**: 18px, semibold (section headers)
- **Body**: 16px, regular (main content)
- **Caption**: 12px, regular (secondary info, timestamps)

## Layout Principles

- **Safe Area**: All content respects notch and home indicator areas
- **Spacing**: 4px grid system (4, 8, 12, 16, 24, 32px)
- **Tab Bar**: Fixed at bottom with 4-5 main navigation items
- **Modals**: Full-screen or sheet-style for secondary flows
- **Lists**: Use FlatList for performance, never ScrollView with .map()

## Interaction Patterns

- **Button Press**: Scale 0.97 + light haptic feedback
- **List Item Press**: Opacity 0.7 on press
- **Toggle**: Medium haptic feedback on state change
- **Loading**: Subtle spinner, no blocking UI
- **Errors**: Toast notification with error message and retry option

## Responsive Design

- **Portrait**: Primary orientation (9:16 aspect ratio)
- **Tablet**: Supported with adjusted layouts
- **Web**: Responsive design for testing
- **Dark Mode**: Automatic theme switching based on system preference

## Accessibility

- **Text**: Minimum 16px for body text
- **Touch Targets**: Minimum 44x44pt for interactive elements
- **Contrast**: WCAG AA compliant color combinations
- **Labels**: All interactive elements have descriptive labels
- **Haptics**: Used for critical feedback, can be disabled in settings

## Performance Considerations

- **Code Splitting**: Lazy load screens via Expo Router
- **Image Optimization**: Use expo-image for efficient loading
- **Data Fetching**: React Query for caching and background sync
- **Storage**: AsyncStorage for local persistence, Supabase for cloud sync
- **Bundle Size**: Monitor and optimize with tree-shaking

## Backend Integration

- **Authentication**: Supabase Auth with email/password
- **Database**: PostgreSQL via Supabase
- **Real-time**: Supabase Realtime for live data sync
- **File Storage**: Supabase Storage for user uploads
- **API**: tRPC for type-safe server communication

## Future Enhancements

- Push notifications via Expo Notifications
- Offline-first architecture with local sync queue
- Advanced analytics and crash reporting
- Biometric authentication (Face ID, Touch ID)
- Social sharing capabilities
- In-app messaging and support chat
