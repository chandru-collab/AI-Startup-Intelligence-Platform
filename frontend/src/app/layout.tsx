import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Startup Intelligence Platform",
  description: "Autonomous discovery, verification, analysis, prediction, and reporting of startup intelligence",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
