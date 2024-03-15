/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit', // Habilita o Just-In-Time Compiler
  
  content: [
    "./node_modules/flowbite/**/*.js",
    // Certifique-se de adicionar todos os caminhos onde o Tailwind deve procurar por classes
    // Isso deve incluir seus arquivos HTML, JS, e quaisquer outros templates
    // Exemplo: './path/to/your/html/templates/**/*.html'
  ],
  
  theme: {
    extend: {
      // Adicionando novas larguras
      width: {
        '96': '24rem',
        'custom': '500px',
      },
      colors: {
        primary: {
          "50": "#eff6ff",
          "100": "#dbeafe",
          "200": "#bfdbfe",
          "300": "#93c5fd",
          "400": "#60a5fa",
          "500": "#3b82f6",
          "600": "#2563eb",
          "700": "#1d4ed8",
          "800": "#1e40af",
          "900": "#1e3a8a",
          "950": "#172554"
        },
      },
      fontFamily: {
        'sans': ['Montserrat', 'Arial', 'sans-serif'],
        'serif': ['Montserrat', 'Georgia', 'serif'],
        'mono': ['Montserrat', 'Courier New', 'monospace'],
        'body': ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'],
      },
    },
  },
  
  plugins: [
    require('flowbite/plugin'), // Adiciona o plugin Flowbite, se estiver usando
    // Inclua aqui outros plugins conforme necessário
  ],
}
