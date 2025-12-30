# ERP Intelligence Agent - Next.js

A modern, professional ERP Intelligence Agent built with Next.js 14, TypeScript, and Tailwind CSS.

## Features

- **Dark/Light Theme** - Toggle between themes with smooth transitions
- **3D UI Components** - Professional 3D button and card designs
- **Interactive Charts** - Chart.js visualizations for financial, manufacturing, inventory, sales, and purchase data
- **Responsive Design** - Works on all screen sizes
- **State Management** - Zustand for client state
- **TypeScript** - Full type safety

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Chart.js + react-chartjs-2
- Zustand
- Lucide React

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Navigate to the project directory
cd next-app

# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at `http://localhost:3000`

## Project Structure

```
next-app/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── analyze/
│   │   │       └── route.ts     # API routes for analysis
│   │   ├── analysis/
│   │   │   └── page.tsx         # Analysis configuration page
│   │   ├── results/
│   │   │   └── page.tsx         # Results display page
│   │   ├── globals.css          # Global styles + 3D effects
│   │   ├── layout.tsx           # Root layout with providers
│   │   └── page.tsx             # Upload page (home)
│   ├── components/
│   │   ├── charts/              # Chart components
│   │   │   ├── chartConfig.ts
│   │   │   ├── RevenueChart.tsx
│   │   │   ├── MarginChart.tsx
│   │   │   ├── AgingChart.tsx
│   │   │   ├── ParetoChart.tsx
│   │   │   ├── EfficiencyChart.tsx
│   │   │   ├── WastageChart.tsx
│   │   │   ├── DeliveryChart.tsx
│   │   │   ├── SpendChart.tsx
│   │   │   └── LeadTimeChart.tsx
│   │   ├── layout/              # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── SidebarNav.tsx
│   │   ├── theme/
│   │   │   └── ThemeProvider.tsx
│   │   └── ui/                  # Base UI components
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Modal.tsx
│   │       ├── Tabs.tsx
│   │       └── ThemeToggle.tsx
│   ├── hooks/
│   │   └── useTheme.ts
│   ├── lib/
│   │   ├── formatters.ts        # Number/currency formatting
│   │   └── types.ts             # TypeScript type definitions
│   └── store/
│       └── useAppStore.ts       # Zustand store
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

## Theme System

The app uses CSS variables for theme colors. Toggle between light and dark modes:

```css
/* Light Theme (default) */
--bg-primary: #f8fafc;
--bg-secondary: #ffffff;
--text-primary: #1e293b;
--text-secondary: #64748b;

/* Dark Theme */
--bg-primary: #0f172a;
--bg-secondary: #1e293b;
--text-primary: #f1f5f9;
--text-secondary: #94a3b8;
```

## 3D Effects

The app includes 3D styling for buttons and cards:

```css
/* 3D Button */
.btn-3d {
  box-shadow: 0 4px 0 var(--primary-hover), 0 5px 10px rgba(0,0,0,0.2);
}

.btn-3d:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 0 var(--primary-hover), 0 8px 15px rgba(0,0,0,0.25);
}

/* 3D Card */
.card-3d {
  box-shadow: 5px 5px 10px var(--shadow-color),
              -5px -5px 10px rgba(255,255,255,0.8);
}
```

## Charts

Available chart components:

- `RevenueChart` - Revenue trend over time
- `MarginChart` - Margin percentage trend
- `AgingChart` - Stock aging distribution (doughnut)
- `ParetoChart` - 80/20 analysis
- `EfficiencyChart` - Production efficiency by product
- `WastageChart` - Wastage by product (horizontal bar)
- `DeliveryChart` - Delivery performance (doughnut)
- `SpendChart` - Spend by supplier (horizontal bar)
- `LeadTimeChart` - Lead time trend

## Building for Production

```bash
npm run build
npm start
```

## License

MIT
