import { defineConfig } from 'vite'


export default defineConfig({
    build: {
        outDir: 'public',
        rollupOptions: {
            input: 'src/main.js',
            output: {
                entryFileNames: 'bundle.js'
            }
        },
        emptyOutDir: false
    }
})