module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh",
        "100vh": "100vh",

      },
      fill: theme => ({
        'red': theme('colors.red.500'),
      }),
      borderRadius: {
        xl: "1.5rem"
      }
    },
  },
  variants: {
    extend: { fill: ['hover', 'focus'], },
  },
  plugins: [],
}
