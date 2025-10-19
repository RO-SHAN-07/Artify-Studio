# Artify Studio - Screen Inventory

## 1. Screen Architecture Overview

### 1.1 Core Screen Structure

Artify Studio implements a comprehensive 7-screen architecture designed for optimal user experience across all platforms:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Artify Studio Screens                          │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Splash    │  │    Home     │  │Conversion   │  │  Output     │    │
│  │   Screen    │  │   Screen    │  │   Type      │  │  Preview    │    │
│  │             │  │             │  │  Screen     │  │  Screen     │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │  Settings   │  │ My Creations│  │   Profile   │                     │
│  │   Screen    │  │   Screen    │  │   Screen    │                     │
│  └─────────────┘  └─────────────┘  └─────────────┘                     │
├─────────────────────────────────────────────────────────────────────────┤
│                    Navigation & State Management                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │ Bottom Nav  │  │  Hamburger  │  │   Drawer    │                     │
│  │  (Mobile)   │  │   Menu      │  │   Menu      │                     │
│  │             │  │  (Web)      │  │  (Mobile)    │                     │
│  └─────────────┘  └─────────────┘  └─────────────┘                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Navigation Flow Architecture

#### Primary User Journey
```
Splash Screen → Home Screen → Conversion Type Selection → Output Preview → Export/Save
      ↑              ↓                    ↓              ↓              ↓
      ←←←←←←←←←← Settings ←←←←←←←←←←←←←←← Profile ←←←←←←←←←←←←←←←←←←←←←←
```

#### Secondary Navigation Patterns
- **Bottom Navigation Bar**: Mobile platforms (Android/iOS) - Primary navigation
- **Hamburger Drawer Menu**: Web platform - Secondary navigation and settings access
- **Tab-based Navigation**: Settings and Profile screens with sub-navigation
- **Breadcrumb Navigation**: Output Preview with back navigation to previous screens

## 2. Material 3 Design System Implementation

### 2.1 Design Tokens and Color System

#### Primary Color Palette
```css
/* Material 3 Color Tokens */
--md-sys-color-primary: #1976D2;          /* Primary brand color */
--md-sys-color-on-primary: #FFFFFF;       /* Text on primary */
--md-sys-color-primary-container: #D3E4FD; /* Primary container */
--md-sys-color-on-primary-container: #001B3E; /* Text on primary container */

--md-sys-color-secondary: #565F71;        /* Secondary elements */
--md-sys-color-on-secondary: #FFFFFF;     /* Text on secondary */
--md-sys-color-tertiary: #705575;         /* Accent elements */
--md-sys-color-surface: #FEFBFF;          /* Main surface color */

--md-sys-color-background: #FEFBFF;       /* App background */
--md-sys-color-on-background: #1A1C1E;    /* Primary text */
--md-sys-color-surface-variant: #DDE3EA;  /* Alternative surface */
--md-sys-color-outline: #757B85;          /* Borders and dividers */
```

#### Typography Scale (Material 3)
```css
/* Display Scale */
--md-sys-typescale-display-large: 57px / 64px (Roboto, Medium)
--md-sys-typescale-display-medium: 45px / 52px (Roboto, Medium)
--md-sys-typescale-display-small: 36px / 44px (Roboto, Medium)

/* Headline Scale */
--md-sys-typescale-headline-large: 32px / 40px (Roboto, Regular)
--md-sys-typescale-headline-medium: 28px / 36px (Roboto, Regular)
--md-sys-typescale-headline-small: 24px / 32px (Roboto, Regular)

/* Body Scale */
--md-sys-typescale-body-large: 16px / 24px (Roboto, Regular)
--md-sys-typescale-body-medium: 14px / 20px (Roboto, Regular)
--md-sys-typescale-body-small: 12px / 16px (Roboto, Regular)

/* Label Scale */
--md-sys-typescale-label-large: 14px / 20px (Roboto, Medium)
--md-sys-typescale-label-medium: 12px / 16px (Roboto, Medium)
--md-sys-typescale-label-small: 11px / 16px (Roboto, Medium)
```

### 2.2 Component Mapping Matrix

| Material 3 Component | Streamlit Implementation | Kivy Implementation | Purpose |
|---------------------|------------------------|-------------------|---------|
| **Navigation Bar** | `st.navigation` | `MDNavigationBar` | Primary mobile navigation |
| **Navigation Drawer** | Custom sidebar | `MDNavigationDrawer` | Web secondary navigation |
| **Card** | `st.container` | `MDCard` | Content containers |
| **Button** | `st.button` | `MDRaisedButton` | Primary actions |
| **Icon Button** | Custom component | `MDIconButton` | Icon-only actions |
| **Text Field** | `st.text_input` | `MDTextField` | User input |
| **Slider** | `st.slider` | `MDSlider` | Parameter adjustment |
| **Chip** | Custom badges | `MDChip` | Filter and selection |
| **Progress Indicator** | `st.progress` | `MDCircularProgressIndicator` | Loading states |
| **Dialog** | `st.dialog` | `MDDialog` | Modal interactions |
| **Snackbar** | Custom toast | `MDSnackbar` | Notifications |
| **Bottom Sheet** | Custom modal | `MDBottomSheet` | Action menus |

## 3. Screen-by-Screen Design Blueprint

### 3.1 Splash Screen

#### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│                  Splash Screen Layout                   │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐  │
│  │                Logo Container                       │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │           Artify Studio                     │    │  │
│  │  │        ┌─────────────┐                      │    │  │
│  │  │        │    LOGO     │  Large Icon (128dp)  │    │  │
│  │  │        └─────────────┘                      │    │  │
│  │  │         Loading Animation                   │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  │                                                 │    │  │
│  │            Progress Indicator                   │    │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │     Linear Progress Bar (Indeterminate)     │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  │                                                 │    │  │
│  │             Version Info & Status               │    │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Version 1.0.0  |  Loading Resources...     │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

#### Component Specifications
- **Logo Animation**: Scale and fade-in animation (300ms duration)
- **Progress Indicator**: Material 3 Linear Progress Indicator (indeterminate)
- **Background**: Gradient background with subtle brand colors
- **Typography**: Display Medium for app name, Body Small for version info

#### State Management
- **Loading States**: Resource initialization, library loading, cache validation
- **Error Handling**: Network connectivity, corrupted resources, insufficient storage
- **Transition Logic**: Auto-advance to Home screen after successful initialization

#### Platform Adaptations
- **Web**: Full-screen centered layout with responsive sizing
- **Mobile**: Status bar integration with immersive mode support
- **Animation**: 60fps smooth animations with GPU acceleration

### 3.2 Home Screen

#### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│                   Home Screen Layout                    │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐  │
│  │              App Bar / Header                       │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Artify Studio  │         [Menu Icon]        │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Quick Actions Grid                     │  │
│  │  ┌─────────────┬─────────────┬─────────────┐       │  │
│  │  │ Pencil      │  Colored    │   OpenCV    │       │  │
│  │  │ Sketch      │   Sketch    │  Filters     │       │  │
│  │  │             │             │             │       │  │
│  │  │ [Icon]      │   [Icon]    │   [Icon]    │       │  │
│  │  └─────────────┴─────────────┴─────────────┘       │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Recent Creations                       │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Recent Work  │            [View All]        │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Horizontal Scrollable Gallery              │    │  │
│  │  │  [Image] [Image] [Image] [Image] [Image]    │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

#### Component Specifications
- **App Bar**: Material 3 Top App Bar with navigation icon and title
- **Quick Actions Grid**: 3-column grid with Material 3 Filled Cards
- **Recent Creations**: Horizontal scrollable list with image thumbnails
- **Navigation**: Hamburger menu integration for secondary actions

#### State Management
- **Gallery States**: Empty state, loading state, populated state, error state
- **Quick Actions**: Available, disabled during processing, loading states
- **Navigation State**: Active screen tracking and breadcrumb management

#### Platform Adaptations
- **Web**: Full-width layout with sidebar navigation drawer
- **Mobile**: Bottom navigation bar with tab indicators
- **Tablet**: Optimized layout for larger screens with multi-panel design

### 3.3 Conversion Type Screen

#### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│              Conversion Type Screen Layout              │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐  │
│  │              App Bar / Header                       │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Choose Transformation  │     [Back Icon]     │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Image Preview Area                     │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │         Selected Image Thumbnail            │    │  │
│  │  │  ┌─────────────────────────────────────┐     │    │  │
│  │  │  │         [Image Preview]             │     │    │  │
│  │  │  │        Original Image               │     │    │  │
│  │  │  └─────────────────────────────────────┘     │    │  │
│  │  │  [Change Image] [Image Info Button]          │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Transformation Options                 │  │
│  │  ┌─────────────┬─────────────┬─────────────┐       │  │
│  │  │ Pencil      │  Colored    │   Turtle    │       │  │
│  │  │ Sketch      │   Sketch    │  Graphics    │       │  │
│  │  │             │             │             │       │  │
│  │  │ [Icon]      │   [Icon]    │   [Icon]    │       │  │
│  │  │ Detailed    │   Detailed  │   Detailed  │       │  │
│  │  │ Options →   │   Options → │   Options → │       │  │
│  │  └─────────────┴─────────────┴─────────────┘       │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Action Buttons                         │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │         [Process Image]  [Save Draft]       │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

#### Component Specifications
- **Image Preview**: Interactive thumbnail with zoom and pan capabilities
- **Transformation Cards**: Material 3 Outlined Cards with icons and descriptions
- **Parameter Controls**: Collapsible sections with sliders and input fields
- **Action Buttons**: Material 3 Filled Button (primary) and Outlined Button (secondary)

#### State Management
- **Image States**: No image selected, image loading, image loaded, processing
- **Transformation States**: Option selection, parameter adjustment, preview generation
- **Validation States**: Input validation, processing capability checks

#### Platform Adaptations
- **Web**: Large preview area with detailed parameter controls
- **Mobile**: Compact layout with bottom sheet for advanced options
- **Touch Optimization**: Large touch targets (48dp minimum) for mobile interaction

### 3.4 Output Preview Screen

#### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│               Output Preview Screen Layout              │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐  │
│  │              App Bar / Header                       │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Preview Results  │  [Back] [Save] [Share]   │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Before/After Comparison                │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Before  │  After  │  [Comparison Toggle]    │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  │  ┌──────────────┬─────────────────────────────┐       │  │
│  │  │   Original   │      Transformed Image      │       │  │
│  │  │   [Image]    │         [Image]             │       │  │
│  │  │              │                             │       │  │
│  │  │              │  [Zoom] [Pan] [Rotate]      │       │  │
│  │  └──────────────┴─────────────────────────────┘       │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Export Options                         │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Format: PNG  │  Quality: 95%  │  Size: Auto │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Action Buttons                         │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │ [Export Image]  [Save to Creations] [Share] │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

#### Component Specifications
- **Image Comparison**: Side-by-side view with swipe or toggle functionality
- **Zoom Controls**: Pinch-to-zoom on mobile, zoom buttons on web
- **Export Panel**: Collapsible settings for format, quality, and sizing options
- **Action Bar**: Multiple action buttons with clear visual hierarchy

#### State Management
- **Preview States**: Loading, processing, ready, error
- **Comparison Modes**: Side-by-side, overlay, difference, toggle
- **Export States**: Format selection, quality adjustment, size optimization

#### Platform Adaptations
- **Web**: Full-screen preview with keyboard shortcuts for zoom and pan
- **Mobile**: Gesture-based interaction with haptic feedback
- **Performance**: Progressive image loading and adaptive quality

### 3.5 Settings Screen

#### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│                 Settings Screen Layout                  │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐  │
│  │              App Bar / Header                       │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │     Settings     │       [Back Icon]        │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              General Settings                       │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Theme  │  Language  │  Notifications       │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  [Dark Mode Toggle]  [English]  [On/Off]    │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Processing Settings                    │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Default Quality  │  Max Image Size        │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  [Quality Slider]   [Size Dropdown]        │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Storage & Cache                        │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Clear Cache  │  Storage Location         │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  [Clear Button]  [Location Info]           │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

#### Component Specifications
- **Settings List**: Material 3 List Items with icons and toggle switches
- **Sliders**: Material 3 Slider component for quality and size settings
- **Dropdowns**: Material 3 Dropdown Menu for selection options
- **Toggles**: Material 3 Switch component for boolean settings

#### State Management
- **Settings States**: Loading preferences, validating changes, saving settings
- **Validation**: Input validation for numeric settings and format selection
- **Persistence**: Real-time saving with backup and restore capabilities

#### Platform Adaptations
- **Web**: Scrollable layout with search functionality for settings
- **Mobile**: Sectioned layout with navigation between setting categories
- **Accessibility**: High contrast mode and screen reader optimization

### 3.6 My Creations Screen

#### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│              My Creations Screen Layout                 │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐  │
│  │              App Bar / Header                       │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │   My Creations   │   [Search] [Filter]      │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Filter & Sort Controls                 │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  [All] [Pencil] [Colored] [Turtle] [OpenCV] │    │  │
│  │  │  Sort: [Date] [Name] [Size] [Type]          │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Creations Grid                         │  │
│  │  ┌─────────────┬─────────────┬─────────────┐       │  │
│  │  │   [Image]   │   [Image]   │   [Image]   │       │  │
│  │  │  Pencil     │  Colored    │   OpenCV    │       │  │
│  │  │  Sketch     │   Sketch    │   Filter    │       │  │
│  │  │  2 days ago │  1 week ago │  3 days ago │       │  │
│  │  └─────────────┴─────────────┴─────────────┘       │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Empty State (when no creations)        │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  No creations yet                           │    │  │
│  │  │  [Start Creating] Button                    │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

#### Component Specifications
- **Filter Chips**: Material 3 Filter Chip group for transformation type filtering
- **Sort Dropdown**: Material 3 Dropdown Menu for sort options
- **Creations Grid**: Material 3 Image List with responsive grid layout
- **Image Cards**: Material 3 Cards with image, title, and metadata

#### State Management
- **Gallery States**: Empty, loading, populated, filtered, search results
- **Selection States**: Multi-select mode for batch operations
- **Filter States**: Active filters, sort order, search queries

#### Platform Adaptations
- **Web**: Multi-column grid with lazy loading and virtualization
- **Mobile**: Single/double column layout with infinite scroll
- **Performance**: Image thumbnail caching and progressive loading

### 3.7 Profile Screen

#### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│                 Profile Screen Layout                   │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐  │
│  │              App Bar / Header                       │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │     Profile      │       [Edit Icon]        │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              User Profile Info                      │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Avatar  │  User Details  │  Stats           │    │  │
│  │  │  [Image] │  Name: John    │  Creations: 47  │    │  │
│  │  │          │  Email: john@  │  Favorites: 12  │    │  │
│  │  │          │  Member since: │  Total Views:   │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              Account Settings                       │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Export Data  │  Privacy  │  Notifications  │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │              App Information                        │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │  Version  │  Help  │  About  │  Support       │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

#### Component Specifications
- **Profile Header**: Material 3 Card with avatar, name, and stats
- **Settings List**: Material 3 List Items with navigation arrows
- **Statistics Cards**: Material 3 Info Cards with metrics and trends
- **Action Buttons**: Material 3 Outlined Buttons for secondary actions

#### State Management
- **Profile States**: Loading, editing, saving, error
- **Data States**: Sync status, local vs cloud data, backup status
- **Privacy States**: Data sharing preferences, analytics opt-in status

#### Platform Adaptations
- **Web**: Detailed layout with comprehensive account management
- **Mobile**: Simplified layout with essential profile features
- **Privacy**: Platform-specific privacy controls and data management

## 4. Navigation Flow Diagrams

### 4.1 Primary User Journey Map

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Splash        │───▶│      Home       │───▶│ Conversion Type │
│   Screen        │    │    Screen       │    │    Screen       │
│                 │    │                 │    │                 │
│ • App Init      │    │ • Gallery View  │    │ • Select Image  │
│ • Load Resources│    │ • Quick Actions │    │ • Choose Type   │
│ • Check Updates │    │ • Recent Work   │    │ • Set Params    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Output Preview  │◀───│   Settings      │    │ My Creations    │
│    Screen       │    │    Screen       │    │    Screen       │
│                 │    │                 │    │                 │
│ • View Results  │    │ • App Prefs     │    │ • View Gallery  │
│ • Compare Images│    │ • Processing    │    │ • Filter & Sort │
│ • Export Options│    │ • Storage       │    │ • Manage Work   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Export      │    │     Profile     │    │     Share       │
│   & Save        │    │    Screen       │    │   Options       │
│                 │    │                 │    │                 │
│ • File Save     │    │ • User Info     │    │ • Social Media  │
│ • Format Choice │    │ • Account       │    │ • Export Options│
│ • Quality Set   │    │ • Preferences   │    │ • Link Generate │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 4.2 Navigation State Management

#### Screen State Transitions
- **Forward Navigation**: Splash → Home → Conversion Type → Output Preview → Export
- **Backward Navigation**: Output Preview → Conversion Type → Home (with state preservation)
- **Modal Navigation**: Settings and Profile accessible from all screens via drawer/menu
- **Contextual Navigation**: Deep linking to specific creations or transformation types

#### Breadcrumb Implementation
```typescript
interface BreadcrumbItem {
  label: string;
  screen: ScreenType;
  state?: any;
}

class NavigationManager {
  private breadcrumb: BreadcrumbItem[] = [];
  private currentScreen: ScreenType = ScreenType.SPLASH;

  navigateTo(screen: ScreenType, state?: any): void {
    // Preserve state for backward navigation
    this.breadcrumb.push({
      label: this.getScreenLabel(screen),
      screen: this.currentScreen,
      state: this.getCurrentState()
    });
    this.currentScreen = screen;
  }

  navigateBack(): boolean {
    if (this.breadcrumb.length > 0) {
      const previous = this.breadcrumb.pop()!;
      this.currentScreen = previous.screen;
      this.restoreState(previous.state);
      return true;
    }
    return false;
  }
}
```

## 5. Accessibility Requirements

### 5.1 WCAG 2.1 AA Compliance

#### Visual Accessibility
- **Color Contrast**: Minimum 4.5:1 ratio for normal text, 3:1 for large text
- **Focus Indicators**: Visible focus indicators for all interactive elements
- **Color Independence**: Information not conveyed by color alone
- **Text Scaling**: Support for 200% text scaling without horizontal scrolling

#### Motor Accessibility
- **Touch Targets**: Minimum 48x48dp touch targets for all interactive elements
- **Gesture Support**: Alternative input methods for complex gestures
- **Keyboard Navigation**: Full keyboard accessibility for all features
- **Switch Control**: Compatibility with iOS Switch Control and Android Switch Access

#### Cognitive Accessibility
- **Clear Navigation**: Consistent navigation patterns across all screens
- **Error Prevention**: Clear validation and prevention of data loss
- **Progress Indicators**: Clear indication of processing status and progress
- **Help Text**: Contextual help and instructions for complex features

### 5.2 Screen Reader Support

#### Semantic Structure
- **Heading Hierarchy**: Proper H1-H6 structure for screen organization
- **Landmark Regions**: Navigation, main content, and complementary content areas
- **List Structure**: Proper list markup for galleries and option lists
- **Button Labels**: Descriptive button labels with clear action intent

#### Dynamic Content
- **Live Regions**: ARIA live regions for dynamic content updates
- **Status Announcements**: Screen reader announcements for processing status
- **Error Messages**: Clear error descriptions with resolution suggestions
- **Progress Updates**: Accessible progress indicators with percentage completion

### 5.3 Platform-Specific Accessibility

#### Web Platform
- **Keyboard Shortcuts**: Standard shortcuts for common actions (Ctrl+S for save, etc.)
- **High Contrast Mode**: Windows High Contrast Mode support
- **Screen Reader Testing**: NVDA, JAWS, and VoiceOver compatibility
- **Browser Zoom**: Support for browser zoom up to 400%

#### Mobile Platforms
- **VoiceOver (iOS)**: Full VoiceOver gesture and navigation support
- **TalkBack (Android)**: Complete TalkBack screen reader integration
- **Voice Control**: Siri and Google Assistant voice command support
- **Dynamic Type**: iOS Dynamic Type and Android font scaling support

## 6. Responsive Design Specifications

### 6.1 Breakpoint System

#### Web Breakpoints
```css
/* Mobile First Approach */
--breakpoint-xs: 0px;      /* Extra small devices */
--breakpoint-sm: 600px;    /* Small tablets */
--breakpoint-md: 960px;    /* Medium tablets/desktop */
--breakpoint-lg: 1280px;   /* Large desktop */
--breakpoint-xl: 1920px;   /* Extra large desktop */
```

#### Layout Adaptations
- **Compact (0-599px)**: Single column, collapsed navigation, essential features only
- **Medium (600-959px)**: Two-column layout where appropriate, expanded navigation
- **Expanded (960px+)**: Multi-column layout, full feature set, advanced controls

### 6.2 Component Responsiveness

#### Grid System
```css
/* Responsive Grid Classes */
.grid-compact { display: grid; grid-template-columns: 1fr; }
.grid-medium { display: grid; grid-template-columns: repeat(2, 1fr); }
.grid-expanded { display: grid; grid-template-columns: repeat(3, 1fr); }
.grid-large { display: grid; grid-template-columns: repeat(4, 1fr); }
```

#### Typography Responsiveness
- **Fluid Typography**: Responsive font sizes using clamp() function
- **Line Height**: Adaptive line height for optimal readability
- **Letter Spacing**: Platform-appropriate letter spacing adjustments

### 6.3 Platform-Specific Responsive Patterns

#### Web Platform
- **Container Queries**: Component-based responsive design
- **Viewport Units**: Responsive sizing based on viewport dimensions
- **CSS Grid**: Advanced layout capabilities with fallback to Flexbox

#### Mobile Platforms
- **Orientation Support**: Landscape and portrait mode optimization
- **Safe Areas**: iOS notch and Android navigation bar accommodation
- **Split Screen**: iPad split-screen multitasking support

## 7. Component Interaction Specifications

### 7.1 Touch and Gesture System

#### Mobile Touch Gestures
- **Tap**: Primary interaction for buttons and selectable items
- **Long Press**: Contextual menus and secondary actions
- **Swipe**: Gallery navigation and image comparison
- **Pinch**: Zoom in/out on preview images
- **Pan**: Image positioning and transformation controls

#### Web Interaction Patterns
- **Click**: Primary mouse interaction
- **Right-click**: Context menus where appropriate
- **Mouse Wheel**: Zoom and scroll actions
- **Drag and Drop**: File selection and image positioning

### 7.2 State Management Architecture

#### Component State Types
```typescript
interface ComponentState {
  // UI State
  isLoading: boolean;
  isDisabled: boolean;
  isSelected: boolean;
  isFocused: boolean;

  // Data State
  data?: any;
  error?: Error;
  validationMessage?: string;

  // Interaction State
  isHovered?: boolean;
  isPressed?: boolean;
  isDragging?: boolean;
}
```

#### State Transition Management
- **Atomic Updates**: Individual state property updates
- **Batch Updates**: Multiple state changes in single update cycle
- **State Persistence**: Cross-session state preservation where appropriate
- **State Validation**: Input validation and error state management

### 7.3 Animation and Motion System

#### Animation Principles
- **Material 3 Motion**: Easing curves and duration guidelines
- **Performance**: 60fps animations with GPU acceleration
- **Accessibility**: Respects prefers-reduced-motion settings
- **Purposeful Animation**: Animation serves clear functional purpose

#### Animation Tokens
```css
/* Duration Tokens */
--motion-duration-short-1: 50ms;
--motion-duration-short-2: 100ms;
--motion-duration-short-3: 150ms;
--motion-duration-short-4: 200ms;
--motion-duration-medium-1: 250ms;
--motion-duration-medium-2: 300ms;
--motion-duration-long: 500ms;

/* Easing Tokens */
--motion-easing-linear: cubic-bezier(0, 0, 1, 1);
--motion-easing-standard: cubic-bezier(0.4, 0, 0.2, 1);
--motion-easing-decelerate: cubic-bezier(0, 0, 0, 1);
--motion-easing-accelerate: cubic-bezier(0.4, 0, 1, 1);
```

---

*Document Version: 1.0*
*Last Updated: October 2025*
*Author: Roshan*
*Project: Artify Studio (com.roshan.artifystudio)*