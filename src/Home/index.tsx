import './style.css'


export default function App() { 

  return (
    <>
      <main class="w-screen flex bg-zinc-800">
          <section class="w-1/2">
            <div class="w-full px-2 flex justify-end">
              <button>Translate</button>
            </div>
            {/* amber-500 */}
            <textarea class="h-64 w-full" placeholder="Insert input text..." />
          </section>

          <textarea class="h-64 w-full" readonly />
      </main>
    </>
  )
}


