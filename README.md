<div align="center">
  <a href="https://KC Riff.com" />
    <img alt="KC Riff" height="200px" src="https://github.com/KC Riff/KC Riff/assets/3325447/0d0b44e2-8f4a-4e99-9b52-a5c1c741c8f7">
  </a>
</div>

# KC Riff

Get up and running with large language models.

### macOS

[Download](https://KC Riff.com/download/KC Riff-darwin.zip)

### Windows

[Download](https://KC Riff.com/download/KC RiffSetup.exe)

### Linux

```shell
curl -fsSL https://KC Riff.com/install.sh | sh
```

[Manual install instructions](https://github.com/KC Riff/KC Riff/blob/main/docs/linux.md)

### Docker

The official [KC Riff Docker image](https://hub.docker.com/r/KC Riff/KC Riff) `KC Riff/KC Riff` is available on Docker Hub.

### Libraries

- [KC Riff-python](https://github.com/KC Riff/KC Riff-python)
- [KC Riff-js](https://github.com/KC Riff/KC Riff-js)

### Community

- [Discord](https://discord.gg/KC Riff)
- [Reddit](https://reddit.com/r/KC Riff)

## Quickstart

To run and chat with [Llama 3.2](https://KC Riff.com/library/llama3.2):

```shell
KC Riff run llama3.2
```

## Model library

KC Riff supports a list of models available on [KC Riff.com/library](https://KC Riff.com/library 'KC Riff model library')

Here are some example models that can be downloaded:

| Model              | Parameters | Size  | Download                         |
| ------------------ | ---------- | ----- | -------------------------------- |
| DeepSeek-R1        | 7B         | 4.7GB | `KC Riff run deepseek-r1`         |
| DeepSeek-R1        | 671B       | 404GB | `KC Riff run deepseek-r1:671b`    |
| Llama 3.3          | 70B        | 43GB  | `KC Riff run llama3.3`            |
| Llama 3.2          | 3B         | 2.0GB | `KC Riff run llama3.2`            |
| Llama 3.2          | 1B         | 1.3GB | `KC Riff run llama3.2:1b`         |
| Llama 3.2 Vision   | 11B        | 7.9GB | `KC Riff run llama3.2-vision`     |
| Llama 3.2 Vision   | 90B        | 55GB  | `KC Riff run llama3.2-vision:90b` |
| Llama 3.1          | 8B         | 4.7GB | `KC Riff run llama3.1`            |
| Llama 3.1          | 405B       | 231GB | `KC Riff run llama3.1:405b`       |
| Phi 4              | 14B        | 9.1GB | `KC Riff run phi4`                |
| Phi 3 Mini         | 3.8B       | 2.3GB | `KC Riff run phi3`                |
| Gemma 2            | 2B         | 1.6GB | `KC Riff run gemma2:2b`           |
| Gemma 2            | 9B         | 5.5GB | `KC Riff run gemma2`              |
| Gemma 2            | 27B        | 16GB  | `KC Riff run gemma2:27b`          |
| Mistral            | 7B         | 4.1GB | `KC Riff run mistral`             |
| Moondream 2        | 1.4B       | 829MB | `KC Riff run moondream`           |
| Neural Chat        | 7B         | 4.1GB | `KC Riff run neural-chat`         |
| Starling           | 7B         | 4.1GB | `KC Riff run starling-lm`         |
| Code Llama         | 7B         | 3.8GB | `KC Riff run codellama`           |
| Llama 2 Uncensored | 7B         | 3.8GB | `KC Riff run llama2-uncensored`   |
| LLaVA              | 7B         | 4.5GB | `KC Riff run llava`               |
| Solar              | 10.7B      | 6.1GB | `KC Riff run solar`               |

> [!NOTE]
> You should have at least 8 GB of RAM available to run the 7B models, 16 GB to run the 13B models, and 32 GB to run the 33B models.

## Customize a model

### Import from GGUF

KC Riff supports importing GGUF models in the Modelfile:

1. Create a file named `Modelfile`, with a `FROM` instruction with the local filepath to the model you want to import.

   ```
   FROM ./vicuna-33b.Q4_0.gguf
   ```

2. Create the model in KC Riff

   ```shell
   KC Riff create example -f Modelfile
   ```

3. Run the model

   ```shell
   KC Riff run example
   ```

### Import from Safetensors

See the [guide](docs/import.md) on importing models for more information.

### Customize a prompt

Models from the KC Riff library can be customized with a prompt. For example, to customize the `llama3.2` model:

```shell
KC Riff pull llama3.2
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
KC Riff create mario -f ./Modelfile
KC Riff run mario
>>> hi
Hello! It's your friend Mario.
```

For more information on working with a Modelfile, see the [Modelfile](docs/modelfile.md) documentation.

## CLI Reference

### Create a model

`KC Riff create` is used to create a model from a Modelfile.

```shell
KC Riff create mymodel -f ./Modelfile
```

### Pull a model

```shell
KC Riff pull llama3.2
```

> This command can also be used to update a local model. Only the diff will be pulled.

### Remove a model

```shell
KC Riff rm llama3.2
```

### Copy a model

```shell
KC Riff cp llama3.2 my-model
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
KC Riff run llava "What's in this image? /Users/jmorgan/Desktop/smile.png"
```

> **Output**: The image features a yellow smiley face, which is likely the central focus of the picture.

### Pass the prompt as an argument

```shell
KC Riff run llama3.2 "Summarize this file: $(cat README.md)"
```

> **Output**: KC Riff is a lightweight, extensible framework for building and running language models on the local machine. It provides a simple API for creating, running, and managing models, as well as a library of pre-built models that can be easily used in a variety of applications.

### Show model information

```shell
KC Riff show llama3.2
```

### List models on your computer

```shell
KC Riff list
```

### List which models are currently loaded

```shell
KC Riff ps
```

### Stop a model which is currently running

```shell
KC Riff stop llama3.2
```

### Start KC Riff

`KC Riff serve` is used when you want to start KC Riff without running the desktop application.

## Building

See the [developer guide](https://github.com/KC Riff/KC Riff/blob/main/docs/development.md)

### Running local builds

Next, start the server:

```shell
./KC Riff serve
```

Finally, in a separate shell, run a model:

```shell
./KC Riff run llama3.2
```

## REST API

KC Riff has a REST API for running and managing models.

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
- [HTML UI](https://github.com/rtcfirefly/KC Riff-ui)
- [Saddle](https://github.com/jikkuatwork/saddle)
- [Chatbot UI](https://github.com/ivanfioravanti/chatbot-KC Riff)
- [Chatbot UI v2](https://github.com/mckaywrigley/chatbot-ui)
- [Typescript UI](https://github.com/KC Riff-interface/KC Riff-Gui?tab=readme-ov-file)
- [Minimalistic React UI for KC Riff Models](https://github.com/richawo/minimal-llm-ui)
- [KC Riffc](https://github.com/kevinhermawan/KC Riffc)
- [big-AGI](https://github.com/enricoros/big-AGI/blob/main/docs/config-local-KC Riff.md)
- [Cheshire Cat assistant framework](https://github.com/cheshire-cat-ai/core)
- [Amica](https://github.com/semperai/amica)
- [chatd](https://github.com/BruceMacD/chatd)
- [KC Riff-SwiftUI](https://github.com/kghandour/KC Riff-SwiftUI)
- [Dify.AI](https://github.com/langgenius/dify)
- [MindMac](https://mindmac.app)
- [NextJS Web Interface for KC Riff](https://github.com/jakobhoeg/nextjs-KC Riff-llm-ui)
- [Msty](https://msty.app)
- [Chatbox](https://github.com/Bin-Huang/Chatbox)
- [WinForm KC Riff Copilot](https://github.com/tgraupmann/WinForm_KC Riff_Copilot)
- [NextChat](https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web) with [Get Started Doc](https://docs.nextchat.dev/models/KC Riff)
- [Alpaca WebUI](https://github.com/mmo80/alpaca-webui)
- [KC RiffGUI](https://github.com/enoch1118/KC RiffGUI)
- [OpenAOE](https://github.com/InternLM/OpenAOE)
- [Odin Runes](https://github.com/leonid20000/OdinRunes)
- [LLM-X](https://github.com/mrdjohnson/llm-x) (Progressive Web App)
- [AnythingLLM (Docker + MacOs/Windows/Linux native app)](https://github.com/Mintplex-Labs/anything-llm)
- [KC Riff Basic Chat: Uses HyperDiv Reactive UI](https://github.com/rapidarchitect/KC Riff_basic_chat)
- [KC Riff-chats RPG](https://github.com/drazdra/KC Riff-chats)
- [IntelliBar](https://intellibar.app/) (AI-powered assistant for macOS)
- [QA-Pilot](https://github.com/reid41/QA-Pilot) (Interactive chat tool that can leverage KC Riff models for rapid understanding and navigation of GitHub code repositories)
- [ChatKC Riff](https://github.com/sugarforever/chat-KC Riff) (Open Source Chatbot based on KC Riff with Knowledge Bases)
- [CRAG KC Riff Chat](https://github.com/Nagi-ovo/CRAG-KC Riff-Chat) (Simple Web Search with Corrective RAG)
- [RAGFlow](https://github.com/infiniflow/ragflow) (Open-source Retrieval-Augmented Generation engine based on deep document understanding)
- [StreamDeploy](https://github.com/StreamDeploy-DevRel/streamdeploy-llm-app-scaffold) (LLM Application Scaffold)
- [chat](https://github.com/swuecho/chat) (chat web app for teams)
- [Lobe Chat](https://github.com/lobehub/lobe-chat) with [Integrating Doc](https://lobehub.com/docs/self-hosting/examples/KC Riff)
- [KC Riff RAG Chatbot](https://github.com/datvodinh/rag-chatbot.git) (Local Chat with multiple PDFs using KC Riff and RAG)
- [BrainSoup](https://www.nurgo-software.com/products/brainsoup) (Flexible native client with RAG & multi-agent automation)
- [macai](https://github.com/Renset/macai) (macOS client for KC Riff, ChatGPT, and other compatible API back-ends)
- [RWKV-Runner](https://github.com/josStorer/RWKV-Runner) (RWKV offline LLM deployment tool, also usable as a client for ChatGPT and KC Riff)
- [KC Riff Grid Search](https://github.com/dezoito/KC Riff-grid-search) (app to evaluate and compare models)
- [Olpaka](https://github.com/Otacon/olpaka) (User-friendly Flutter Web App for KC Riff)
- [KC RiffSpring](https://github.com/CrazyNeil/KC RiffSpring) (KC Riff Client for macOS)
- [LLocal.in](https://github.com/kartikm7/llocal) (Easy to use Electron Desktop Client for KC Riff)
- [Shinkai Desktop](https://github.com/dcSpark/shinkai-apps) (Two click install Local AI using KC Riff + Files + RAG)
- [AiLama](https://github.com/zeyoyt/ailama) (A Discord User App that allows you to interact with KC Riff anywhere in discord )
- [KC Riff with Google Mesop](https://github.com/rapidarchitect/KC Riff_mesop/) (Mesop Chat Client implementation with KC Riff)
- [R2R](https://github.com/SciPhi-AI/R2R) (Open-source RAG engine)
- [KC Riff-Kis](https://github.com/elearningshow/KC Riff-kis) (A simple easy to use GUI with sample custom LLM for Drivers Education)
- [OpenGPA](https://opengpa.org) (Open-source offline-first Enterprise Agentic Application)
- [Painting Droid](https://github.com/mateuszmigas/painting-droid) (Painting app with AI integrations)
- [Kerlig AI](https://www.kerlig.com/) (AI writing assistant for macOS)
- [AI Studio](https://github.com/MindWorkAI/AI-Studio)
- [Sidellama](https://github.com/gyopak/sidellama) (browser-based LLM client)
- [LLMStack](https://github.com/trypromptly/LLMStack) (No-code multi-agent framework to build LLM agents and workflows)
- [BoltAI for Mac](https://boltai.com) (AI Chat Client for Mac)
- [Harbor](https://github.com/av/harbor) (Containerized LLM Toolkit with KC Riff as default backend)
- [PyGPT](https://github.com/szczyglis-dev/py-gpt) (AI desktop assistant for Linux, Windows and Mac)
- [Alpaca](https://github.com/Jeffser/Alpaca) (An KC Riff client application for linux and macos made with GTK4 and Adwaita)
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT/blob/master/docs/content/platform/KC Riff.md) (AutoGPT KC Riff integration)
- [Go-CREW](https://www.jonathanhecl.com/go-crew/) (Powerful Offline RAG in Golang)
- [PartCAD](https://github.com/openvmp/partcad/) (CAD model generation with OpenSCAD and CadQuery)
- [KC Riff4j Web UI](https://github.com/KC Riff4j/KC Riff4j-web-ui) - Java-based Web UI for KC Riff built with Vaadin, Spring Boot and KC Riff4j
- [PyOllaMx](https://github.com/kspviswa/pyOllaMx) - macOS application capable of chatting with both KC Riff and Apple MLX models.
- [Claude Dev](https://github.com/saoudrizwan/claude-dev) - VSCode extension for multi-file/whole-repo coding
- [Cherry Studio](https://github.com/kangfenmao/cherry-studio) (Desktop client with KC Riff support)
- [ConfiChat](https://github.com/1runeberg/confichat) (Lightweight, standalone, multi-platform, and privacy focused LLM chat interface with optional encryption)
- [Archyve](https://github.com/nickthecook/archyve) (RAG-enabling document library)
- [crewAI with Mesop](https://github.com/rapidarchitect/KC Riff-crew-mesop) (Mesop Web Interface to run crewAI with KC Riff)
- [Tkinter-based client](https://github.com/chyok/KC Riff-gui) (Python tkinter-based Client for KC Riff)
- [LLMChat](https://github.com/trendy-design/llmchat) (Privacy focused, 100% local, intuitive all-in-one chat interface)
- [Local Multimodal AI Chat](https://github.com/Leon-Sander/Local-Multimodal-AI-Chat) (KC Riff-based LLM Chat with support for multiple features, including PDF RAG, voice chat, image-based interactions, and integration with OpenAI.)
- [ARGO](https://github.com/xark-argo/argo) (Locally download and run KC Riff and Huggingface models with RAG on Mac/Windows/Linux)
- [OrionChat](https://github.com/EliasPereirah/OrionChat) - OrionChat is a web interface for chatting with different AI providers
- [G1](https://github.com/bklieger-groq/g1) (Prototype of using prompting strategies to improve the LLM's reasoning through o1-like reasoning chains.)
- [Web management](https://github.com/lemonit-eric-mao/KC Riff-web-management) (Web management page)
- [Promptery](https://github.com/promptery/promptery) (desktop client for KC Riff.)
- [KC Riff App](https://github.com/JHubi1/KC Riff-app) (Modern and easy-to-use multi-platform client for KC Riff)
- [chat-KC Riff](https://github.com/annilq/chat-KC Riff) (a React Native client for KC Riff)
- [SpaceLlama](https://github.com/tcsenpai/spacellama) (Firefox and Chrome extension to quickly summarize web pages with KC Riff in a sidebar)
- [YouLama](https://github.com/tcsenpai/youlama) (Webapp to quickly summarize any YouTube video, supporting Invidious as well)
- [DualMind](https://github.com/tcsenpai/dualmind) (Experimental app allowing two models to talk to each other in the terminal or in a web interface)
- [KC Rifframa-matrix](https://github.com/h1ddenpr0cess20/KC Rifframa-matrix) (KC Riff chatbot for the Matrix chat protocol)
- [KC Riff-chat-app](https://github.com/anan1213095357/KC Riff-chat-app) (Flutter-based chat app)
- [Perfect Memory AI](https://www.perfectmemory.ai/) (Productivity AI assists personalized by what you have seen on your screen, heard and said in the meetings)
- [Hexabot](https://github.com/hexastack/hexabot) (A conversational AI builder)
- [Reddit Rate](https://github.com/rapidarchitect/reddit_analyzer) (Search and Rate Reddit topics with a weighted summation)
- [OpenTalkGpt](https://github.com/adarshM84/OpenTalkGpt) (Chrome Extension to manage open-source models supported by KC Riff, create custom models, and chat with models from a user-friendly UI)
- [VT](https://github.com/vinhnx/vt.ai) (A minimal multimodal AI chat app, with dynamic conversation routing. Supports local models via KC Riff)
- [Nosia](https://github.com/nosia-ai/nosia) (Easy to install and use RAG platform based on KC Riff)
- [Witsy](https://github.com/nbonamy/witsy) (An AI Desktop application available for Mac/Windows/Linux)
- [Abbey](https://github.com/US-Artificial-Intelligence/abbey) (A configurable AI interface server with notebooks, document storage, and YouTube support)
- [Minima](https://github.com/dmayboroda/minima) (RAG with on-premises or fully local workflow)
- [aidful-KC Riff-model-delete](https://github.com/AidfulAI/aidful-KC Riff-model-delete) (User interface for simplified model cleanup)
- [Perplexica](https://github.com/ItzCrazyKns/Perplexica) (An AI-powered search engine & an open-source alternative to Perplexity AI)
- [KC Riff Chat WebUI for Docker ](https://github.com/oslook/KC Riff-webui) (Support for local docker deployment, lightweight KC Riff webui)
- [AI Toolkit for Visual Studio Code](https://aka.ms/ai-tooklit/KC Riff-docs) (Microsoft-official VSCode extension to chat, test, evaluate models with KC Riff support, and use them in your AI applications.)
- [MinimalNextKC RiffChat](https://github.com/anilkay/MinimalNextKC RiffChat) (Minimal Web UI for Chat and Model Control)
- [Chipper](https://github.com/TilmanGriesel/chipper) AI interface for tinkerers (KC Riff, Haystack RAG, Python)
- [ChibiChat](https://github.com/CosmicEventHorizon/ChibiChat) (Kotlin-based Android app to chat with KC Riff and Koboldcpp API endpoints)
- [LocalLLM](https://github.com/qusaismael/localllm) (Minimal Web-App to run KC Riff models on it with a GUI)
- [KC Riffzing](https://github.com/buiducnhat/KC Riffzing) (Web extension to run KC Riff models)

### Cloud

- [Google Cloud](https://cloud.google.com/run/docs/tutorials/gpu-gemma2-with-KC Riff)
- [Fly.io](https://fly.io/docs/python/do-more/add-KC Riff/)
- [Koyeb](https://www.koyeb.com/deploy/KC Riff)

### Terminal

- [oterm](https://github.com/ggozad/oterm)
- [Ellama Emacs client](https://github.com/s-kostyaev/ellama)
- [Emacs client](https://github.com/zweifisch/KC Riff)
- [neKC Riff](https://github.com/paradoxical-dev/neKC Riff) UI client for interacting with models from within Neovim
- [gen.nvim](https://github.com/David-Kunz/gen.nvim)
- [KC Riff.nvim](https://github.com/nomnivore/KC Riff.nvim)
- [ollero.nvim](https://github.com/marco-souza/ollero.nvim)
- [KC Riff-chat.nvim](https://github.com/gerazov/KC Riff-chat.nvim)
- [ogpt.nvim](https://github.com/huynle/ogpt.nvim)
- [gptel Emacs client](https://github.com/karthink/gptel)
- [Oatmeal](https://github.com/dustinblackman/oatmeal)
- [cmdh](https://github.com/pgibler/cmdh)
- [ooo](https://github.com/npahlfer/ooo)
- [shell-pilot](https://github.com/reid41/shell-pilot)(Interact with models via pure shell scripts on Linux or macOS)
- [tenere](https://github.com/pythops/tenere)
- [llm-KC Riff](https://github.com/taketwo/llm-KC Riff) for [Datasette's LLM CLI](https://llm.datasette.io/en/stable/).
- [typechat-cli](https://github.com/anaisbetts/typechat-cli)
- [ShellOracle](https://github.com/djcopley/ShellOracle)
- [tlm](https://github.com/yusufcanb/tlm)
- [podman-KC Riff](https://github.com/ericcurtin/podman-KC Riff)
- [gKC Riff](https://github.com/sammcj/gKC Riff)
- [ParLlama](https://github.com/paulrobello/parllama)
- [KC Riff eBook Summary](https://github.com/cognitivetech/KC Riff-ebook-summary/)
- [KC Riff Mixture of Experts (MOE) in 50 lines of code](https://github.com/rapidarchitect/KC Riff_moe)
- [vim-intelligence-bridge](https://github.com/pepo-ec/vim-intelligence-bridge) Simple interaction of "KC Riff" with the Vim editor
- [x-cmd KC Riff](https://x-cmd.com/mod/KC Riff)
- [bb7](https://github.com/drunkwcodes/bb7)
- [SwKC RiffCLI](https://github.com/marcusziade/SwKC Riff) bundled with the SwKC Riff Swift package. [Demo](https://github.com/marcusziade/SwKC Riff?tab=readme-ov-file#cli-usage)
- [aichat](https://github.com/sigoden/aichat) All-in-one LLM CLI tool featuring Shell Assistant, Chat-REPL, RAG, AI tools & agents, with access to OpenAI, Claude, Gemini, KC Riff, Groq, and more.
- [PowershAI](https://github.com/rrg92/powershai) PowerShell module that brings AI to terminal on Windows, including support for KC Riff
- [orbiton](https://github.com/xyproto/orbiton) Configuration-free text editor and IDE with support for tab completion with KC Riff.

### Apple Vision Pro

- [Enchanted](https://github.com/AugustDev/enchanted)

### Database

- [pgai](https://github.com/timescale/pgai) - PostgreSQL as a vector database (Create and search embeddings from KC Riff models using pgvector)
   - [Get started guide](https://github.com/timescale/pgai/blob/main/docs/vectorizer-quick-start.md)
- [MindsDB](https://github.com/mindsdb/mindsdb/blob/staging/mindsdb/integrations/handlers/KC Riff_handler/README.md) (Connects KC Riff models with nearly 200 data platforms and apps)
- [chromem-go](https://github.com/philippgille/chromem-go/blob/v0.5.0/embed_KC Riff.go) with [example](https://github.com/philippgille/chromem-go/tree/v0.5.0/examples/rag-wikipedia-KC Riff)
- [Kangaroo](https://github.com/dbkangaroo/kangaroo) (AI-powered SQL client and admin tool for popular databases)

### Package managers

- [Pacman](https://archlinux.org/packages/extra/x86_64/KC Riff/)
- [Gentoo](https://github.com/gentoo/guru/tree/master/app-misc/KC Riff)
- [Homebrew](https://formulae.brew.sh/formula/KC Riff)
- [Helm Chart](https://artifacthub.io/packages/helm/KC Riff-helm/KC Riff)
- [Guix channel](https://codeberg.org/tusharhero/KC Riff-guix)
- [Nix package](https://search.nixos.org/packages?show=KC Riff&from=0&size=50&sort=relevance&type=packages&query=KC Riff)
- [Flox](https://flox.dev/blog/KC Riff-part-one)

### Libraries

- [LangChain](https://python.langchain.com/docs/integrations/llms/KC Riff) and [LangChain.js](https://js.langchain.com/docs/integrations/chat/KC Riff/) with [example](https://js.langchain.com/docs/tutorials/local_rag/)
- [Firebase Genkit](https://firebase.google.com/docs/genkit/plugins/KC Riff)
- [crewAI](https://github.com/crewAIInc/crewAI)
- [Yacana](https://remembersoftwares.github.io/yacana/) (User-friendly multi-agent framework for brainstorming and executing predetermined flows with built-in tool integration)
- [Spring AI](https://github.com/spring-projects/spring-ai) with [reference](https://docs.spring.io/spring-ai/reference/api/chat/KC Riff-chat.html) and [example](https://github.com/tzolov/KC Riff-tools)
- [LangChainGo](https://github.com/tmc/langchaingo/) with [example](https://github.com/tmc/langchaingo/tree/main/examples/KC Riff-completion-example)
- [LangChain4j](https://github.com/langchain4j/langchain4j) with [example](https://github.com/langchain4j/langchain4j-examples/tree/main/KC Riff-examples/src/main/java)
- [LangChainRust](https://github.com/Abraxas-365/langchain-rust) with [example](https://github.com/Abraxas-365/langchain-rust/blob/main/examples/llm_KC Riff.rs)
- [LangChain for .NET](https://github.com/tryAGI/LangChain) with [example](https://github.com/tryAGI/LangChain/blob/main/examples/LangChain.Samples.OpenAI/Program.cs)
- [LLPhant](https://github.com/theodo-group/LLPhant?tab=readme-ov-file#KC Riff)
- [LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/llm/KC Riff/) and [LlamaIndexTS](https://ts.llamaindex.ai/modules/llms/available_llms/KC Riff)
- [LiteLLM](https://github.com/BerriAI/litellm)
- [KC RiffFarm for Go](https://github.com/presbrey/KC Rifffarm)
- [KC RiffSharp for .NET](https://github.com/awaescher/KC RiffSharp)
- [KC Riff for Ruby](https://github.com/gbaptista/KC Riff-ai)
- [KC Riff-rs for Rust](https://github.com/pepperoni21/KC Riff-rs)
- [KC Riff-hpp for C++](https://github.com/jmont-dev/KC Riff-hpp)
- [KC Riff4j for Java](https://github.com/KC Riff4j/KC Riff4j)
- [ModelFusion Typescript Library](https://modelfusion.dev/integration/model-provider/KC Riff)
- [KC RiffKit for Swift](https://github.com/kevinhermawan/KC RiffKit)
- [KC Riff for Dart](https://github.com/breitburg/dart-KC Riff)
- [KC Riff for Laravel](https://github.com/cloudstudio/KC Riff-laravel)
- [LangChainDart](https://github.com/davidmigloz/langchain_dart)
- [Semantic Kernel - Python](https://github.com/microsoft/semantic-kernel/tree/main/python/semantic_kernel/connectors/ai/KC Riff)
- [Haystack](https://github.com/deepset-ai/haystack-integrations/blob/main/integrations/KC Riff.md)
- [Elixir LangChain](https://github.com/brainlid/langchain)
- [KC Riff for R - rKC Riff](https://github.com/JBGruber/rKC Riff)
- [KC Riff for R - KC Riff-r](https://github.com/hauselin/KC Riff-r)
- [KC Riff-ex for Elixir](https://github.com/lebrunel/KC Riff-ex)
- [KC Riff Connector for SAP ABAP](https://github.com/b-tocs/abap_btocs_KC Riff)
- [Testcontainers](https://testcontainers.com/modules/KC Riff/)
- [Portkey](https://portkey.ai/docs/welcome/integration-guides/KC Riff)
- [PromptingTools.jl](https://github.com/svilupp/PromptingTools.jl) with an [example](https://svilupp.github.io/PromptingTools.jl/dev/examples/working_with_KC Riff)
- [LlamaScript](https://github.com/Project-Llama/llamascript)
- [llm-axe](https://github.com/emirsahin1/llm-axe) (Python Toolkit for Building LLM Powered Apps)
- [Gollm](https://docs.gollm.co/examples/KC Riff-example)
- [GKC Riff for Golang](https://github.com/jonathanhecl/gKC Riff)
- [KC Riffclient for Golang](https://github.com/xyproto/KC Riffclient)
- [High-level function abstraction in Go](https://gitlab.com/tozd/go/fun)
- [KC Riff PHP](https://github.com/ArdaGnsrn/KC Riff-php)
- [Agents-Flex for Java](https://github.com/agents-flex/agents-flex) with [example](https://github.com/agents-flex/agents-flex/tree/main/agents-flex-llm/agents-flex-llm-KC Riff/src/test/java/com/agentsflex/llm/KC Riff)
- [Parakeet](https://github.com/parakeet-nest/parakeet) is a GoLang library, made to simplify the development of small generative AI applications with KC Riff.
- [Haverscript](https://github.com/andygill/haverscript) with [examples](https://github.com/andygill/haverscript/tree/main/examples)
- [KC Riff for Swift](https://github.com/mattt/KC Riff-swift)
- [SwKC Riff for Swift](https://github.com/marcusziade/SwKC Riff) with [DocC](https://marcusziade.github.io/SwKC Riff/documentation/swKC Riff/)
- [GoLamify](https://github.com/prasad89/golamify)
- [KC Riff for Haskell](https://github.com/tusharad/KC Riff-haskell)
- [multi-llm-ts](https://github.com/nbonamy/multi-llm-ts) (A Typescript/JavaScript library allowing access to different LLM in unified API)
- [LlmTornado](https://github.com/lofcz/llmtornado) (C# library providing a unified interface for major FOSS & Commercial inference APIs)
- [KC Riff for Zig](https://github.com/dravenk/KC Riff-zig)
- [Abso](https://github.com/lunary-ai/abso) (OpenAI-compatible TypeScript SDK for any LLM provider)

### Mobile

- [Enchanted](https://github.com/AugustDev/enchanted)
- [Maid](https://github.com/Mobile-Artificial-Intelligence/maid)
- [KC Riff App](https://github.com/JHubi1/KC Riff-app) (Modern and easy-to-use multi-platform client for KC Riff)
- [ConfiChat](https://github.com/1runeberg/confichat) (Lightweight, standalone, multi-platform, and privacy focused LLM chat interface with optional encryption)

### Extensions & Plugins

- [Raycast extension](https://github.com/MassimilianoPasquini97/raycast_KC Riff)
- [DiscKC Riff](https://github.com/mxyng/discKC Riff) (Discord bot inside the KC Riff discord channel)
- [Continue](https://github.com/continuedev/continue)
- [Vibe](https://github.com/thewh1teagle/vibe) (Transcribe and analyze meetings with KC Riff)
- [Obsidian KC Riff plugin](https://github.com/hinterdupfinger/obsidian-KC Riff)
- [Logseq KC Riff plugin](https://github.com/omagdy7/KC Riff-logseq)
- [NotesKC Riff](https://github.com/andersrex/notesKC Riff) (Apple Notes KC Riff plugin)
- [Dagger Chatbot](https://github.com/samalba/dagger-chatbot)
- [Discord AI Bot](https://github.com/mekb-turtle/discord-ai-bot)
- [KC Riff Telegram Bot](https://github.com/ruecat/KC Riff-telegram)
- [Hass KC Riff Conversation](https://github.com/ej52/hass-KC Riff-conversation)
- [Rivet plugin](https://github.com/abrenneke/rivet-plugin-KC Riff)
- [Obsidian BMO Chatbot plugin](https://github.com/longy2k/obsidian-bmo-chatbot)
- [Cliobot](https://github.com/herval/cliobot) (Telegram bot with KC Riff support)
- [Copilot for Obsidian plugin](https://github.com/logancyang/obsidian-copilot)
- [Obsidian Local GPT plugin](https://github.com/pfrankov/obsidian-local-gpt)
- [Open Interpreter](https://docs.openinterpreter.com/language-model-setup/local-models/KC Riff)
- [Llama Coder](https://github.com/ex3ndr/llama-coder) (Copilot alternative using KC Riff)
- [KC Riff Copilot](https://github.com/bernardo-bruning/KC Riff-copilot) (Proxy that allows you to use KC Riff as a copilot like Github copilot)
- [twinny](https://github.com/rjmacarthy/twinny) (Copilot and Copilot chat alternative using KC Riff)
- [Wingman-AI](https://github.com/RussellCanfield/wingman-ai) (Copilot code and chat alternative using KC Riff and Hugging Face)
- [Page Assist](https://github.com/n4ze3m/page-assist) (Chrome Extension)
- [Plasmoid KC Riff Control](https://github.com/imoize/plasmoid-KC Riffcontrol) (KDE Plasma extension that allows you to quickly manage/control KC Riff model)
- [AI Telegram Bot](https://github.com/tusharhero/aitelegrambot) (Telegram bot using KC Riff in backend)
- [AI ST Completion](https://github.com/yaroslavyaroslav/OpenAI-sublime-text) (Sublime Text 4 AI assistant plugin with KC Riff support)
- [Discord-KC Riff Chat Bot](https://github.com/kevinthedang/discord-KC Riff) (Generalized TypeScript Discord Bot w/ Tuning Documentation)
- [ChatGPTBox: All in one browser extension](https://github.com/josStorer/chatGPTBox) with [Integrating Tutorial](https://github.com/josStorer/chatGPTBox/issues/616#issuecomment-1975186467)
- [Discord AI chat/moderation bot](https://github.com/rapmd73/Companion) Chat/moderation bot written in python. Uses KC Riff to create personalities.
- [Headless KC Riff](https://github.com/nischalj10/headless-KC Riff) (Scripts to automatically install KC Riff client & models on any OS for apps that depends on KC Riff server)
- [Terraform AWS KC Riff & Open WebUI](https://github.com/xuyangbocn/terraform-aws-self-host-llm) (A Terraform module to deploy on AWS a ready-to-use KC Riff service, together with its front end Open WebUI service.)
- [node-red-contrib-KC Riff](https://github.com/jakubburkiewicz/node-red-contrib-KC Riff)
- [Local AI Helper](https://github.com/ivostoykov/localAI) (Chrome and Firefox extensions that enable interactions with the active tab and customisable API endpoints. Includes secure storage for user prompts.)
- [vnc-lm](https://github.com/jake83741/vnc-lm) (Discord bot for messaging with LLMs through KC Riff and LiteLLM. Seamlessly move between local and flagship models.)
- [LSP-AI](https://github.com/SilasMarvin/lsp-ai) (Open-source language server for AI-powered functionality)
- [QodeAssist](https://github.com/Palm1r/QodeAssist) (AI-powered coding assistant plugin for Qt Creator)
- [Obsidian Quiz Generator plugin](https://github.com/ECuiDev/obsidian-quiz-generator)
- [AI Summmary Helper plugin](https://github.com/philffm/ai-summary-helper)
- [TextCraft](https://github.com/suncloudsmoon/TextCraft) (Copilot in Word alternative using KC Riff)
- [Alfred KC Riff](https://github.com/zeitlings/alfred-KC Riff) (Alfred Workflow)
- [TextLLaMA](https://github.com/adarshM84/TextLLaMA) A Chrome Extension that helps you write emails, correct grammar, and translate into any language
- [Simple-Discord-AI](https://github.com/zyphixor/simple-discord-ai)

### Supported backends

- [llama.cpp](https://github.com/ggerganov/llama.cpp) project founded by Georgi Gerganov.

### Observability
- [Lunary](https://lunary.ai/docs/integrations/KC Riff) is the leading open-source LLM observability platform. It provides a variety of enterprise-grade features such as real-time analytics, prompt templates management, PII masking, and comprehensive agent tracing.
- [OpenLIT](https://github.com/openlit/openlit) is an OpenTelemetry-native tool for monitoring KC Riff Applications & GPUs using traces and metrics.
- [HoneyHive](https://docs.honeyhive.ai/integrations/KC Riff) is an AI observability and evaluation platform for AI agents. Use HoneyHive to evaluate agent performance, interrogate failures, and monitor quality in production.
- [Langfuse](https://langfuse.com/docs/integrations/KC Riff) is an open source LLM observability platform that enables teams to collaboratively monitor, evaluate and debug AI applications.
- [MLflow Tracing](https://mlflow.org/docs/latest/llms/tracing/index.html#automatic-tracing) is an open source LLM observability tool with a convenient API to log and visualize traces, making it easy to debug and evaluate GenAI applications.
