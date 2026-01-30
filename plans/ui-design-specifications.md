# SeaFood Dashboard - UI Design Specifications

## Design Philosophy

The SeaFood dashboard follows a **modern, clean, and professional** design approach with:
- **Spacious layouts** for easy scanning
- **Clear visual hierarchy** with typography and color
- **Consistent spacing** using 8px grid system
- **Subtle animations** for delightful interactions
- **Data-first approach** with emphasis on metrics and insights

## Color System

### Primary Palette
```
Primary Blue (#7C86F5)
├── Used for: Primary actions, active states, links
├── Hover: #5B67D8
└── Active: #4651B8

Secondary Lavender (#AFB5F7)
├── Used for: Secondary actions, highlights
├── Hover: #9BA2F6
└── Active: #8A92F5

Background (#E5E7F9)
├── Used for: Page background, subtle containers
└── Variant: #F5F6FE (lighter)
```

### Semantic Colors
```
Success: #10B981 (Green)
├── Completed, Paid, Active, Positive trends

Warning: #F59E0B (Amber)
├── Pending, In Transit, Warnings

Error: #EF4444 (Red)
├── Failed, Overdue, Errors, Negative trends

Info: #3B82F6 (Blue)
├── Created, Processing, Information
```

### Neutral Colors
```
Gray Scale:
├── 900: #111827 (Headings)
├── 800: #1F2937 (Body text)
├── 700: #374151 (Secondary text)
├── 600: #4B5563 (Muted text)
├── 500: #6B7280 (Placeholder)
├── 400: #9CA3AF (Disabled)
├── 300: #D1D5DB (Borders)
├── 200: #E5E7EB (Dividers)
├── 100: #F3F4F6 (Backgrounds)
└── 50: #F9FAFB (Subtle backgrounds)
```

## Typography System

### Font Families
```css
Headings: 'Poppins', sans-serif
Body: 'Inter', sans-serif
Monospace: 'JetBrains Mono', monospace
```

### Type Scale
```
Display: 48px / 3rem (Page titles)
H1: 40px / 2.5rem (Section headers)
H2: 32px / 2rem (Card titles)
H3: 24px / 1.5rem (Subsections)
H4: 20px / 1.25rem (Small headers)
H5: 18px / 1.125rem (Labels)
Body Large: 18px / 1.125rem
Body: 16px / 1rem (Default)
Body Small: 14px / 0.875rem (Secondary)
Caption: 12px / 0.75rem (Metadata)
```

### Font Weights
```
Regular: 400 (Body text)
Medium: 500 (Emphasis)
Semibold: 600 (Subheadings)
Bold: 700 (Headings)
```

### Line Heights
```
Tight: 1.25 (Headings)
Normal: 1.5 (Body)
Relaxed: 1.75 (Long-form content)
```

## Spacing System (8px Grid)

```
xs: 4px (0.25rem)
sm: 8px (0.5rem)
md: 16px (1rem)
lg: 24px (1.5rem)
xl: 32px (2rem)
2xl: 48px (3rem)
3xl: 64px (4rem)
4xl: 96px (6rem)
```

## Component Specifications

### 1. Sidebar Navigation

**Dimensions:**
- Width: 280px (expanded), 80px (collapsed)
- Height: 100vh
- Background: White (#FFFFFF)
- Border: 1px solid #E5E7EB (right)

**Logo Area:**
- Height: 64px
- Padding: 16px
- Logo size: 40px × 40px (icon), 160px × 40px (full)

**Navigation Items:**
- Height: 48px
- Padding: 12px 16px
- Border radius: 8px
- Gap between items: 4px
- Icon size: 20px × 20px
- Font: Inter 500, 14px

**States:**
```css
Default:
  background: transparent
  color: #6B7280

Hover:
  background: #F3F4F6
  color: #1F2937

Active:
  background: #E5E7F9
  color: #7C86F5
  border-left: 3px solid #7C86F5
```

**Navigation Groups:**
```
Main
├── Dashboard
├── Shipments
├── Products
└── Sales

Operations
├── Payments
├── Purchases
├── Costs
└── Logistics

Settings
├── Users
├── Currencies
└── Settings
```

### 2. Header

**Dimensions:**
- Height: 64px
- Background: White (#FFFFFF)
- Border: 1px solid #E5E7EB (bottom)
- Padding: 0 24px

**Layout (Left to Right):**
```
[Menu Toggle] [Breadcrumbs] [Spacer] [Search] [Notifications] [User Menu]
```

**Search Bar:**
- Width: 320px
- Height: 40px
- Border radius: 8px
- Background: #F3F4F6
- Placeholder: "Search..."
- Icon: Search (16px)

**User Menu:**
- Avatar: 40px × 40px (circle)
- Name: Inter 500, 14px
- Role: Inter 400, 12px, #6B7280

### 3. Stat Cards

**Dimensions:**
- Min height: 120px
- Padding: 24px
- Border radius: 12px
- Background: White
- Border: 1px solid #E5E7EB
- Shadow: 0 1px 3px rgba(0,0,0,0.1)

**Layout:**
```
┌─────────────────────────────┐
│ [Icon]          [Title]     │
│                             │
│ [Large Value]               │
│ [Trend] [Percentage]        │
└─────────────────────────────┘
```

**Elements:**
- Icon: 24px × 24px, top-right, #6B7280
- Title: Inter 500, 14px, #6B7280
- Value: Poppins 700, 32px, #1F2937
- Trend: Inter 400, 12px, Success/Error color

**Hover Effect:**
- Transform: translateY(-2px)
- Shadow: 0 4px 12px rgba(124,134,245,0.15)
- Transition: 200ms ease

### 4. Data Tables

**Header:**
- Height: 48px
- Background: #F9FAFB
- Border: 1px solid #E5E7EB (bottom)
- Font: Inter 600, 12px, uppercase, #6B7280
- Padding: 12px 16px

**Rows:**
- Height: 56px
- Border: 1px solid #E5E7EB (bottom)
- Font: Inter 400, 14px, #1F2937
- Padding: 16px

**States:**
```css
Default:
  background: white

Hover:
  background: #F9FAFB

Selected:
  background: #E5E7F9
  border-left: 3px solid #7C86F5
```

**Action Buttons:**
- Size: 32px × 32px
- Border radius: 6px
- Icon: 16px × 16px
- Gap: 8px

### 5. Buttons

**Primary Button:**
```css
height: 40px
padding: 0 24px
border-radius: 8px
background: #7C86F5
color: white
font: Inter 500, 14px
shadow: 0 1px 2px rgba(0,0,0,0.05)

hover:
  background: #5B67D8
  shadow: 0 4px 12px rgba(124,134,245,0.3)

active:
  background: #4651B8
```

**Secondary Button:**
```css
background: transparent
border: 1px solid #D1D5DB
color: #1F2937

hover:
  background: #F9FAFB
  border-color: #9CA3AF
```

**Sizes:**
- Small: 32px height, 16px padding
- Medium: 40px height, 24px padding (default)
- Large: 48px height, 32px padding

### 6. Form Inputs

**Text Input:**
```css
height: 40px
padding: 0 12px
border-radius: 8px
border: 1px solid #D1D5DB
background: white
font: Inter 400, 14px

focus:
  border-color: #7C86F5
  ring: 0 0 0 3px rgba(124,134,245,0.1)

error:
  border-color: #EF4444
  ring: 0 0 0 3px rgba(239,68,68,0.1)
```

**Select Dropdown:**
- Same as text input
- Chevron icon: 16px, right-aligned
- Dropdown: max-height 300px, scrollable

**Textarea:**
- Min height: 100px
- Padding: 12px
- Resize: vertical

**Checkbox/Radio:**
- Size: 20px × 20px
- Border radius: 4px (checkbox), 50% (radio)
- Checked: background #7C86F5

### 7. Cards

**Standard Card:**
```css
padding: 24px
border-radius: 12px
background: white
border: 1px solid #E5E7EB
shadow: 0 1px 3px rgba(0,0,0,0.1)
```

**Card Header:**
- Margin bottom: 16px
- Title: Poppins 600, 18px
- Subtitle: Inter 400, 14px, #6B7280

**Card Content:**
- Gap: 16px between elements

**Card Footer:**
- Margin top: 24px
- Border top: 1px solid #E5E7EB
- Padding top: 16px

### 8. Badges

**Status Badge:**
```css
height: 24px
padding: 0 12px
border-radius: 12px
font: Inter 500, 12px
display: inline-flex
align-items: center
gap: 4px
```

**Colors by Status:**
```
Success: bg-green-100, text-green-800
Warning: bg-yellow-100, text-yellow-800
Error: bg-red-100, text-red-800
Info: bg-blue-100, text-blue-800
Neutral: bg-gray-100, text-gray-800
```

### 9. Charts

**Container:**
- Min height: 300px
- Padding: 24px
- Background: white
- Border radius: 12px

**Chart Colors:**
```
Primary series: #7C86F5
Secondary series: #AFB5F7
Tertiary series: #10B981
Quaternary series: #F59E0B
Grid lines: #E5E7EB
Axis labels: #6B7280
```

**Legend:**
- Position: top-right
- Font: Inter 400, 12px
- Marker: 12px × 12px circle

### 10. Modals/Dialogs

**Overlay:**
```css
background: rgba(0,0,0,0.5)
backdrop-filter: blur(4px)
```

**Dialog:**
```css
max-width: 600px
border-radius: 16px
background: white
shadow: 0 20px 25px -5px rgba(0,0,0,0.1)
```

**Dialog Header:**
- Padding: 24px
- Border bottom: 1px solid #E5E7EB
- Title: Poppins 600, 20px

**Dialog Content:**
- Padding: 24px
- Max height: 60vh
- Overflow: auto

**Dialog Footer:**
- Padding: 24px
- Border top: 1px solid #E5E7EB
- Buttons: right-aligned, gap 12px

## Page Layouts

### Dashboard Overview Layout

```
┌─────────────────────────────────────────────────────────┐
│ Header (64px)                                           │
├──────┬──────────────────────────────────────────────────┤
│      │ Page Title + Breadcrumbs (80px)                  │
│      ├──────────────────────────────────────────────────┤
│ Side │ Stat Cards Grid (4 columns)                      │
│ bar  │ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐            │
│      │ │ Card │ │ Card │ │ Card │ │ Card │            │
│ 280  │ └──────┘ └──────┘ └──────┘ └──────┘            │
│ px   ├──────────────────────────────────────────────────┤
│      │ Charts Row (2 columns)                           │
│      │ ┌─────────────────┐ ┌─────────────────┐        │
│      │ │ Revenue Chart   │ │ Status Chart    │        │
│      │ │                 │ │                 │        │
│      │ └─────────────────┘ └─────────────────┘        │
│      ├──────────────────────────────────────────────────┤
│      │ Bottom Row (2 columns)                           │
│      │ ┌─────────────────┐ ┌─────────────────┐        │
│      │ │ Recent Activity │ │ Quick Actions   │        │
│      │ │                 │ │                 │        │
│      │ └─────────────────┘ └─────────────────┘        │
└──────┴──────────────────────────────────────────────────┘
```

### List Page Layout

```
┌─────────────────────────────────────────────────────────┐
│ Header (64px)                                           │
├──────┬──────────────────────────────────────────────────┤
│      │ Page Title + Create Button (80px)                │
│      ├──────────────────────────────────────────────────┤
│ Side │ Filters Bar (56px)                               │
│ bar  │ [Search] [Status] [Date] [Clear] [Export]       │
│      ├──────────────────────────────────────────────────┤
│ 280  │ Data Table                                       │
│ px   │ ┌─────────────────────────────────────────────┐ │
│      │ │ Header Row                                  │ │
│      │ ├─────────────────────────────────────────────┤ │
│      │ │ Data Row 1                          [Actions]│ │
│      │ │ Data Row 2                          [Actions]│ │
│      │ │ Data Row 3                          [Actions]│ │
│      │ │ ...                                          │ │
│      │ └─────────────────────────────────────────────┘ │
│      │ Pagination (56px)                                │
│      │ [< Previous] [1] [2] [3] ... [Next >]           │
└──────┴──────────────────────────────────────────────────┘
```

### Detail Page Layout

```
┌─────────────────────────────────────────────────────────┐
│ Header (64px)                                           │
├──────┬──────────────────────────────────────────────────┤
│      │ Back Button + Title + Actions (80px)             │
│      │ [< Back] Shipment #12345 [Edit] [Delete]        │
│      ├──────────────────────────────────────────────────┤
│ Side │ Status Badge + Metadata (60px)                   │
│ bar  │ [IN_TRANSIT] Created: Jan 15, 2024               │
│      ├──────────────────────────────────────────────────┤
│ 280  │ Tabs Navigation (48px)                           │
│ px   │ [Overview] [Sales] [Costs] [Logistics] [Timeline]│
│      ├──────────────────────────────────────────────────┤
│      │ Tab Content                                      │
│      │ ┌─────────────────────────────────────────────┐ │
│      │ │ Information Cards                           │ │
│      │ │                                             │ │
│      │ │ Related Data Tables                         │ │
│      │ │                                             │ │
│      │ └─────────────────────────────────────────────┘ │
└──────┴──────────────────────────────────────────────────┘
```

### Form Page Layout

```
┌─────────────────────────────────────────────────────────┐
│ Header (64px)                                           │
├──────┬──────────────────────────────────────────────────┤
│      │ Page Title (80px)                                │
│      │ Create New Shipment                              │
│      ├──────────────────────────────────────────────────┤
│ Side │ Form Container (max-width: 800px, centered)      │
│ bar  │ ┌─────────────────────────────────────────────┐ │
│      │ │ Section: Basic Information                  │ │
│ 280  │ │ [Country Origin] [Currency] [Status]        │ │
│ px   │ │                                             │ │
│      │ │ Section: Items                              │ │
│      │ │ [Product] [Quantity] [Price] [+ Add]        │ │
│      │ │                                             │ │
│      │ │ Section: Additional Details                 │ │
│      │ │ [Notes]                                     │ │
│      │ │                                             │ │
│      │ │ Actions                                     │ │
│      │ │ [Cancel] [Save Draft] [Create Shipment]     │ │
│      │ └─────────────────────────────────────────────┘ │
└──────┴──────────────────────────────────────────────────┘
```

## Responsive Breakpoints

### Desktop (> 1024px)
- Sidebar: 280px, always visible
- Content: Full width minus sidebar
- Grid: 4 columns for stat cards
- Charts: 2 columns

### Tablet (640px - 1024px)
- Sidebar: Collapsible, 80px when collapsed
- Content: Full width
- Grid: 2 columns for stat cards
- Charts: 1 column

### Mobile (< 640px)
- Sidebar: Hidden, accessible via drawer
- Content: Full width
- Grid: 1 column for stat cards
- Charts: 1 column, scrollable
- Tables: Horizontal scroll
- Forms: Full width inputs

## Animation & Transitions

### Timing Functions
```css
ease-out: cubic-bezier(0, 0, 0.2, 1)
ease-in: cubic-bezier(0.4, 0, 1, 1)
ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)
```

### Durations
```
Fast: 150ms (hover, focus)
Normal: 200ms (default)
Slow: 300ms (page transitions)
```

### Common Animations
```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide Up */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scale In */
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

## Loading States

### Skeleton Loaders
- Background: #E5E7EB
- Animation: Shimmer effect
- Border radius: Match component
- Height: Match content

### Spinners
- Size: 24px (small), 32px (medium), 48px (large)
- Color: #7C86F5
- Animation: Rotate 360deg, 1s linear infinite

### Progress Bars
- Height: 4px
- Background: #E5E7EB
- Fill: #7C86F5
- Animation: Indeterminate slide

## Empty States

**Layout:**
```
┌─────────────────────────┐
│                         │
│      [Large Icon]       │
│                         │
│   No data available     │
│   Create your first...  │
│                         │
│   [Primary Action]      │
│                         │
└─────────────────────────┘
```

**Styling:**
- Icon: 64px × 64px, #D1D5DB
- Title: Poppins 600, 18px, #1F2937
- Description: Inter 400, 14px, #6B7280
- Button: Primary style

## Error States

**Inline Error:**
```css
color: #EF4444
font: Inter 400, 12px
margin-top: 4px
icon: AlertCircle, 14px
```

**Error Banner:**
```css
background: #FEE2E2
border: 1px solid #FCA5A5
border-radius: 8px
padding: 12px 16px
color: #991B1B
icon: AlertTriangle, 20px
```

**Error Page:**
- Centered layout
- Large error icon
- Error code (404, 500, etc.)
- Description
- Action buttons (Go Home, Try Again)

## Accessibility Features

### Focus States
```css
outline: 2px solid #7C86F5
outline-offset: 2px
border-radius: inherit
```

### Keyboard Navigation
- Tab order: logical flow
- Skip links: "Skip to main content"
- Escape: Close modals/dropdowns
- Arrow keys: Navigate lists/menus

### Screen Reader
- ARIA labels on icons
- ARIA live regions for updates
- Semantic HTML elements
- Alt text on images

### Color Contrast
- Text on white: Minimum 4.5:1
- Large text: Minimum 3:1
- Interactive elements: Minimum 3:1

## Icon Usage

### Icon Library: Lucide React

**Common Icons:**
```
Navigation:
- Home, Package, Box, TrendingUp, CreditCard
- ShoppingCart, DollarSign, Truck, Users, Settings

Actions:
- Plus, Edit, Trash2, Eye, Download, Upload
- Save, X, Check, ChevronRight, ChevronDown

Status:
- CheckCircle, AlertCircle, AlertTriangle, Info
- Clock, Calendar, MapPin, Mail, Phone

Data:
- BarChart, LineChart, PieChart, Activity
- Filter, Search, SortAsc, SortDesc
```

**Icon Sizes:**
```
Small: 16px (inline with text)
Medium: 20px (buttons, nav items)
Large: 24px (headers, stat cards)
XLarge: 32px (empty states)
```

## Print Styles

```css
@media print {
  /* Hide navigation */
  .sidebar, .header { display: none; }
  
  /* Full width content */
  .main-content { margin: 0; width: 100%; }
  
  /* Page breaks */
  .card { page-break-inside: avoid; }
  
  /* Black and white */
  * { color: black !important; }
  
  /* Remove shadows */
  * { box-shadow: none !important; }
}
```

## Dark Mode (Future Enhancement)

```css
.dark {
  --background: #111827;
  --foreground: #F9FAFB;
  --card: #1F2937;
  --primary: #7C86F5;
  --border: #374151;
}
```

## Summary

This comprehensive UI design specification ensures consistency across the entire SeaFood dashboard. Every component, color, spacing, and interaction is carefully defined to create a cohesive, professional, and user-friendly interface.

The design system is:
- **Scalable**: Easy to extend with new components
- **Consistent**: Unified visual language
- **Accessible**: WCAG AA compliant
- **Responsive**: Works on all devices
- **Modern**: Contemporary design trends
- **Professional**: Business-appropriate aesthetics

Use this document as the single source of truth for all design decisions during implementation.
