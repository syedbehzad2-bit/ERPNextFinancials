import type { Metadata } from 'next';
import { ThemeProvider } from '@/components/theme/ThemeProvider';
import './globals.css';

export const metadata: Metadata = {
  title: 'ERP Intelligence Agent',
  description: 'Senior ERP Financial & Operations Intelligence Agent',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-light-bg dark:bg-dark-bg">
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
