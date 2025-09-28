import { defineConfig } from 'vite'
import solid from 'vite-plugin-solid'
import { viteStaticCopy } from 'vite-plugin-static-copy'


export default defineConfig({
  plugins: [
    solid(),
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
