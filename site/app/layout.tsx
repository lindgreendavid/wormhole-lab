import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Wormhole Lab — the Morris-Thorne throat, computed exactly",
  description:
    "A rigorous, interactive computed exploration of the Morris-Thorne traversable wormhole: the real general-relativistic metric, the exotic matter it forces, and the actual open problem it implies.",
  applicationName: "Wormhole Lab",
  keywords: [
    "traversable wormhole",
    "Morris-Thorne metric",
    "general relativity",
    "exotic matter",
    "energy conditions",
    "theoretical physics",
    "reproducible research",
    "web accessibility",
  ],
  openGraph: {
    title: "Wormhole Lab",
    description:
      "Does a traversable wormhole solve Einstein's equations, and what does that force the matter at its throat to be? Computed exactly, not asserted.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Wormhole Lab",
    description:
      "A rigorous computed exploration of the Morris-Thorne traversable wormhole and the exotic-matter problem it implies.",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>{children}</body>
    </html>
  );
}
