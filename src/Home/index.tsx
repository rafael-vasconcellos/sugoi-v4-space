import { createSignal, useTransition } from 'solid-js'
import './style.css'



interface ITranslation { 
    originalText: string
    translatedText?: string
}

export default function App() { 
    const [ isPending, start ] = useTransition()
    const [ translation, setTranslation ] = createSignal<ITranslation | null>(null)
    const placeholder_text = () => isPending()? 'Translating...' : 'Translation'
    let textarea: HTMLTextAreaElement | undefined

    async function fetchData(text: string) { 
      if (text === translation()?.translatedText || !text) { return }
      if (translation()) { setTranslation(null) }
      const response = await fetch(`/api/translate?text=${text}`, { method: "POST" }).then(response => { 
          if (response.status === 200) { return response.json() }
  
      }).then(response => response?.[0])
      .catch(() => null)
  
      setTranslation({ originalText: text, translatedText: response })
  }

    return (
      <main class="w-screen my-24 mx-5">
        <div class="w-1/2 py-4 px-2 flex justify-end">
          <button onclick={() => { 
              start(() => fetchData(textarea?.value as string))
          } }>Translate</button>
        </div>
        <section class="flex">
            {/* amber-500 */}
            <textarea class="h-64 p-2 w-1/2 bg-zinc-700" placeholder="Insert input text..." ref={textarea} />
            <textarea class="h-64 p-7 w-1/2 text-2xl" placeholder={placeholder_text()} readonly value={translation()?.translatedText ?? ''} />
        </section>
      </main>
    )
}


