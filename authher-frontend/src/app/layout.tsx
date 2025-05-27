import type { Metadata } from "next";
import "./globals.css";
import { Instrument_Sans } from "next/font/google";

const instrumentSans = Instrument_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"], // Pick weights you use
  variable: "--font-instrument-sans", // Optional if using CSS vars
});

export const metadata: Metadata = {
  title: "auther.",
  description: "Start your search with women-led research.",
  icons: [
    {
      rel: "icon",
      url: "/autherbooklight.svg",
      media: "(prefers-color-scheme: light)",
    },
    {
      rel: "icon",
      url: "/autherbookdark.svg",
      media: "(prefers-color-scheme: dark)",
    },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={instrumentSans.className}>
      <body className="antialiased">{children}</body>
    </html>
  );
}
