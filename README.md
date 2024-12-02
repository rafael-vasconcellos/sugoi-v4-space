# About

---
title: Sugoi V4
emoji: 🐳
colorFrom: purple
colorTo: gray
sdk: docker
app_port: 7860
license: mit
pinned: false
---

[Sugoi](https://huggingface.co/JustFrederik/sugoi-v4-ja-en-ct2) is a well-known lightweight Japanese to English translator. It can run on the average workstation, without a GPU. This space can run in a free hugging face space.

## How it works

The Flask server serves a rudimental web GUI and a rudimental web API that connects with a Redis server, which manages a queue to the model.


