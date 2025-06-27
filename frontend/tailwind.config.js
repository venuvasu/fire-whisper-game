module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primaryBackground: "var(--color-primaryBackground)",
        primaryText: "var(--color-primaryText)",
        containerBackground: "var(--color-containerBackground)",
      },
      fontFamily: {
        ebgaramond: ['"EB Garamond"', "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};
