import Link from "next/link"
import type React from "react"
import "./globals.css"

export const metadata = {
  title: "Tanda Agent | AI-Powered Solutions",
  description: "Next-gen AI solutions for businesses",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-gray-900 text-gray-100">
        <div className="flex flex-col md:flex-row flex-grow">
          <aside className="bg-gray-800 w-full md:w-64 p-6 space-y-6">
            <Link
              href="/"
              className="text-2xl font-bold block mb-6 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text"
            >
              Tanda Agent
            </Link>
            <nav className="space-y-4">
              <Link href="/" className="block hover:bg-gray-700 p-2 rounded transition-colors duration-200">
                Home
              </Link>
              <Link href="/tanda-agent" className="block hover:bg-gray-700 p-2 rounded transition-colors duration-200">
                AI Chat
              </Link>
            </nav>
          </aside>
          <main className="flex-grow p-6 overflow-auto">{children}</main>
        </div>
      </body>
    </html>
  )
}

