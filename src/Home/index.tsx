import './style.css'


export default function App() { 

  return (
    <main class="w-screen my-24 mx-5">
      <div class="w-1/2 p-3 flex justify-end">
        <button>Translate</button>
      </div>
      <section class="flex">
          {/* amber-500 */}
          <textarea class="h-64 p-2 w-1/2 bg-zinc-700" placeholder="Insert input text..." />
          <textarea class="h-64 p-7 w-1/2 text-2xl" placeholder='Translation' readonly />
      </section>
    </main>
  )
}


