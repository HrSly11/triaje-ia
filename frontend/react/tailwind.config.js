export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#3b82f6", 50: "#eff6ff", 100: "#dbeafe", 500: "#3b82f6", 600: "#2563eb", 700: "#1d4ed8" },
        secondary: { DEFAULT: "#64748b", 50: "#f8fafc", 100: "#f1f5f9", 500: "#64748b", 600: "#475569" },
        success: { DEFAULT: "#10b981", 50: "#ecfdf5", 500: "#10b981", 600: "#059669" },
        warning: { DEFAULT: "#f59e0b", 50: "#fffbeb", 500: "#f59e0b", 600: "#d97706" },
        danger: { DEFAULT: "#ef4444", 50: "#fef2f2", 500: "#ef4444", 600: "#dc2626" },
        urgent: { critico: "#dc2626", alto: "#f97316", moderado: "#eab308", bajo: "#22c55e" }
      }
    }
  },
  plugins: []
};
