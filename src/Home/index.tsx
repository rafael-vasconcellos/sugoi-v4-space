import { createSignal, createResource } from 'solid-js'
import './style.css'



interface ITranslation { 
    originalText: string
    translatedText?: string
}

interface InputTextState { 
    text?: string
}

export default function App() { 
    const [ text, setText ] = createSignal<InputTextState | null>(null)
    const [ translation, { mutate } ] = createResource(text, fetchData)
    let textarea: HTMLTextAreaElement | undefined


    async function fetchData(input: InputTextState): Promise<ITranslation | null> { 
      const { text } = input
      if (!text || translation.loading) { return null }
      if (translation()) { mutate(null) }
      const response = await fetch(`/api/translate?text=${text}`, { method: "POST" }).then(response => { 
          if (response.status === 200) { return response.json() }
  
      }).then(response => response?.[0])
      .catch(() => null)
  
      return { originalText: text, translatedText: response }
  }


    return (
      <main class="w-screen my-24 mx-5">
        <div class="w-1/2 py-4 px-2 flex justify-end">
          <button onclick={() => {
              setText({ text: textarea?.value })
          }}>Translate</button>
        </div>
        <section class="flex">
            {/* amber-500 */}
            <textarea class="h-64 p-2 w-1/2 bg-zinc-700" placeholder="Insert input text..." ref={textarea} />
            <textarea class="h-64 p-7 w-1/2 text-2xl" placeholder={translation.loading? "Translating..." : "Translation"} readonly value={translation()?.translatedText ?? ''} />
        </section>
      </main>
    )
}


