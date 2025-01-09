"use client";

import { useState } from "react";
import { ToggleHome } from "@/components/dark-light-toggle";
import {useRouter} from "next/navigation";

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const router = useRouter();
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    if (darkMode) {
      document.documentElement.classList.remove("dark");
    } else {
      document.documentElement.classList.add("dark");
    }
  };

  return (
    <div className="h-screen bg-white text-black dark:bg-neutral-800 dark:text-white">
      <ToggleHome mode={darkMode ? "dark" : "light"} onClick={toggleDarkMode} />

      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center h-full px-4 gap-2">
        {/* Title */}
        <h1 className="text-5xl font-bold text-center mb-4">Welcome to Spendalysis</h1>

        <p className="text-lg text-center max-w-2xl mb-8">
          Take control of your finances with Spendalysis. Analyze your expenses,
          visualize spending patterns, and achieve your financial goals effortlessly.
        </p>

        <label>Upload a CSV of your file to get insight on your sepnding</label>
        <a

          className="px-6 py-3 text-lg font-semibold text-white bg-blue-500 rounded-lg shadow-lg hover:bg-blue-600 transition duration-300" onClick={()=> router.push('/uploads')}
        >
          Take me!
        </a>
      </div>

      <footer className="absolute bottom-4 w-full text-center">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          &copy; {new Date().getFullYear()} Spendalysis. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
