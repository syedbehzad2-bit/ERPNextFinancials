'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Upload,
  FileBarChart,
  Settings,
  ChevronRight,
} from 'lucide-react';
import { clsx } from 'clsx';

interface NavItem {
  href: string;
  label: string;
  icon: React.ReactNode;
}

const navItems: NavItem[] = [
  {
    href: '/',
    label: 'Upload Data',
    icon: <Upload className="w-5 h-5" />,
  },
  {
    href: '/analysis',
    label: 'Configure Analysis',
    icon: <Settings className="w-5 h-5" />,
  },
  {
    href: '/results',
    label: 'View Results',
    icon: <FileBarChart className="w-5 h-5" />,
  },
];

export function SidebarNav() {
  const pathname = usePathname();

  return (
    <nav className="flex flex-col gap-1 p-3">
      {navItems.map((item) => {
        const isActive = pathname === item.href;
        return (
          <Link
            key={item.href}
            href={item.href}
            className={clsx(
              'sidebar-item',
              isActive && 'active'
            )}
          >
            {item.icon}
            <span className="font-medium">{item.label}</span>
            {isActive && <ChevronRight className="w-4 h-4 ml-auto" />}
          </Link>
        );
      })}
    </nav>
  );
}
