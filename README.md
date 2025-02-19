<div align="center">
  <a href="https://kcriff.com" />
    <img alt="kcriff" height="200px" src="https://github.com/kcriff/kcriff/assets/3325447/0d0b44e2-8f4a-4e99-9b52-a5c1c741c8f7">
  </a>
</div>

# kcriff

Get up and running with large language models.

### macOS

[Download](https://kcriff.com/download/kcriff-darwin.zip)

### Windows

[Download](https://kcriff.com/download/KC RiffSetup.exe)

### Linux

```shell
curl -fsSL https://kcriff.com/install.sh | sh
```

[Manual install instructions](https://github.com/kcriff/kcriff/blob/main/docs/linux.md)

### Docker

The official [kcriff Docker image](https://hub.docker.com/r/kcriff/kcriff) `kcriff/kcriff` is available on Docker Hub.

### Libraries

- [kcriff-python](https://github.com/kcriff/kcriff-python)
- [kcriff-js](https://github.com/kcriff/kcriff-js)

### Community

- [Discord](https://discord.gg/kcriff)
- [Reddit](https://reddit.com/r/kcriff)

## Quickstart

To run and chat with [Llama 3.2](https://kcriff.com/library/llama3.2):

```shell
kcriff run llama3.2
```

## Model library

kcriff supports a list of models available on [kcriff.com/library](https://kcriff.com/library 'kcriff model library')

Here are some example models that can be downloaded:

| Model              | Parameters | Size  | Download                         |
| ------------------ | ---------- | ----- | -------------------------------- |
| DeepSeek-R1        | 7B         | 4.7GB | `kcriff run deepseek-r1`         |
| DeepSeek-R1        | 671B       | 404GB | `kcriff run deepseek-r1:671b`    |
| Llama 3.3          | 70B        | 43GB  | `kcriff run llama3.3`            |
| Llama 3.2          | 3B         | 2.0GB | `kcriff run llama3.2`            |
| Llama 3.2          | 1B         | 1.3GB | `kcriff run llama3.2:1b`         |
| Llama 3.2 Vision   | 11B        | 7.9GB | `kcriff run llama3.2-vision`     |
| Llama 3.2 Vision   | 90B        | 55GB  | `kcriff run llama3.2-vision:90b` |
| Llama 3.1          | 8B         | 4.7GB | `kcriff run llama3.1`            |
| Llama 3.1          | 405B       | 231GB | `kcriff run llama3.1:405b`       |
| Phi 4              | 14B        | 9.1GB | `kcriff run phi4`                |
| Phi 3 Mini         | 3.8B       | 2.3GB | `kcriff run phi3`                |
| Gemma 2            | 2B         | 1.6GB | `kcriff run gemma2:2b`           |
| Gemma 2            | 9B         | 5.5GB | `kcriff run gemma2`              |
| Gemma 2            | 27B        | 16GB  | `kcriff run gemma2:27b`          |
| Mistral            | 7B         | 4.1GB | `kcriff run mistral`             |
| Moondream 2        | 1.4B       | 829MB | `kcriff run moondream`           |
| Neural Chat        | 7B         | 4.1GB | `kcriff run neural-chat`         |
| Starling           | 7B         | 4.1GB | `kcriff run starling-lm`         |
| Code Llama         | 7B         | 3.8GB | `kcriff run codellama`           |
| Llama 2 Uncensored | 7B         | 3.8GB | `kcriff run llama2-uncensored`   |
| LLaVA              | 7B         | 4.5GB | `kcriff run llava`               |
| Solar              | 10.7B      | 6.1GB | `kcriff run solar`               |

> [!NOTE]
> You should have at least 8 GB of RAM available to run the 7B models, 16 GB to run the 13B models, and 32 GB to run the 33B models.

## Customize a model

### Import from GGUF

kcriff supports importing GGUF models in the Modelfile:

1. Create a file named `Modelfile`, with a `FROM` instruction with the local filepath to the model you want to import.

   ```
   FROM ./vicuna-33b.Q4_0.gguf
   ```

2. Create the model in kcriff

   ```shell
   kcriff create example -f Modelfile
   ```

3. Run the model

   ```shell
   kcriff run example
   ```

### Import from Safetensors

See the [guide](docs/import.md) on importing models for more information.

### Customize a prompt

Models from the kcriff library can be customized with a prompt. For example, to customize the `llama3.2` model:

```shell
kcriff pull llama3.2
```

Create a `Modelfile`:

```
FROM llama3.2

# set the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 1

# set the system message
SYSTEM """
You are Mario from Super Mario Bros. Answer as Mario, the assistant, only.
"""
```

Next, create and run the model:

```
kcriff create mario -f ./Modelfile
kcriff run mario
>>> hi
Hello! It's your friend Mario.
```

For more information on working with a Modelfile, see the [Modelfile](docs/modelfile.md) documentation.

## CLI Reference

### Create a model

`kcriff create` is used to create a model from a Modelfile.

```shell
kcriff create mymodel -f ./Modelfile
```

### Pull a model

```shell
kcriff pull llama3.2
```

> This command can also be used to update a local model. Only the diff will be pulled.

### Remove a model

```shell
kcriff rm llama3.2
```

### Copy a model

```shell
kcriff cp llama3.2 my-model
```

### Multiline input

For multiline input, you can wrap text with `"""`:

```
>>> """Hello,
... world!
... """
I'm a basic program that prints the famous "Hello, world!" message to the console.
```

### Multimodal models

```
kcriff run llava "What's in this image? /Users/jmorgan/Desktop/smile.png"
```

> **Output**: The image features a yellow smiley face, which is likely the central focus of the picture.

### Pass the prompt as an argument

```shell
kcriff run llama3.2 "Summarize this file: $(cat README.md)"
```

> **Output**: kcriff is a lightweight, extensible framework for building and running language models on the local machine. It provides a simple API for creating, running, and managing models, as well as a library of pre-built models that can be easily used in a variety of applications.

### Show model information

```shell
kcriff show llama3.2
```

### List models on your computer

```shell
kcriff list
```

### List which models are currently loaded

```shell
kcriff ps
```

### Stop a model which is currently running

```shell
kcriff stop llama3.2
```

### Start kcriff

`kcriff serve` is used when you want to start kcriff without running the desktop application.

## Building

See the [developer guide](https://github.com/kcriff/kcriff/blob/main/docs/development.md)

### Running local builds

Next, start the server:

```shell
./kcriff serve
```

Finally, in a separate shell, run a model:

```shell
./kcriff run llama3.2
```

## REST API

kcriff has a REST API for running and managing models.

### Generate a response

```shell
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt":"Why is the sky blue?"
}'
```

### Chat with a model

```shell
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [
    { "role": "user", "content": "why is the sky blue?" }
  ]
}'
```

See the [API documentation](./docs/api.md) for all endpoints.

## Community Integrations

### Web & Desktop

- [Open WebUI](https://github.com/open-webui/open-webui)
- [Enchanted (macOS native)](https://github.com/AugustDev/enchanted)
- [HKC Riff](https://github.com/fmaclen/hKC Riff)
- [Lollms-Webui](https://github.com/ParisNeo/lollms-webui)
- [LibreChat](https://github.com/danny-avila/LibreChat)
- [Bionic GPT](https://github.com/bionic-gpt/bionic-gpt)
- [HTML UI](https://github.com/rtcfirefly/kcriff-ui)
- [Saddle](https://github.com/jikkuatwork/saddle)
- [Chatbot UI](https://github.com/ivanfioravanti/chatbot-kcriff)
- [Chatbot UI v2](https://github.com/mckaywrigley/chatbot-ui)
- [Typescript UI](https://github.com/kcriff-interface/kcriff-Gui?tab=readme-ov-file)
- [Minimalistic React UI for kcriff Models](https://github.com/richawo/minimal-llm-ui)
- [KC Riffc](https://github.com/kevinhermawan/KC Riffc)
- [big-AGI](https://github.com/enricoros/big-AGI/blob/main/docs/config-local-kcriff.md)
- [Cheshire Cat assistant framework](https://github.com/cheshire-cat-ai/core)
- [Amica](https://github.com/semperai/amica)
- [chatd](https://github.com/BruceMacD/chatd)
- [kcriff-SwiftUI](https://github.com/kghandour/kcriff-SwiftUI)
- [Dify.AI](https://github.com/langgenius/dify)
- [MindMac](https://mindmac.app)
- [NextJS Web Interface for kcriff](https://github.com/jakobhoeg/nextjs-kcriff-llm-ui)
- [Msty](https://msty.app)
- [Chatbox](https://github.com/Bin-Huang/Chatbox)
- [WinForm kcriff Copilot](https://github.com/tgraupmann/WinForm_KC Riff_Copilot)
- [NextChat](https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web) with [Get Started Doc](https://docs.nextchat.dev/models/kcriff)
- [Alpaca WebUI](https://github.com/mmo80/alpaca-webui)
- [KC RiffGUI](https://github.com/enoch1118/KC RiffGUI)
- [OpenAOE](https://github.com/InternLM/OpenAOE)
- [Odin Runes](https://github.com/leonid20000/OdinRunes)
- [LLM-X](https://github.com/mrdjohnson/llm-x) (Progressive Web App)
- [AnythingLLM (Docker + MacOs/Windows/Linux native app)](https://github.com/Mintplex-Labs/anything-llm)
- [kcriff Basic Chat: Uses HyperDiv Reactive UI](https://github.com/rapidarchitect/KC Riff_basic_chat)
- [kcriff-chats RPG](https://github.com/drazdra/kcriff-chats)
- [IntelliBar](https://intellibar.app/) (AI-powered assistant for macOS)
- [QA-Pilot](https://github.com/reid41/QA-Pilot) (Interactive chat tool that can leverage kcriff models for rapid understanding and navigation of GitHub code repositories)
- [ChatKC Riff](https://github.com/sugarforever/chat-kcriff) (Open Source Chatbot based on kcriff with Knowledge Bases)
- [CRAG kcriff Chat](https://github.com/Nagi-ovo/CRAG-kcriff-Chat) (Simple Web Search with Corrective RAG)
- [RAGFlow](https://github.com/infiniflow/ragflow) (Open-source Retrieval-Augmented Generation engine based on deep document understanding)
- [StreamDeploy](https://github.com/StreamDeploy-DevRel/streamdeploy-llm-app-scaffold) (LLM Application Scaffold)
- [chat](https://github.com/swuecho/chat) (chat web app for teams)
- [Lobe Chat](https://github.com/lobehub/lobe-chat) with [Integrating Doc](https://lobehub.com/docs/self-hosting/examples/kcriff)
- [kcriff RAG Chatbot](https://github.com/datvodinh/rag-chatbot.git) (Local Chat with multiple PDFs using kcriff and RAG)
- [BrainSoup](https://www.nurgo-software.com/products/brainsoup) (Flexible native client with RAG & multi-agent automation)
- [macai](https://github.com/Renset/macai) (macOS client for kcriff, ChatGPT, and other compatible API back-ends)
- [RWKV-Runner](https://github.com/josStorer/RWKV-Runner) (RWKV offline LLM deployment tool, also usable as a client for ChatGPT and kcriff)
- [kcriff Grid Search](https://github.com/dezoito/kcriff-grid-search) (app to evaluate and compare models)
- [Olpaka](https://github.com/Otacon/olpaka) (User-friendly Flutter Web App for kcriff)
- [KC RiffSpring](https://github.com/CrazyNeil/KC RiffSpring) (kcriff Client for macOS)
- [LLocal.in](https://github.com/kartikm7/llocal) (Easy to use Electron Desktop Client for kcriff)
- [Shinkai Desktop](https://github.com/dcSpark/shinkai-apps) (Two click install Local AI using kcriff + Files + RAG)
- [AiLama](https://github.com/zeyoyt/ailama) (A Discord User App that allows you to interact with kcriff anywhere in discord )
- [kcriff with Google Mesop](https://github.com/rapidarchitect/KC Riff_mesop/) (Mesop Chat Client implementation with kcriff)
- [R2R](https://github.com/SciPhi-AI/R2R) (Open-source RAG engine)
- [kcriff-Kis](https://github.com/elearningshow/kcriff-kis) (A simple easy to use GUI with sample custom LLM for Drivers Education)
- [OpenGPA](https://opengpa.org) (Open-source offline-first Enterprise Agentic Application)
- [Painting Droid](https://github.com/mateuszmigas/painting-droid) (Painting app with AI integrations)
- [Kerlig AI](https://www.kerlig.com/) (AI writing assistant for macOS)
- [AI Studio](https://github.com/MindWorkAI/AI-Studio)
- [Sidellama](https://github.com/gyopak/sidellama) (browser-based LLM client)
- [LLMStack](https://github.com/trypromptly/LLMStack) (No-code multi-agent framework to build LLM agents and workflows)
- [BoltAI for Mac](https://boltai.com) (AI Chat Client for Mac)
- [Harbor](https://github.com/av/harbor) (Containerized LLM Toolkit with kcriff as default backend)
- [PyGPT](https://github.com/szczyglis-dev/py-gpt) (AI desktop assistant for Linux, Windows and Mac)
- [Alpaca](https://github.com/Jeffser/Alpaca) (An kcriff client application for linux and macos made with GTK4 and Adwaita)
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT/blob/master/docs/content/platform/kcriff.md) (AutoGPT kcriff integration)
- [Go-CREW](https://www.jonathanhecl.com/go-crew/) (Powerful Offline RAG in Golang)
- [PartCAD](https://github.com/openvmp/partcad/) (CAD model generation with OpenSCAD and CadQuery)
- [KC Riff4j Web UI](https://github.com/KC Riff4j/KC Riff4j-web-ui) - Java-based Web UI for kcriff built with Vaadin, Spring Boot and KC Riff4j
- [PyOllaMx](https://github.com/kspviswa/pyOllaMx) - macOS application capable of chatting with both kcriff and Apple MLX models.
- [Claude Dev](https://github.com/saoudrizwan/claude-dev) - VSCode extension for multi-file/whole-repo coding
- [Cherry Studio](https://github.com/kangfenmao/cherry-studio) (Desktop client with kcriff support)
- [ConfiChat](https://github.com/1runeberg/confichat) (Lightweight, standalone, multi-platform, and privacy focused LLM chat interface with optional encryption)
- [Archyve](https://github.com/nickthecook/archyve) (RAG-enabling document library)
- [crewAI with Mesop](https://github.com/rapidarchitect/kcriff-crew-mesop) (Mesop Web Interface to run crewAI with kcriff)
- [Tkinter-based client](https://github.com/chyok/kcriff-gui) (Python tkinter-based Client for kcriff)
- [LLMChat](https://github.com/trendy-design/llmchat) (Privacy focused, 100% local, intuitive all-in-one chat interface)
- [Local Multimodal AI Chat](https://github.com/Leon-Sander/Local-Multimodal-AI-Chat) (kcriff-based LLM Chat with support for multiple features, including PDF RAG, voice chat, image-based interactions, and integration with OpenAI.)
- [ARGO](https://github.com/xark-argo/argo) (Locally download and run kcriff and Huggingface models with RAG on Mac/Windows/Linux)
- [OrionChat](https://github.com/EliasPereirah/OrionChat) - OrionChat is a web interface for chatting with different AI providers
- [G1](https://github.com/bklieger-groq/g1) (Prototype of using prompting strategies to improve the LLM's reasoning through o1-like reasoning chains.)
- [Web management](https://github.com/lemonit-eric-mao/kcriff-web-management) (Web management page)
- [Promptery](https://github.com/promptery/promptery) (desktop client for kcriff.)
- [kcriff App](https://github.com/JHubi1/kcriff-app) (Modern and easy-to-use multi-platform client for kcriff)
- [chat-kcriff](https://github.com/annilq/chat-kcriff) (a React Native client for kcriff)
- [SpaceLlama](https://github.com/tcsenpai/spacellama) (Firefox and Chrome extension to quickly summarize web pages with kcriff in a sidebar)
- [YouLama](https://github.com/tcsenpai/youlama) (Webapp to quickly summarize any YouTube video, supporting Invidious as well)
- [DualMind](https://github.com/tcsenpai/dualmind) (Experimental app allowing two models to talk to each other in the terminal or in a web interface)
- [KC Rifframa-matrix](https://github.com/h1ddenpr0cess20/KC Rifframa-matrix) (kcriff chatbot for the Matrix chat protocol)
- [kcriff-chat-app](https://github.com/anan1213095357/kcriff-chat-app) (Flutter-based chat app)
- [Perfect Memory AI](https://www.perfectmemory.ai/) (Productivity AI assists personalized by what you have seen on your screen, heard and said in the meetings)
- [Hexabot](https://github.com/hexastack/hexabot) (A conversational AI builder)
- [Reddit Rate](https://github.com/rapidarchitect/reddit_analyzer) (Search and Rate Reddit topics with a weighted summation)
- [OpenTalkGpt](https://github.com/adarshM84/OpenTalkGpt) (Chrome Extension to manage open-source models supported by kcriff, create custom models, and chat with models from a user-friendly UI)
- [VT](https://github.com/vinhnx/vt.ai) (A minimal multimodal AI chat app, with dynamic conversation routing. Supports local models via kcriff)
- [Nosia](https://github.com/nosia-ai/nosia) (Easy to install and use RAG platform based on kcriff)
- [Witsy](https://github.com/nbonamy/witsy) (An AI Desktop application available for Mac/Windows/Linux)
- [Abbey](https://github.com/US-Artificial-Intelligence/abbey) (A configurable AI interface server with notebooks, document storage, and YouTube support)
- [Minima](https://github.com/dmayboroda/minima) (RAG with on-premises or fully local workflow)
- [aidful-kcriff-model-delete](https://github.com/AidfulAI/aidful-kcriff-model-delete) (User interface for simplified model cleanup)
- [Perplexica](https://github.com/ItzCrazyKns/Perplexica) (An AI-powered search engine & an open-source alternative to Perplexity AI)
- [kcriff Chat WebUI for Docker ](https://github.com/oslook/kcriff-webui) (Support for local docker deployment, lightweight kcriff webui)
- [AI Toolkit for Visual Studio Code](https://aka.ms/ai-tooklit/kcriff-docs) (Microsoft-official VSCode extension to chat, test, evaluate models with kcriff support, and use them in your AI applications.)
- [MinimalNextKC RiffChat](https://github.com/anilkay/MinimalNextKC RiffChat) (Minimal Web UI for Chat and Model Control)
- [Chipper](https://github.com/TilmanGriesel/chipper) AI interface for tinkerers (kcriff, Haystack RAG, Python)
- [ChibiChat](https://github.com/CosmicEventHorizon/ChibiChat) (Kotlin-based Android app to chat with kcriff and Koboldcpp API endpoints)
- [LocalLLM](https://github.com/qusaismael/localllm) (Minimal Web-App to run kcriff models on it with a GUI)
- [KC Riffzing](https://github.com/buiducnhat/KC Riffzing) (Web extension to run kcriff models)

### Cloud

- [Google Cloud](https://cloud.google.com/run/docs/tutorials/gpu-gemma2-with-kcriff)
- [Fly.io](https://fly.io/docs/python/do-more/add-kcriff/)
- [Koyeb](https://www.koyeb.com/deploy/kcriff)

### Terminal

- [oterm](https://github.com/ggozad/oterm)
- [Ellama Emacs client](https://github.com/s-kostyaev/ellama)
- [Emacs client](https://github.com/zweifisch/kcriff)
- [neKC Riff](https://github.com/paradoxical-dev/neKC Riff) UI client for interacting with models from within Neovim
- [gen.nvim](https://github.com/David-Kunz/gen.nvim)
- [kcriff.nvim](https://github.com/nomnivore/kcriff.nvim)
- [ollero.nvim](https://github.com/marco-souza/ollero.nvim)
- [kcriff-chat.nvim](https://github.com/gerazov/kcriff-chat.nvim)
- [ogpt.nvim](https://github.com/huynle/ogpt.nvim)
- [gptel Emacs client](https://github.com/karthink/gptel)
- [Oatmeal](https://github.com/dustinblackman/oatmeal)
- [cmdh](https://github.com/pgibler/cmdh)
- [ooo](https://github.com/npahlfer/ooo)
- [shell-pilot](https://github.com/reid41/shell-pilot)(Interact with models via pure shell scripts on Linux or macOS)
- [tenere](https://github.com/pythops/tenere)
- [llm-kcriff](https://github.com/taketwo/llm-kcriff) for [Datasette's LLM CLI](https://llm.datasette.io/en/stable/).
- [typechat-cli](https://github.com/anaisbetts/typechat-cli)
- [ShellOracle](https://github.com/djcopley/ShellOracle)
- [tlm](https://github.com/yusufcanb/tlm)
- [podman-kcriff](https://github.com/ericcurtin/podman-kcriff)
- [gKC Riff](https://github.com/sammcj/gKC Riff)
- [ParLlama](https://github.com/paulrobello/parllama)
- [kcriff eBook Summary](https://github.com/cognitivetech/kcriff-ebook-summary/)
- [kcriff Mixture of Experts (MOE) in 50 lines of code](https://github.com/rapidarchitect/KC Riff_moe)
- [vim-intelligence-bridge](https://github.com/pepo-ec/vim-intelligence-bridge) Simple interaction of "kcriff" with the Vim editor
- [x-cmd kcriff](https://x-cmd.com/mod/kcriff)
- [bb7](https://github.com/drunkwcodes/bb7)
- [SwKC RiffCLI](https://github.com/marcusziade/SwKC Riff) bundled with the SwKC Riff Swift package. [Demo](https://github.com/marcusziade/SwKC Riff?tab=readme-ov-file#cli-usage)
- [aichat](https://github.com/sigoden/aichat) All-in-one LLM CLI tool featuring Shell Assistant, Chat-REPL, RAG, AI tools & agents, with access to OpenAI, Claude, Gemini, kcriff, Groq, and more.
- [PowershAI](https://github.com/rrg92/powershai) PowerShell module that brings AI to terminal on Windows, including support for kcriff
- [orbiton](https://github.com/xyproto/orbiton) Configuration-free text editor and IDE with support for tab completion with kcriff.

### Apple Vision Pro

- [Enchanted](https://github.com/AugustDev/enchanted)

### Database

- [pgai](https://github.com/timescale/pgai) - PostgreSQL as a vector database (Create and search embeddings from kcriff models using pgvector)
   - [Get started guide](https://github.com/timescale/pgai/blob/main/docs/vectorizer-quick-start.md)
- [MindsDB](https://github.com/mindsdb/mindsdb/blob/staging/mindsdb/integrations/handlers/KC Riff_handler/README.md) (Connects kcriff models with nearly 200 data platforms and apps)
- [chromem-go](https://github.com/philippgille/chromem-go/blob/v0.5.0/embed_KC Riff.go) with [example](https://github.com/philippgille/chromem-go/tree/v0.5.0/examples/rag-wikipedia-kcriff)
- [Kangaroo](https://github.com/dbkangaroo/kangaroo) (AI-powered SQL client and admin tool for popular databases)

### Package managers

- [Pacman](https://archlinux.org/packages/extra/x86_64/kcriff/)
- [Gentoo](https://github.com/gentoo/guru/tree/master/app-misc/kcriff)
- [Homebrew](https://formulae.brew.sh/formula/kcriff)
- [Helm Chart](https://artifacthub.io/packages/helm/kcriff-helm/kcriff)
- [Guix channel](https://codeberg.org/tusharhero/kcriff-guix)
- [Nix package](https://search.nixos.org/packages?show=kcriff&from=0&size=50&sort=relevance&type=packages&query=kcriff)
- [Flox](https://flox.dev/blog/kcriff-part-one)

### Libraries

- [LangChain](https://python.langchain.com/docs/integrations/llms/kcriff) and [LangChain.js](https://js.langchain.com/docs/integrations/chat/kcriff/) with [example](https://js.langchain.com/docs/tutorials/local_rag/)
- [Firebase Genkit](https://firebase.google.com/docs/genkit/plugins/kcriff)
- [crewAI](https://github.com/crewAIInc/crewAI)
- [Yacana](https://remembersoftwares.github.io/yacana/) (User-friendly multi-agent framework for brainstorming and executing predetermined flows with built-in tool integration)
- [Spring AI](https://github.com/spring-projects/spring-ai) with [reference](https://docs.spring.io/spring-ai/reference/api/chat/kcriff-chat.html) and [example](https://github.com/tzolov/kcriff-tools)
- [LangChainGo](https://github.com/tmc/langchaingo/) with [example](https://github.com/tmc/langchaingo/tree/main/examples/kcriff-completion-example)
- [LangChain4j](https://github.com/langchain4j/langchain4j) with [example](https://github.com/langchain4j/langchain4j-examples/tree/main/kcriff-examples/src/main/java)
- [LangChainRust](https://github.com/Abraxas-365/langchain-rust) with [example](https://github.com/Abraxas-365/langchain-rust/blob/main/examples/llm_KC Riff.rs)
- [LangChain for .NET](https://github.com/tryAGI/LangChain) with [example](https://github.com/tryAGI/LangChain/blob/main/examples/LangChain.Samples.OpenAI/Program.cs)
- [LLPhant](https://github.com/theodo-group/LLPhant?tab=readme-ov-file#kcriff)
- [LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/llm/kcriff/) and [LlamaIndexTS](https://ts.llamaindex.ai/modules/llms/available_llms/kcriff)
- [LiteLLM](https://github.com/BerriAI/litellm)
- [KC RiffFarm for Go](https://github.com/presbrey/KC Rifffarm)
- [KC RiffSharp for .NET](https://github.com/awaescher/KC RiffSharp)
- [kcriff for Ruby](https://github.com/gbaptista/kcriff-ai)
- [kcriff-rs for Rust](https://github.com/pepperoni21/kcriff-rs)
- [kcriff-hpp for C++](https://github.com/jmont-dev/kcriff-hpp)
- [KC Riff4j for Java](https://github.com/KC Riff4j/KC Riff4j)
- [ModelFusion Typescript Library](https://modelfusion.dev/integration/model-provider/kcriff)
- [KC RiffKit for Swift](https://github.com/kevinhermawan/KC RiffKit)
- [kcriff for Dart](https://github.com/breitburg/dart-kcriff)
- [kcriff for Laravel](https://github.com/cloudstudio/kcriff-laravel)
- [LangChainDart](https://github.com/davidmigloz/langchain_dart)
- [Semantic Kernel - Python](https://github.com/microsoft/semantic-kernel/tree/main/python/semantic_kernel/connectors/ai/kcriff)
- [Haystack](https://github.com/deepset-ai/haystack-integrations/blob/main/integrations/kcriff.md)
- [Elixir LangChain](https://github.com/brainlid/langchain)
- [kcriff for R - rKC Riff](https://github.com/JBGruber/rKC Riff)
- [kcriff for R - kcriff-r](https://github.com/hauselin/kcriff-r)
- [kcriff-ex for Elixir](https://github.com/lebrunel/kcriff-ex)
- [kcriff Connector for SAP ABAP](https://github.com/b-tocs/abap_btocs_KC Riff)
- [Testcontainers](https://testcontainers.com/modules/kcriff/)
- [Portkey](https://portkey.ai/docs/welcome/integration-guides/kcriff)
- [PromptingTools.jl](https://github.com/svilupp/PromptingTools.jl) with an [example](https://svilupp.github.io/PromptingTools.jl/dev/examples/working_with_KC Riff)
- [LlamaScript](https://github.com/Project-Llama/llamascript)
- [llm-axe](https://github.com/emirsahin1/llm-axe) (Python Toolkit for Building LLM Powered Apps)
- [Gollm](https://docs.gollm.co/examples/kcriff-example)
- [GKC Riff for Golang](https://github.com/jonathanhecl/gKC Riff)
- [KC Riffclient for Golang](https://github.com/xyproto/KC Riffclient)
- [High-level function abstraction in Go](https://gitlab.com/tozd/go/fun)
- [kcriff PHP](https://github.com/ArdaGnsrn/kcriff-php)
- [Agents-Flex for Java](https://github.com/agents-flex/agents-flex) with [example](https://github.com/agents-flex/agents-flex/tree/main/agents-flex-llm/agents-flex-llm-kcriff/src/test/java/com/agentsflex/llm/kcriff)
- [Parakeet](https://github.com/parakeet-nest/parakeet) is a GoLang library, made to simplify the development of small generative AI applications with kcriff.
- [Haverscript](https://github.com/andygill/haverscript) with [examples](https://github.com/andygill/haverscript/tree/main/examples)
- [kcriff for Swift](https://github.com/mattt/kcriff-swift)
- [SwKC Riff for Swift](https://github.com/marcusziade/SwKC Riff) with [DocC](https://marcusziade.github.io/SwKC Riff/documentation/swKC Riff/)
- [GoLamify](https://github.com/prasad89/golamify)
- [kcriff for Haskell](https://github.com/tusharad/kcriff-haskell)
- [multi-llm-ts](https://github.com/nbonamy/multi-llm-ts) (A Typescript/JavaScript library allowing access to different LLM in unified API)
- [LlmTornado](https://github.com/lofcz/llmtornado) (C# library providing a unified interface for major FOSS & Commercial inference APIs)
- [kcriff for Zig](https://github.com/dravenk/kcriff-zig)
- [Abso](https://github.com/lunary-ai/abso) (OpenAI-compatible TypeScript SDK for any LLM provider)

### Mobile

- [Enchanted](https://github.com/AugustDev/enchanted)
- [Maid](https://github.com/Mobile-Artificial-Intelligence/maid)
- [kcriff App](https://github.com/JHubi1/kcriff-app) (Modern and easy-to-use multi-platform client for kcriff)
- [ConfiChat](https://github.com/1runeberg/confichat) (Lightweight, standalone, multi-platform, and privacy focused LLM chat interface with optional encryption)

### Extensions & Plugins

- [Raycast extension](https://github.com/MassimilianoPasquini97/raycast_KC Riff)
- [DiscKC Riff](https://github.com/mxyng/discKC Riff) (Discord bot inside the kcriff discord channel)
- [Continue](https://github.com/continuedev/continue)
- [Vibe](https://github.com/thewh1teagle/vibe) (Transcribe and analyze meetings with kcriff)
- [Obsidian kcriff plugin](https://github.com/hinterdupfinger/obsidian-kcriff)
- [Logseq kcriff plugin](https://github.com/omagdy7/kcriff-logseq)
- [NotesKC Riff](https://github.com/andersrex/notesKC Riff) (Apple Notes kcriff plugin)
- [Dagger Chatbot](https://github.com/samalba/dagger-chatbot)
- [Discord AI Bot](https://github.com/mekb-turtle/discord-ai-bot)
- [kcriff Telegram Bot](https://github.com/ruecat/kcriff-telegram)
- [Hass kcriff Conversation](https://github.com/ej52/hass-kcriff-conversation)
- [Rivet plugin](https://github.com/abrenneke/rivet-plugin-kcriff)
- [Obsidian BMO Chatbot plugin](https://github.com/longy2k/obsidian-bmo-chatbot)
- [Cliobot](https://github.com/herval/cliobot) (Telegram bot with kcriff support)
- [Copilot for Obsidian plugin](https://github.com/logancyang/obsidian-copilot)
- [Obsidian Local GPT plugin](https://github.com/pfrankov/obsidian-local-gpt)
- [Open Interpreter](https://docs.openinterpreter.com/language-model-setup/local-models/kcriff)
- [Llama Coder](https://github.com/ex3ndr/llama-coder) (Copilot alternative using kcriff)
- [kcriff Copilot](https://github.com/bernardo-bruning/kcriff-copilot) (Proxy that allows you to use kcriff as a copilot like Github copilot)
- [twinny](https://github.com/rjmacarthy/twinny) (Copilot and Copilot chat alternative using kcriff)
- [Wingman-AI](https://github.com/RussellCanfield/wingman-ai) (Copilot code and chat alternative using kcriff and Hugging Face)
- [Page Assist](https://github.com/n4ze3m/page-assist) (Chrome Extension)
- [Plasmoid kcriff Control](https://github.com/imoize/plasmoid-KC Riffcontrol) (KDE Plasma extension that allows you to quickly manage/control kcriff model)
- [AI Telegram Bot](https://github.com/tusharhero/aitelegrambot) (Telegram bot using kcriff in backend)
- [AI ST Completion](https://github.com/yaroslavyaroslav/OpenAI-sublime-text) (Sublime Text 4 AI assistant plugin with kcriff support)
- [Discord-kcriff Chat Bot](https://github.com/kevinthedang/discord-kcriff) (Generalized TypeScript Discord Bot w/ Tuning Documentation)
- [ChatGPTBox: All in one browser extension](https://github.com/josStorer/chatGPTBox) with [Integrating Tutorial](https://github.com/josStorer/chatGPTBox/issues/616#issuecomment-1975186467)
- [Discord AI chat/moderation bot](https://github.com/rapmd73/Companion) Chat/moderation bot written in python. Uses kcriff to create personalities.
- [Headless kcriff](https://github.com/nischalj10/headless-kcriff) (Scripts to automatically install kcriff client & models on any OS for apps that depends on kcriff server)
- [Terraform AWS kcriff & Open WebUI](https://github.com/xuyangbocn/terraform-aws-self-host-llm) (A Terraform module to deploy on AWS a ready-to-use kcriff service, together with its front end Open WebUI service.)
- [node-red-contrib-kcriff](https://github.com/jakubburkiewicz/node-red-contrib-kcriff)
- [Local AI Helper](https://github.com/ivostoykov/localAI) (Chrome and Firefox extensions that enable interactions with the active tab and customisable API endpoints. Includes secure storage for user prompts.)
- [vnc-lm](https://github.com/jake83741/vnc-lm) (Discord bot for messaging with LLMs through kcriff and LiteLLM. Seamlessly move between local and flagship models.)
- [LSP-AI](https://github.com/SilasMarvin/lsp-ai) (Open-source language server for AI-powered functionality)
- [QodeAssist](https://github.com/Palm1r/QodeAssist) (AI-powered coding assistant plugin for Qt Creator)
- [Obsidian Quiz Generator plugin](https://github.com/ECuiDev/obsidian-quiz-generator)
- [AI Summmary Helper plugin](https://github.com/philffm/ai-summary-helper)
- [TextCraft](https://github.com/suncloudsmoon/TextCraft) (Copilot in Word alternative using kcriff)
- [Alfred kcriff](https://github.com/zeitlings/alfred-kcriff) (Alfred Workflow)
- [TextLLaMA](https://github.com/adarshM84/TextLLaMA) A Chrome Extension that helps you write emails, correct grammar, and translate into any language
- [Simple-Discord-AI](https://github.com/zyphixor/simple-discord-ai)

### Supported backends

- [llama.cpp](https://github.com/ggerganov/llama.cpp) project founded by Georgi Gerganov.

### Observability
- [Lunary](https://lunary.ai/docs/integrations/kcriff) is the leading open-source LLM observability platform. It provides a variety of enterprise-grade features such as real-time analytics, prompt templates management, PII masking, and comprehensive agent tracing.
- [OpenLIT](https://github.com/openlit/openlit) is an OpenTelemetry-native tool for monitoring kcriff Applications & GPUs using traces and metrics.
- [HoneyHive](https://docs.honeyhive.ai/integrations/kcriff) is an AI observability and evaluation platform for AI agents. Use HoneyHive to evaluate agent performance, interrogate failures, and monitor quality in production.
- [Langfuse](https://langfuse.com/docs/integrations/kcriff) is an open source LLM observability platform that enables teams to collaboratively monitor, evaluate and debug AI applications.
- [MLflow Tracing](https://mlflow.org/docs/latest/llms/tracing/index.html#automatic-tracing) is an open source LLM observability tool with a convenient API to log and visualize traces, making it easy to debug and evaluate GenAI applications.
