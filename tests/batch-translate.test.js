import { it } from "node:test"
import assert from "node:assert"


it("should batch translate", async() => { 
    const input_texts = [
        "ダンガンロンパ 希望の学園と絶望の高校生",
        "スーパーダンガンロンパ2 さよなら絶望学園",
        "ニューダンガンロンパV3 みんなのコロシアイ新学期",
    ]
    const response = await fetch("http://localhost:7860/api/translate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ input_texts })
    })
    const { translations } = await response.text()
        .then(text => {
            try { return JSON.parse(text) }
            catch {
                console.log(text)
                return { translations: [] }
            }
        })

    assert.ok(response.ok && translations.length === input_texts.length)
})