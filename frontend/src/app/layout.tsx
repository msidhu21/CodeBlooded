import type { Metadata } from 'next'
import './globals.css'
import ClientThemeProvider from '@/components/ClientThemeProvider'

export const metadata: Metadata = {
  title: 'COSC 310 - Product Catalog',
  description: 'Product search and management system',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <ClientThemeProvider>
          {children}
        </ClientThemeProvider>
      </body>
    </html>
  )
}

