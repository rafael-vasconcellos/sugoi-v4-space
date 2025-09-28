import { defineConfig } from 'vite'
import solid from 'vite-plugin-solid'
import tailwindcss from '@tailwindcss/vite'
import { viteStaticCopy } from 'vite-plugin-static-copy'


export default defineConfig({
  plugins: [
    solid(),
    tailwindcss(),
    viteStaticCopy({
        targets: [
          { src: 'public', dest: '.' } // copia tudo para dist/public/
        ]
    })
  ],
  build: { 
      outDir: "server/dist"
  },
  publicDir: false,
})
