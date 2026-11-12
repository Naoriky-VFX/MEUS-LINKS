"""Site de links em PASTAS: grupo -> subpasta (Consoles/PS5, IA/Agentes...).

Cada pasta tem seu index.html com uma tabela. Fonte: favoritos do Firefox
(github.com / gitlab.com) + L2J oficial (Bitbucket).
"""
import html
import json
import os
import shutil

RAIZ = r"D:\PROJETOS DE PROGRAMAÇÃO\LINKS-NAORIKY"
FONTE = r"C:\Users\danie\AppData\Local\Temp\opencode\github-itens.json"

# (pasta) -> lista de (nome, descricao)
ITENS = {
    "consoles/switch": [
        ("Atmosphere-NX/Atmosphere", "Custom firmware do Switch: é o desbloqueio em si."),
        ("CTCaer/hekate", "Bootloader/payload do Switch, base de quase todo desbloqueio."),
        ("WerWolv/Hekate-Toolbox", "Manutenção pelo hekate: backup de partições, eMMC, etc."),
        ("eliboa/TegraRcmGUI", "Manda o payload do desbloqueio para o Switch pelo PC (RCM)."),
        ("shchmue/Lockpick_RCM", "Extrai as chaves do Switch (necessário para vários programas)."),
        ("blawar/tinleaf", "Instalador de NSP/NSZ no Switch (cartão ou rede)."),
        ("ITotalJustice/sigpatch-updater", "Baixa e atualiza os sigpatches do Atmosphere."),
        ("HamletDuFromage/aio-switch-updater", "Atualiza firmware, sigpatches e homebrews num app só."),
        ("rashevskyv/switch", "Pacote KEFIR: arquivos de desbloqueio prontos."),
        ("FlagBrew/Checkpoint", "Backup e restauração de saves do Switch."),
        ("julesontheroad/NSC_BUILDER", "Converte e monta NSP/XCI do Switch no PC."),
        ("ndeadly/MissionControl", "Usa controles de PS/Xbox no Switch por Bluetooth."),
        ("cathery/sys-con", "Sysmodule para controles genéricos no Switch."),
        ("AMSNX/cnxpack-updater", "Atualizador de pacotes do CNX (CFW alternativo)."),
    ],
    "consoles/switch-2": [
        ("misshexa66/OunceCake", "Extrai romFS/exeFS não criptografados de jogos do Switch 2."),
    ],
    "consoles/playstation-4": [
        ("diegolix29/shadPS4", "Emulador de PS4 para PC."),
    ],
    "consoles/playstation-5": [
        ("KytyPS5/KytyPS5", "Camada de tradução de PS5 para Windows/Linux/macOS (experimental)."),
        ("drakmor/ShadowMountPlus", "Payload que monta discos externos sozinho no PS5 desbloqueado."),
        ("notmaj0r/Y2JB", "Execução de código no PS5 pelo app do YouTube (jailbreak)."),
        ("leolobato/playden-ps5", "Roda jogos Windows da Steam na biblioteca do PS5 desbloqueado."),
    ],
    "consoles/ps-vita": [
        ("blastrock/pkgj", "PKGj: instala jogos e DLCs direto no PS Vita."),
    ],
    "consoles/wii-u": [
        ("slashiee.github.io/cemu_graphic_packs", "Graphic packs do Cemu (emulador de Wii U): texturas e resolução melhores."),
    ],

    "servidores/lineage-ii": [
        ("L2J oficial · game server", "Core do servidor L2J oficial (Java). Mantido no Bitbucket."),
        ("L2J oficial · datapack", "Datapack oficial: NPCs, quests, scripts e configuração do mundo."),
        ("L2J oficial · login server", "Login server oficial (autenticação das contas)."),
        ("L2J oficial · commons", "Biblioteca comum usada pelo game e pelo login."),
        ("L2J oficial · docker", "Docker com game + login + banco prontos para subir."),
        ("L2J · site oficial", "Site do L2J: downloads, fórum e documentação."),
        ("MobiusDevelopment/L2J_Mobius", "L2J Mobius: servidor de Lineage II (Interlude/Essence e derivados)."),
        ("MobiusDevelopment/l2clientdat", "Editor de L2ClientDat (arquivos .dat do cliente)."),
        ("L2Miko/L2FileEdit", "L2FileEdit: edita arquivos do cliente Lineage II."),
    ],
    "servidores/palworld": [
        ("jammsen/docker-palworld-dedicated-server", "Servidor dedicado de Palworld em Docker."),
        ("xNul/palworld-host-save-fix", "Corrige o bug de save do Palworld em servidor."),
        ("deafdudecomputers/PalWorldSaveTools", "Ferramentas para editar/converter saves do Palworld."),
    ],

    "ia/terminal": [
        ("google-gemini/gemini-cli", "108k★ · agente de IA do Gemini direto no terminal."),
        ("OpenHands/OpenHands", "93k★ · agente que escreve, testa e corrige software sozinho."),
        ("cline/cline", "71k★ · agente que programa dentro do editor/CLI e pede aprovação."),
        ("openinterpreter/openinterpreter", "68k★ · escreve e roda código na sua máquina pra cumprir a tarefa."),
        ("herdrdev/herdr", "50k★ · runtime onde os agentes de código rodam em paralelo."),
        ("Aider-AI/aider", "50k★ · pair programming de IA no terminal (edita seu repositório)."),
        ("QwenLM/qwen-code", "29k★ · agente de código da Qwen que vive no terminal."),
        ("manaflow-ai/cmux", "28k★ · terminal com abas verticais e avisos para agentes."),
        ("plandex-ai/plandex", "15k★ · agente para projetos grandes, com plano e contexto."),
        ("TheR1D/shell_gpt", "12k★ · comandos e respostas de IA no shell."),
        ("smtg-ai/claude-squad", "8.7k★ · gerencia vários agentes de terminal ao mesmo tempo."),
        ("graykode/abtop", "3.8k★ · “htop dos agentes”: tokens e sessões em tempo real."),
        ("SeemSeam/claude_codex_bridge", "3.6k★ · mistura Codex, Claude, Gemini e Kimi num workspace só."),
    ],
    "ia/api": [
        ("firecrawl/firecrawl", "201k★ · qualquer site vira conteúdo limpo pra IA (crawl + MCP)."),
        ("microsoft/markitdown", "195k★ · PDF, Word, Excel e PowerPoint viram texto limpo pra IA."),
        ("browser-use/browser-use", "120k★ · agente que clica, preenche e pesquisa no navegador."),
        ("punkpeye/awesome-mcp-servers", "97k★ · catálogo gigante de servidores MCP."),
        ("modelcontextprotocol/servers", "91k★ · servidores MCP de referência (oficial)."),
        ("zylon-ai/private-gpt", "57k★ · API completa de IA privada em cima de modelos locais."),
        ("microsoft/playwright-mcp", "39k★ · MCP oficial do Playwright (automação de navegador)."),
        ("github/github-mcp-server", "34k★ · MCP oficial do GitHub (repos, issues, PRs)."),
        ("PrefectHQ/fastmcp", "28k★ · jeito rápido de criar servidor/cliente MCP em Python."),
        ("activepieces/activepieces", "25k★ · automação com ~400 MCPs prontos."),
        ("modelcontextprotocol/python-sdk", "24k★ · SDK oficial de MCP para Python."),
        ("czlonkowski/n8n-mcp", "23k★ · MCP que deixa a IA montar/editar fluxos do n8n."),
        ("tashfeenahmed/freellmapi", "34 provedores de LLM grátis e 635 endpoints numa API só."),
        ("Mans230/dsh-llm-cli", "Roteia modelos DeepSeek pelas CLIs de agente instaladas na máquina."),
    ],
    "ia/workspaces": [
        ("gastownhall/gastown", "18.8k★ · gerenciador de workspace multi-agente (o mais estrelado da lista)."),
        ("NanmiCoder/cc-haha", "15.4k★ · mesa de trabalho desktop do Claude Code: worktrees, diff, multi-modelo."),
        ("EKKOLearnAI/ekko-studio", "11.8k★ · workspace local-first multi-agente (chat, código, fluxo visual)."),
        ("ValueCell-ai/ClawX", "7.6k★ · app desktop com interface gráfica para agentes OpenClaw."),
        ("xingkongliang/skills-manager", "7.5k★ · app para organizar/sincronizar skills entre 50+ ferramentas."),
        ("Devin-AXIS/iPolloWork", "7.4k★ · workbench local-first para times de agentes."),
        ("Gaurav-Gosain/tuios", "6.5k★ · gerenciador de janelas de terminal que acompanha os agentes."),
        ("spacering-net/codeg", "4.4k★ · workspace colaborativo (Claude, Codex, OpenCode)."),
        ("golutra/golutra", "3.9k★ · plataforma de orquestração multi-agente."),
        ("eneskirca/nodeterm", "2.5k★ · terminal com nós, tmux e sessões paralelas de agentes."),
        ("phodal/routa", "1.8k★ · coordenação multi-agente com specs e kanban."),
        ("Ryder-Sun/Meldwork", "1.6k★ · workspace local-first para colaboração entre agentes."),
        ("kbwo/ccmanager", "1.3k★ · gerenciador de sessões (Claude, Gemini, Codex, Cursor)."),
        ("asheshgoplani/agent-deck", "1.3k★ · TUI para gerenciar sessões de agentes."),
        ("AI-QL/tuui", "1.2k★ · cliente MCP desktop para integrar ferramentas."),
        ("chriswritescode-dev/opencode-manager", "1k★ · central de comando self-hosted para o OpenCode."),
        ("greenfield-inc/Pane", "620★ · gerenciador de agentes CLI (qualquer SO)."),
        ("kdcokenny/opencode-workspace", "584★ · harness pronto de multi-agente para OpenCode."),
        ("tony1223/better-agent-terminal", "522★ · agregador de terminais multi-workspace com Claude Code."),
        ("Kc1t/alethe-agents", "1.2k★ · workspace local-first para rodar e retomar vários agentes (a sua)."),
    ],
    "ia/agentes": [
        ("langchain-ai/langchain", "149k★ · plataforma de engenharia de agentes (base de muita coisa)."),
        ("Significant-Gravitas/AutoGPT", "187k★ · agentes que trabalham sozinhos, sem você mandar prompt."),
        ("paperclipai/paperclip", "113k★ · app open-source pra gerenciar agentes no trabalho."),
        ("stablyai/orca", "123k★ · roda uma frota de agentes de código com a sua assinatura."),
        ("FoundationAgents/MetaGPT", "71k★ · framework multi-agente que simula uma empresa de software."),
        ("microsoft/autogen", "61k★ · framework da Microsoft pra agentes e conversas entre eles."),
        ("crewAIInc/crewAI", "60k★ · orquestra agentes com papéis e tarefas (crew)."),
        ("langchain-ai/langgraph", "44k★ · agentes resilientes com estado e ciclos."),
        ("Yeachan-Heo/oh-my-claudecode", "40k★ · orquestração multi-agente para o Claude Code."),
        ("openai/swarm", "22k★ · framework leve de orquestração multi-agente (OpenAI)."),
        ("HKUDS/DeepCode", "16k★ · código aberto com harness e loop multi-agente."),
        ("microsoft/agent-framework", "14k★ · cria, orquestra e publica agentes/multi-agentes."),
        ("kyegomez/swarms", "7.3k★ · orquestração multi-agente em escala."),
        ("VRSEN/agency-swarm", "4.6k★ · multi-agente confiável com agentes especializados."),
        ("abhi1693/openclaw-mission-control", "4k★ · painel de controle de agentes (tarefas e coordenação)."),
        ("Kc1t/alethe-orchestrate-skill", "Skill que orquestra Codex, Claude Code, Antigravity, Kimi e outros."),
        ("Kc1t/fish-audio-voice-agents", "Agentes de terminal (Claude Code, Codex) que falam pela API da Fish Audio."),
        ("morluto/rea", "Engenharia reversa com agentes: de comportamento de app até binários."),
        ("togg53192-cmd/jailbreaks", "Lista de jailbreaks/prompts sem filtro para modelos."),
    ],
    "ia/paineis": [
        ("n8n-io/n8n", "210k★ · automação com IA no seu servidor (funcionário digital 24h)."),
        ("langgenius/dify", "161k★ · apps e agentes montados arrastando blocos."),
        ("FlowiseAI/Flowise", "55k★ · agentes de IA montados ligando blocos na tela."),
        ("appsmithorg/appsmith", "41k★ · painéis administrativos e ferramentas internas."),
        ("ToolJet/ToolJet", "41k★ · plataforma de apps internos e dashboards."),
        ("glanceapp/glance", "38k★ · dashboard self-hosted com seus feeds num lugar só."),
        ("gethomepage/homepage", "33k★ · homepage/dashboard de aplicações com Docker."),
        ("lissy93/dashy", "26k★ · dashboard pessoal com status e widgets."),
        ("TwiN/gatus", "12k★ · página de status com alertas (health checks)."),
        ("illacloud/illa-builder", "12k★ · low-code para apps internos."),
        ("presenton/presenton", "11.6k★ · apresentação inteira com IA a partir de um tema ou documento (self-hosted)."),
        ("bastienwirtz/homer", "11k★ · homepage estática simples pro servidor."),
    ],
    "ia/reverse": [
        ("NationalSecurityAgency/ghidra", "99k★ · framework de engenharia reversa da NSA."),
        ("WerWolv/ImHex", "55k★ · editor hexadecimal feito para engenharia reversa."),
        ("x64dbg/x64dbg", "50k★ · debugger de Windows para RE e malware."),
        ("iBotPeaches/Apktool", "27k★ · engenharia reversa de APK (Android)."),
        ("radareorg/radare2", "25k★ · framework de RE em linha de comando."),
        ("frida/frida", "22k★ · instrumentação dinâmica (hook em apps e jogos)."),
        ("rizinorg/cutter", "20k★ · plataforma gráfica de RE (base Rizin)."),
        ("Konloch/bytecode-viewer", "15k★ · decompilador/editor de JAR e APK."),
        ("mrexodia/ida-pro-mcp", "13k★ · liga o IDA Pro a modelos de IA (RE assistida)."),
        ("pwndbg/pwndbg", "11k★ · GDB/LLDB com superpoderes para RE e exploit."),
        ("angr/angr", "9.3k★ · análise de binários e execução simbólica."),
        ("rehan-remade/universal-modder", "9.6k★ · skills/tools que deixam o Claude Code moddar jogos."),
    ],
    "ia/modelos-locais": [
        ("ollama/ollama", "186k★ · DeepSeek, Qwen e Gemma no seu PC com um comando."),
        ("open-webui/open-webui", "158k★ · interface estilo ChatGPT ligada em modelos locais."),
        ("Comfy-Org/ComfyUI", "146k★ · imagem e vídeo por nós, rodando local."),
        ("ggml-org/llama.cpp", "134k★ · motor de inferência que roda até em notebook."),
        ("AUTOMATIC1111/stable-diffusion-webui", "165k★ · a interface mais conhecida para gerar imagens no PC."),
        ("lobehub/lobehub", "85k★ · “super-agentes” com tarefas, horários e relatórios."),
        ("Lllyasviel/Fooocus", "53.8k★ · imagens com IA sem mexer em mil configurações."),
        ("LibreChat-AI/LibreChat", "46.6k★ · todos os modelos numa tela só, hospedada por você."),
        ("janhq/jan", "45.3k★ · alternativa ao ChatGPT que roda sem internet."),
        ("infiniflow/ragflow", "94k★ · RAG nos seus documentos mostrando de onde tirou."),
        ("unslothai/unsloth", "79k★ · treina e roda LLM local (GGUF/MLX)."),
        ("Mintplex-Labs/anything-llm", "68k★ · conversa com PDFs e planilhas sem mandar pra fora."),
        ("mudler/LocalAI", "50k★ · engine local para LLM, visão, voz e imagem."),
        ("PurpleDoubleD/locally-uncensored", "Estúdio de IA local: chat, imagem e vídeo sem filtro."),
        ("Naoriky-VFX/canirun.ai", "“Can I Run AI”: diz se a máquina roda determinado modelo."),
    ],

    "ia/voz": [
        ("openai/whisper", "111k★ · transcrição de áudio em dezenas de idiomas (base do whisper.cpp que você usa)."),
        ("ggml-org/whisper.cpp", "45k★ · Whisper em C/C++ — o servidor local que roda no seu PC."),
        ("SYSTRAN/faster-whisper", "26.7k★ · Whisper 4× mais rápido com CTranslate2 (o que quase todo mundo usa em produção)."),
        ("m-bain/whisperX", "25.2k★ · transcrição com timestamps por palavra e separação de falantes."),
        ("chidiwilliams/buzz", "22.7k★ · app de transcrição/tradução offline no PC."),
        ("NVIDIA-NeMo/Speech", "18.7k★ · framework de fala da NVIDIA (ASR, TTS, diarização)."),
        ("pipecat-ai/pipecat", "17.2k★ · framework para agentes de voz em tempo real."),
        ("SWivid/F5-TTS", "15.6k★ · TTS com clonagem de voz por few-shot."),
        ("k2-fsa/sherpa-onnx", "15.9k★ · STT, TTS e separação de voz em ONNX (roda em qualquer lugar)."),
        ("livekit/agents", "15.2k★ · agentes de voz em tempo real (WebRTC)."),
        ("PaddlePaddle/PaddleSpeech", "12.7k★ · toolkit de fala: ASR, TTS e tradução em streaming."),
        ("speechbrain/speechbrain", "11.9k★ · toolkit de fala em PyTorch."),
        ("pyannote/pyannote-audio", "10.8k★ · diarização (quem falou o quê) e detecção de fala."),
        ("KoljaB/RealtimeSTT", "10.2k★ · STT de baixa latência com detecção de voz."),
        ("Vaibhavs10/insanely-fast-whisper", "13k★ · transcrição ultrarrápida em GPU."),
        ("yl4579/StyleTTS2", "6.4k★ · TTS com qualidade quase humana (estilo)."),
        ("vocodedev/vocode-core", "3.8k★ · agentes de voz modulares."),
        ("jhj0517/Whisper-WebUI", "2.9k★ · interface web para gerar legendas com Whisper."),
        ("debpalash/VoiceStudio", "109k★ · estúdio de voz local: clonagem, TTS e dublagem (alternativa ao ElevenLabs)."),
        ("RVC-Boss/GPT-SoVITS", "64.9k★ · clona uma voz com 1 minuto de áudio (few-shot)."),
        ("jamiepine/voicebox", "60.5k★ · estúdio de voz open-source: clonar, ditar e criar."),
        ("CorentinJ/Real-Time-Voice-Cloning", "60.2k★ · clona uma voz em 5 segundos e fala em tempo real."),
        ("coqui-ai/TTS", "46.2k★ · toolkit de TTS para pesquisa e produção."),
        ("OpenBMB/VoxCPM", "42.4k★ · TTS multilíngue sem tokenizer (design de voz)."),
        ("cjpais/Handy", "38.6k★ · app de transcrição de voz que roda 100% offline."),
        ("myshell-ai/OpenVoice", "38.2k★ · clonagem instantânea de voz (MIT/MyShell)."),
        ("index-tts/index-tts", "25k★ · TTS zero-shot industrial, controlável."),
        ("DrewThomasson/ebook2audiobook", "20.5k★ · transforma e-book em audiolivro com 50+ motores de TTS."),
        ("k2-fsa/OmniVoice", "16.5k★ · clonagem de voz em 600+ idiomas."),
        ("QwenLM/Qwen3-TTS", "14.4k★ · modelos de TTS da Qwen."),
        ("abus-aikorea/voice-pro", "13.4k★ · WebUI com TTS, clonagem e legendas."),
        ("rany2/edge-tts", "12.5k★ · usa o TTS do Edge sem precisar do Windows."),
        ("moonshine-ai/moonshine", "11.5k★ · fala para texto com latência muito baixa."),
        ("rhasspy/piper", "11.3k★ · TTS neural rápido e local."),
        ("QuentinFuxa/WhisperLiveKit", "11.2k★ · transcrição em tempo real com diarização e tradução."),
        ("jianchang512/clone-voice", "9k★ · ferramenta de clonagem de voz com interface web."),
        ("Plachtaa/seed-vc", "3.9k★ · conversão de voz e de canto (zero-shot, tempo real)."),
    ],
    "ia-local/motores": [
        ("ollama/ollama", "186.8k★ · DeepSeek, Qwen e Gemma no seu PC com um comando."),
        ("ggml-org/llama.cpp", "134k★ · motor de inferência que roda até em notebook."),
        ("vllm-project/vllm", "96.8k★ · servidor de inferência rápido (o padrão em GPU)."),
        ("unslothai/unsloth", "79k★ · treina e roda LLM local (GGUF/MLX), 2× mais rápido."),
        ("nomic-ai/gpt4all", "77k★ · roda LLM local em qualquer máquina (app pronto)."),
        ("mudler/LocalAI", "50k★ · engine local para LLM, visão, voz e imagem."),
        ("oobabooga/textgen", "47.7k★ · app desktop local para LLM (texto, visão, ferramentas)."),
        ("janhq/jan", "45.7k★ · alternativa ao ChatGPT que roda sem internet."),
        ("mozilla-ai/llamafile", "26.6k★ · modelo + motor num arquivo só, executa sem instalar nada."),
        ("LostRuins/koboldcpp", "12.3k★ · roda GGUF com interface simples (o clássico do pessoal)."),
        ("withcatai/node-llama-cpp", "2.2k★ · llama.cpp com bindings para Node.js."),
    ],
    "ia-local/interfaces": [
        ("open-webui/open-webui", "158.5k★ · interface estilo ChatGPT ligada em modelos locais."),
        ("lobehub/lobehub", "85k★ · “super-agentes” com tarefas, horários e relatórios."),
        ("Mintplex-Labs/anything-llm", "68k★ · conversa com PDFs e planilhas sem mandar pra fora."),
        ("LibreChat-AI/LibreChat", "47k★ · todos os modelos numa tela só, hospedada por você."),
        ("khoj-ai/khoj", "38k★ · “segundo cérebro” com seus documentos, self-hosted."),
        ("SillyTavern/SillyTavern", "35.6k★ · interface de chat com personagens (roleplay local)."),
        ("mckaywrigley/chatbot-ui", "33.3k★ · clone do ChatGPT para os seus modelos."),
    ],
    "ia-local/imagem-video": [
        ("AUTOMATIC1111/stable-diffusion-webui", "165.3k★ · a interface mais conhecida para gerar imagens no PC."),
        ("Comfy-Org/ComfyUI", "146.5k★ · imagem e vídeo por nós, rodando local."),
        ("Lllyasviel/Fooocus", "53.9k★ · imagens com IA sem mexer em mil configurações."),
        ("invoke-ai/InvokeAI", "29k★ · studio de imagem local com canvas e inpainting."),
        ("PurpleDoubleD/locally-uncensored", "4k★ · estúdio local: chat, imagem e vídeo sem filtro."),
    ],
    "ia-local/agentes-locais": [
        ("Fosowl/agenticSeek", "27.7k★ · agente autônomo 100% local (sem API, sem mensalidade)."),
        ("dyad-sh/dyad", "22.3k★ · construtor de apps com IA local (tipo Lovable/Replit)."),
        ("KunAgent/Kun", "6.4k★ · workspace de agente local para código, escrita e pesquisa."),
        ("AtomicBot-ai/Atomic-Chat", "2k★ · app local com motor de inferência próprio."),
    ],

    "ia/whatsapp": [
        ("WhiskeySockets/Baileys", "API não oficial do WhatsApp Web em TypeScript/JavaScript (sessão por QR)."),
        ("evolution-foundation/evolution-api", "API de WhatsApp open-source, multi-instância, com webhooks."),
        ("wppconnect-team/wppconnect", "Automação do WhatsApp Web para Node.js/TypeScript."),
    ],

    "painel-apis/roteadores": [
        ("cheaper-inference/OmniRoute", "86.8k★ · gateway de IA grátis: um endpoint para 375 provedores (150+ grátis)."),
        ("BerriAI/litellm", "63k★ · chama 100+ APIs de LLM no formato OpenAI, com controle de chaves e custo."),
        ("QuantumNous/new-api", "51.8k★ · gateway self-hosted compatível com OpenAI, Claude e Gemini."),
        ("songquanpeng/one-api", "37.4k★ · gestão e distribuição de chaves de API (OpenAI, Claude, Gemini, DeepSeek)."),
        ("decolua/9router", "32.3k★ · conecta Claude Code, Codex, Cursor e Cline em modelos grátis (a base do seu painel)."),
        ("Portkey-AI/gateway", "13.4k★ · gateway rápido com guardrails, roteando para 1.600+ LLMs."),
        ("maximhq/bifrost", "9.5k★ · gateway de LLM e MCP de alta performance."),
        ("coaidev/coai", "9.3k★ · solução multi-tenant de IA com painel admin e cobrança."),
        ("mnfst/llm-gateway", "7.6k★ · gateway de LLM open-source."),
        ("tbphp/gpt-load", "7.2k★ · gateway self-hosted para várias contas/chaves com balanceamento."),
        ("katanemo/plano", "7.1k★ · proxy/data plane para apps com agentes, com roteamento inteligente."),
        ("BlockRunAI/ClawRouter", "6.7k★ · roteador de LLM para agentes autônomos (uma carteira só)."),
        ("vllm-project/semantic-router", "6.5k★ · camada de decisão programável para escolher o modelo certo."),
        ("lm-sys/RouteLLM", "5.7k★ · framework para rotear entre modelos caros e baratos e economizar."),
        ("qixing-jk/all-api-hub", "5k★ · painel de contas/uso (saldo, check-in, chaves) para gateways."),
    ],
    "painel-apis/observabilidade": [
        ("langfuse/langfuse", "37.4k★ · plataforma de observabilidade, eval e prompt management de LLM."),
        ("tensorzero/tensorzero", "11.7k★ · LLMOps: gateway + observabilidade + experimentos num lugar."),
        ("langwatch/langwatch", "5k★ · observabilidade e avaliação de agentes para times de IA."),
    ],

    "ports": [
        ("BlackLabelHQ/SymphonyRecomp", "Recompilação de Castlevania: Symphony of the Night para PC."),
        ("Revivedx/SavageWindRecomp", "Recompilação estática de Zelda: Breath of the Wild (em progresso)."),
        ("keepvaibin/nebula", "Port/descompilação de Super Mario Galaxy para PC."),
        ("kuraeow/ultratears", "Port nativo de Zelda: Tears of the Kingdom 1.4.3 para Windows."),
        ("yozander2009-stack/Metroid-Dread-Recomp", "Recompilação de Metroid Dread para PC."),
        ("d4lfteam/d4lf", "D4LF: filtro de loot automático para Diablo IV."),
        ("HoldMyBeer-gg/d4builder", "Monta builds de Diablo IV com a matemática do jogo."),
        ("praydog/RE2-Mod-Framework", "Framework de mods em primeira pessoa para Resident Evil 2/3."),
    ],

    "software": [
        ("termux/termux-app", "Termux: terminal Linux no Android (apt, Python, git e SSH no celular)."),
        ("termux/termux-packages", "Pacotes do Termux: repositório de programas prontos para instalar no Android."),
        ("massgravel/Microsoft-Activation-Scripts", "Ativador open-source de Windows e Office (HWID, Ohook, TSforge)."),
        ("ProjectBukkit/CapcutVersions", "Links oficiais das versões do CapCut para PC."),
        ("juliusjus/Capcut-pro-activator", "Ativador do CapCut Pro (projeto de terceiros)."),
        ("Agustinm28/Optiscaler-Client", "OptiScaler: troca DLSS/FSR/XeSS nos jogos (frame generation)."),
        ("anefzaoui/misterdownloadmanager", "Gerenciador de downloads open-source (estilo IDM)."),
        ("Frizti/Fritchii", "Fork especializado (Lichii) de firmware para portátil."),
        ("sourceforge.net/p/xboxburner", "XboxBurner: grava e prepara mídia/DVD de jogos de Xbox 360 (SourceForge)."),
    ],

    "estudos": [
        ("KAYOKG/BibliotecaDev", "Biblioteca de livros de programação em PDF."),
    ],
}

# grupo -> (titulo, dica, subpastas)
GRUPOS = {
    "ia-local": ("IA local", "Rodar IA no seu próprio PC: motores, interfaces, imagem/vídeo e agentes.",
                 ["motores", "interfaces", "imagem-video", "agentes-locais"]),
    "painel-apis": ("Painel de APIs", "Gateways e roteadores de LLM: uma chave, vários modelos.",
                    ["roteadores", "observabilidade"]),
    "consoles": ("Consoles", "Desbloqueio, payloads, instaladores e emuladores por console.",
                 ["switch", "switch-2", "playstation-4", "playstation-5", "ps-vita", "wii-u"]),
    "servidores": ("Servidores de jogos online", "Servidores e ferramentas de Lineage II e Palworld.",
                   ["lineage-ii", "palworld"]),
    "ia": ("IA", "Agentes, terminal, APIs/MCP, painéis, engenharia reversa e modelos locais.",
           ["terminal", "agentes", "workspaces", "canal", "api", "paineis", "voz", "reverse", "whatsapp"]),
}

NOMES_SUB = {
    "switch": "Nintendo Switch",
    "switch-2": "Nintendo Switch 2",
    "playstation-4": "PlayStation 4",
    "playstation-5": "PlayStation 5",
    "ps-vita": "PS Vita",
    "wii-u": "Wii U / Cemu",
    "lineage-ii": "Lineage II / L2J",
    "palworld": "Palworld",
    "api": "APIs de IA",
    "agentes": "Agentes",
    "workspaces": "Workspaces de agentes",
    "canal": "Canais",
    "voz": "Voz & áudio",
    "motores": "Motores (runtimes)",
    "interfaces": "Interfaces de chat",
    "imagem-video": "Imagem & vídeo local",
    "agentes-locais": "Agentes locais",
    "terminal": "Terminal / CLI",
    "paineis": "Painéis & automação",
    "reverse": "Engenharia reversa",
    "modelos-locais": "Modelos locais",
    "whatsapp": "APIs de WhatsApp",
    "roteadores": "Roteadores & gateways",
    "observabilidade": "Observabilidade & evals",
}

DICAS_SUB = {
    "switch": "Atmosphere, hekate, instaladores, sigpatches, saves e controles.",
    "switch-2": "Dump de jogos e ferramentas iniciais do Switch 2.",
    "playstation-4": "Emulador de PS4 no PC.",
    "playstation-5": "Jailbreak, payloads e rodar Steam no PS5.",
    "ps-vita": "Homebrew e instalação de jogos no Vita.",
    "wii-u": "Cemu (emulador de Wii U) e graphic packs.",
    "lineage-ii": "L2J oficial (Bitbucket), Mobius e editores de cliente.",
    "palworld": "Servidor dedicado, correção de save e ferramentas.",
    "api": "APIs prontas de modelos (LLM grátis, roteamento).",
    "agentes": "Agentes de código, orquestração, voz e engenharia reversa.",
    "workspaces": "Mesas de trabalho para rodar e organizar vários agentes (tipo a Alethe).",
    "canal": "Canais e perfis que ensinam, com os vídeos de cada um.",
    "voz": "TTS, clonagem de voz, transcrição e conversão de fala.",
    "motores": "Ollama, llama.cpp, vLLM, GPT4All, LocalAI e afins.",
    "interfaces": "Open WebUI, LobeHub, AnythingLLM, LibreChat, SillyTavern.",
    "imagem-video": "Stable Diffusion, ComfyUI, Fooocus e InvokeAI.",
    "agentes-locais": "Agentes que rodam na sua máquina, sem API paga.",
    "terminal": "Agentes que vivem no terminal: Gemini CLI, Aider, OpenHands e afins.",
    "paineis": "Painéis e automação: n8n, Dify, Flowise, dashboards.",
    "reverse": "Ghidra, x64dbg, radare2, Frida e IA para engenharia reversa.",
    "modelos-locais": "IA rodando no seu PC (chat, voz, imagem).",
    "whatsapp": "Baileys, Evolution API e WPPConnect — WhatsApp fora da Meta.",
    "roteadores": "9router, OmniRoute, LiteLLM, new-api, one-api e afins.",
    "observabilidade": "Langfuse, TensorZero e LangWatch (logs, custo, avaliação).",
}

# páginas de um nível só (sem subpasta)
SIMPLES = {
    "ports": ("Ports & mods de jogos", "Jogos de console rodando nativo no PC e ferramentas de jogos."),
    "software": ("Windows & software", "Ativadores, CapCut, upscalers e utilitários."),
    "estudos": ("Estudos & livros", "Bibliotecas de programação para estudar."),
}

# Hospedagem de projeto: GitHub + as outras forjas (o dono quis o conjunto).
DOMINIOS = (
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "sourceforge.net",
    "codeberg.org",
    "gitea.com",
    "sr.ht",
)

FORA_DO_GITHUB = {
    "L2J oficial · game server": "https://bitbucket.org/l2jserver/l2j-server-game",
    "L2J oficial · datapack": "https://bitbucket.org/l2jserver/l2j-server-datapack",
    "L2J oficial · login server": "https://bitbucket.org/l2jserver/l2j-server-login",
    "L2J oficial · commons": "https://bitbucket.org/l2jserver/l2j-server-commons",
    "L2J oficial · docker": "https://bitbucket.org/l2jserver/l2j-server-docker",
    "L2J · site oficial": "https://web.archive.org/web/20260313053957/https://www.l2jserver.com/pt/docs/installation-guide",
    "sourceforge.net/p/xboxburner": "https://sourceforge.net/p/xboxburner/",
    "slashiee.github.io/cemu_graphic_packs": "https://slashiee.github.io/cemu_graphic_packs/",
}

with open(FONTE, encoding="utf-8") as f:
    favoritos = json.load(f)

# prints baixados (img/manifest.json)
try:
    with open(os.path.join(RAIZ, "img", "manifest.json"), encoding="utf-8") as f:
        MANIFEST = json.load(f)
except Exception:
    MANIFEST = {}

# vídeos tutoriais (_gerar/videos.json)
try:
    with open(os.path.join(RAIZ, "_gerar", "videos.json"), encoding="utf-8") as f:
        VIDEOS = json.load(f)
except Exception:
    VIDEOS = {}

urls, pastas = {}, {}
for item in favoritos:
    if not any(d in item["url"] for d in DOMINIOS):
        continue          # só sites que hospedam projeto
    urls.setdefault(item["repo"], item["url"])
    pastas.setdefault(item["repo"], item["pasta"].replace("menu / ", ""))

CSS = """
:root{--fundo:#0b0710;--card:#160f22;--card2:#1d1429;--borda:#3a2f4e;--texto:#f4f0ff;--suave:#9a8bb5;--roxo:#a855f7}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(1200px 600px at 80% -10%,#2a1145 0,#0b0710 60%);
color:var(--texto);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding:32px 20px 64px}
.wrap{max-width:1180px;margin:0 auto}
header h1{margin:0 0 6px;font-size:1.7rem}
header p{margin:0;color:var(--suave)}
.voltar{display:inline-block;margin-bottom:18px;color:var(--roxo);text-decoration:none;font-weight:700;font-size:.9rem}
.voltar:hover{text-decoration:underline}
.categorias{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;margin-top:26px}
.categoria{display:block;background:var(--card);border:1px solid var(--borda);border-radius:16px;padding:20px;
text-decoration:none;color:var(--texto);transition:.15s}
.categoria:hover{border-color:var(--roxo);background:var(--card2)}
.categoria h2{margin:0 0 6px;font-size:1.05rem}
.categoria p{margin:0;color:var(--suave);font-size:.84rem}
.categoria .num{margin-top:12px;font-size:.78rem;color:var(--roxo);font-weight:800}
.destaque-area{margin-top:26px;padding-top:20px;border-top:1px dashed var(--borda);display:flex;flex-direction:column;gap:10px;max-width:300px}
.destaque-rotulo{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--suave)}
.categoria.destaque{border-color:var(--roxo);box-shadow:0 0 0 1px rgba(168,85,247,.45),0 0 22px rgba(168,85,247,.18)}
.categoria.destaque:hover{background:#241534}
.busca{width:100%;margin-top:18px;padding:13px 16px;border-radius:12px;border:1px solid var(--borda);
background:#120c1c;color:var(--texto);font-size:.95rem}
.busca:focus{outline:none;border-color:var(--roxo)}
.contagem{margin-top:10px;font-size:.8rem;color:var(--suave)}
table{width:100%;border-collapse:collapse;margin-top:16px;background:var(--card);border:1px solid var(--borda);
border-radius:14px;overflow:hidden}
th{text-align:left;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--suave);
padding:12px 14px;background:#1a1126;border-bottom:1px solid var(--borda);white-space:nowrap}
td{padding:12px 14px;border-bottom:1px solid #241a33;font-size:.88rem;vertical-align:top}
tr:last-child td{border-bottom:0}
tr:hover td{background:#1b1228}
td a{color:var(--texto);text-decoration:none;font-family:ui-monospace,Consolas,monospace;font-weight:600}
td a:hover{color:var(--roxo);text-decoration:underline}
td.desc{color:#cfc3e6}
td.pasta{color:#6b5d85;font-size:.72rem;font-family:ui-monospace,Consolas,monospace}
td.thumb{width:180px}
td.thumb img{width:160px;border-radius:8px;border:1px solid var(--borda);display:block;background:#0e0916}
td.thumb a:hover img{border-color:var(--roxo)}
td.video{width:170px}
td.video img{width:150px;border-radius:8px;border:1px solid var(--borda);display:block}
td.video a{text-decoration:none}
td.video a:hover img{border-color:var(--roxo)}
.titulo-video{display:block;margin-top:4px;font-size:.68rem;color:var(--suave);line-height:1.25;
font-family:system-ui,sans-serif;font-weight:500}
.sem-img{color:#4d4266;font-size:.72rem}
footer{margin-top:40px;color:#5d5175;font-size:.76rem;text-align:center}
@media (max-width:720px){ td.pasta{display:none} th.col-pasta{display:none} }
"""


def url_de(nome):
    """URL do item: caso especial, favorito do Firefox, ou GitHub (curado)."""
    if nome in FORA_DO_GITHUB:
        return FORA_DO_GITHUB[nome]
    if nome in urls:
        return urls[nome]
    if "/" in nome and " " not in nome:
        return "https://github.com/" + nome
    return None


def itens_validos(chave):
    """Só o que tem URL."""
    return [(n, d) for n, d in ITENS.get(chave, []) if url_de(n)]


def escrever(relativo, conteudo):
    caminho = os.path.join(RAIZ, relativo)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)


# canais (perfis + vídeos) — aba "Canais"
CANAIS = [
    {
        "nome": "Kauã Miguel (Kc1t)",
        "url": "https://github.com/Kc1t",
        "print": "canal-kc1t.png",
        "bio": "Dev brasileiro: engenharia reversa com IA, orquestração de agentes e skills para Claude Code / Codex.",
        "videos": [
            ("fbSyFc-izIg", "Como usar o REA: engenharia reversa com IA de graça"),
            ("ujW-e6w3NQA", "Como orquestrar agentes de IA com uma skill de graça"),
            ("8jvrucR7QCU", "Pare de usar 1 agente por vez: orquestre agentes de IA"),
        ],
    },
]


def pagina_canais(relativo, titulo, dica, voltar, subida="../../"):
    cartoes = []
    for canal in CANAIS:
        videos = "".join(
            f'<a class="video-card" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">'
            f'<img src="{subida}img/yt/{vid}.jpg" loading="lazy" alt="">'
            f'<span>{html.escape(titulo_vid)}</span></a>'
            for vid, titulo_vid in canal["videos"]
        )
        cartoes.append(f"""
<div class="canal">
  <div class="canal-topo">
    <a href="{html.escape(canal['url'])}" target="_blank" rel="noopener" class="canal-print">
      <img src="{subida}img/{html.escape(canal['print'])}" loading="lazy" alt="">
    </a>
    <div class="canal-info">
      <h2>{html.escape(canal['nome'])}</h2>
      <p>{html.escape(canal['bio'])}</p>
      <a class="canal-link" href="{html.escape(canal['url'])}" target="_blank" rel="noopener">github.com/Kc1t →</a>
    </div>
  </div>
  <div class="videos">{videos}</div>
</div>""")

    escrever(relativo, f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)} - Links</title><style>{CSS}
.canal{{background:var(--card);border:1px solid var(--borda);border-radius:18px;padding:20px;margin-top:22px}}
.canal-topo{{display:flex;gap:18px;flex-wrap:wrap}}
.canal-print img{{width:330px;max-width:100%;border-radius:12px;border:1px solid var(--borda);display:block}}
.canal-info{{flex:1 1 300px}}
.canal-info h2{{margin:0 0 6px;font-size:1.2rem}}
.canal-info p{{margin:0 0 10px;color:var(--suave);font-size:.9rem}}
.canal-link{{color:var(--roxo);text-decoration:none;font-weight:700;font-size:.9rem}}
.canal-link:hover{{text-decoration:underline}}
.videos{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;margin-top:18px}}
.video-card{{display:block;background:var(--card2);border:1px solid var(--borda);border-radius:14px;padding:10px;
text-decoration:none;color:var(--texto);transition:.15s}}
.video-card:hover{{border-color:var(--roxo);transform:translateY(-2px)}}
.video-card img{{width:100%;border-radius:10px;display:block}}
.video-card span{{display:block;margin-top:8px;font-size:.84rem;line-height:1.3}}
</style></head>
<body><div class="wrap">
<a class="voltar" href="{voltar[0]}">← {html.escape(voltar[1])}</a>
<header><h1>{html.escape(titulo)}</h1><p>{html.escape(dica)}</p></header>
{''.join(cartoes)}
<footer>{html.escape(titulo)} · atualizado em 12/11/2026</footer>
</div></body></html>""")



def pagina_tabela(relativo, titulo, dica, itens, voltar):
    subida = "../" * relativo.count("/")
    linhas = []
    for nome, descricao in itens:
        url = url_de(nome)
        if not url:
            continue
        pasta = pastas.get(nome) or (
            "curado — busca na internet" if "github.com" in url
            else "fora do GitHub (Bitbucket / site oficial)"
        )
        busca = (nome + " " + descricao + " " + pasta).lower()
        arquivo_img = MANIFEST.get(nome)
        if arquivo_img:
            print_html = (f'<a href="{html.escape(url)}" target="_blank" rel="noopener">'
                          f'<img src="{subida}img/{html.escape(arquivo_img)}" loading="lazy" alt=""></a>')
        else:
            print_html = '<span class="sem-img">sem print</span>'

        video = VIDEOS.get(nome) or {}
        if video.get("id"):
            titulo_video = html.escape((video.get("titulo") or "")[:70])
            video_html = (
                f'<a href="https://www.youtube.com/watch?v={video["id"]}" target="_blank" '
                f'rel="noopener" title="{titulo_video}">'
                f'<img src="{subida}img/yt/{video["id"]}.jpg" loading="lazy" alt="">'
                f'<span class="titulo-video">{titulo_video[:48]}</span></a>'
            )
        else:
            video_html = '<span class="sem-img">sem vídeo</span>'

        linhas.append(
            f'<tr data-busca="{html.escape(busca)}">'
            f'<td class="video">{video_html}</td>'
            f'<td class="thumb">{print_html}</td>'
            f'<td><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(nome)}</a></td>'
            f'<td class="desc">{html.escape(descricao)}</td>'
            f'<td class="pasta">{html.escape(pasta)}</td></tr>'
        )

    escrever(relativo, f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)} - Links</title><style>{CSS}</style></head>
<body><div class="wrap">
<a class="voltar" href="{voltar[0]}">← {html.escape(voltar[1])}</a>
<header><h1>{html.escape(titulo)}</h1><p>{html.escape(dica)}</p></header>
<input class="busca" placeholder="Procurar por nome, descrição ou pasta…" oninput="filtrar(this.value)">
<div class="contagem" id="contagem">{len(linhas)} link{"s" if len(linhas) > 1 else ""}</div>
<table><thead><tr><th>Vídeo</th><th>Print</th><th>Projeto</th><th>O que faz</th><th class="col-pasta">Pasta de origem</th></tr></thead>
<tbody id="corpo">{''.join(linhas)}</tbody></table>
<footer>{html.escape(titulo)} · links salvos em 12/11/2026</footer>
</div>
<script>
function filtrar(termo) {{
  termo = (termo || '').toLowerCase().trim();
  let visiveis = 0;
  document.querySelectorAll('#corpo tr').forEach(tr => {{
    const mostra = !termo || tr.dataset.busca.includes(termo);
    tr.style.display = mostra ? '' : 'none';
    if (mostra) visiveis++;
  }});
  document.getElementById('contagem').textContent =
    visiveis + (visiveis === 1 ? ' link' : ' links');
}}
</script></body></html>""")


def pagina_grupo(relativo, titulo, dica, subpastas, voltar, raiz_rel):
    cartoes = []
    destaque = ""
    for slug in subpastas:
        if slug == "canal":
            cartao_canal = (
                f'<a class="categoria destaque" href="{slug}/index.html">'
                f'<h2>{html.escape(NOMES_SUB.get(slug, slug))}</h2>'
                f'<p>{html.escape(DICAS_SUB.get(slug, ""))}</p>'
                f'<div class="num">{len(CANAIS)} canal{"is" if len(CANAIS) > 1 else ""}</div></a>'
            )
            continue
        quantidade = len(itens_validos(f"{relativo.split('/')[0]}/{slug}"))
        cartoes.append(
            f'<a class="categoria" href="{slug}/index.html">'
            f'<h2>{html.escape(NOMES_SUB.get(slug, slug))}</h2>'
            f'<p>{html.escape(DICAS_SUB.get(slug, ""))}</p>'
            f'<div class="num">{quantidade} link{"s" if quantidade > 1 else ""}</div></a>'
        )
    if "canal" in subpastas:
        destaque = ('<div class="destaque-area"><span class="destaque-rotulo">Separado</span>'
                    f'{cartao_canal}</div>')
    escrever(relativo + "/index.html", f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)} - Links</title><style>{CSS}</style></head>
<body><div class="wrap">
<a class="voltar" href="{voltar[0]}">← {html.escape(voltar[1])}</a>
<header><h1>{html.escape(titulo)}</h1><p>{html.escape(dica)}</p></header>
<div class="categorias">{''.join(cartoes)}</div>
{destaque}
<footer>{html.escape(titulo)} · links salvos em 12/11/2026</footer>
</div></body></html>""")


# limpa a pasta antes de gerar (menos img/ e _gerar/)
for nome in os.listdir(RAIZ):
    if nome in ("img", "_gerar", ".git"):
        continue
    caminho = os.path.join(RAIZ, nome)
    if os.path.isdir(caminho):
        shutil.rmtree(caminho)
    elif nome.endswith(".html"):
        os.remove(caminho)

# 1) grupos com subpastas
for grupo, (titulo, dica, subs) in GRUPOS.items():
    pagina_grupo(grupo, titulo, dica, subs, ("../index.html", "todos os grupos"), "../")
    for slug in subs:
        if slug == "canal":
            pagina_canais(f"{grupo}/{slug}/index.html", NOMES_SUB.get(slug, slug),
                          DICAS_SUB.get(slug, ""), ("../index.html", titulo))
            continue
        itens = ITENS.get(f"{grupo}/{slug}", [])
        pagina_tabela(f"{grupo}/{slug}/index.html", NOMES_SUB.get(slug, slug),
                      DICAS_SUB.get(slug, ""), itens, ("../index.html", titulo))

# 2) páginas de um nível
for chave, (titulo, dica) in SIMPLES.items():
    pagina_tabela(f"{chave}/index.html", titulo, dica, ITENS.get(chave, []),
                  ("../index.html", "todos os grupos"))

# 3) raiz
cartoes = []
for grupo, (titulo, _, subs) in GRUPOS.items():
    total_grupo = sum(len(itens_validos(f"{grupo}/{s}")) for s in subs)
    if "canal" in subs:
        total_grupo += len(CANAIS)
    cartoes.append(f'<a class="categoria" href="{grupo}/index.html"><h2>{html.escape(titulo)}</h2>'
                   f'<p>{html.escape(dica)}</p>'
                   f'<div class="num">{total_grupo} links · {len(subs)} pasta{"s" if len(subs) > 1 else ""}</div></a>')
for chave, (titulo, dica) in SIMPLES.items():
    quantidade = len(CANAIS) if chave == "canais" else len(itens_validos(chave))
    cartoes.append(f'<a class="categoria" href="{chave}/index.html"><h2>{html.escape(titulo)}</h2>'
                   f'<p>{html.escape(dica)}</p>'
                   f'<div class="num">{quantidade} {"canais" if chave == "canais" else "links"}</div></a>')

total = sum(len(itens_validos(k)) for k in ITENS)

# ---------- dados para a busca da tela inicial ----------
lista = []
for grupo, (titulo_grupo, _, subs) in GRUPOS.items():
    for slug in subs:
        for nome, descricao in itens_validos(f"{grupo}/{slug}"):
            url = url_de(nome)
            lista.append({
                "nome": nome,
                "desc": descricao,
                "url": url,
                "cat": f"{titulo_grupo} · {NOMES_SUB.get(slug, slug)}",
                "img": MANIFEST.get(nome) or "",
                "video": (VIDEOS.get(nome) or {}).get("id") or "",
            })
for chave, (titulo_simples, _) in SIMPLES.items():
    for nome, descricao in itens_validos(chave):
        url = url_de(nome)
        lista.append({
            "nome": nome,
            "desc": descricao,
            "url": url,
            "cat": titulo_simples,
            "img": MANIFEST.get(nome) or "",
            "video": (VIDEOS.get(nome) or {}).get("id") or "",
        })

with open(os.path.join(RAIZ, "dados.json"), "w", encoding="utf-8") as f:
    json.dump(lista, f, ensure_ascii=False)

escrever("index.html", f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MEUS LINKS GITHUB + TUTORIAL</title><style>{CSS}</style></head>
<body><div class="wrap">
<header><h1>MEUS LINKS GITHUB + TUTORIAL</h1><p>{total} projetos com print e vídeo tutorial, separados por assunto.</p></header>
<input class="busca" id="busca" placeholder="Buscar em todos os links (nome, descrição, categoria)…" autocomplete="off">
<div class="contagem" id="contagem" style="display:none"></div>
<div id="resultados"></div>
<div class="categorias">{''.join(cartoes)}</div>
<footer>Gerado a partir dos favoritos do Firefox · atualizado em 12/11/2026</footer>
</div>
<script>
const LISTA = {json.dumps(lista, ensure_ascii=False)};
const campo = document.getElementById('busca');
const alvo = document.getElementById('resultados');
const contagem = document.getElementById('contagem');
const categorias = document.querySelector('.categorias');

function limpar(t) {{
  return (t || '').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
}}

function linha(item) {{
  const img = item.img ? '<img src="img/' + item.img + '" loading="lazy" alt="">' : '';
  const video = item.video
    ? '<a class="vid" href="https://www.youtube.com/watch?v=' + item.video + '" target="_blank" rel="noopener"><img src="img/yt/' + item.video + '.jpg" loading="lazy" alt=""></a>'
    : '<span class="sem-img">sem vídeo</span>';
  return '<tr><td class="video">' + video + '</td><td class="thumb"><a href="' + item.url + '" target="_blank" rel="noopener">' + img + '</a></td>' +
    '<td><a href="' + item.url + '" target="_blank" rel="noopener">' + item.nome + '</a></td>' +
    '<td class="desc">' + item.desc + '</td><td class="pasta">' + item.cat + '</td></tr>';
}}

function mostrar(itens) {{
  contagem.style.display = '';
  contagem.textContent = itens.length + (itens.length === 1 ? ' resultado' : ' resultados');
  alvo.innerHTML = itens.length
    ? '<table><thead><tr><th>Vídeo</th><th>Print</th><th>Projeto</th><th>O que faz</th><th class="col-pasta">Categoria</th></tr></thead><tbody>' +
      itens.slice(0, 80).map(linha).join('') + '</tbody></table>'
    : '<p class="sem-img" style="padding:16px 0">Nada encontrado para essa busca.</p>';
}}

campo.addEventListener('input', () => {{
  const termo = limpar(campo.value.trim());
  if (termo.length < 2) {{
    alvo.innerHTML = '';
    contagem.style.display = 'none';
    categorias.style.display = '';
    return;
  }}
  categorias.style.display = 'none';
  const achados = LISTA.filter((i) =>
    limpar(i.nome).includes(termo) || limpar(i.desc).includes(termo) || limpar(i.cat).includes(termo));
  mostrar(achados);
}});
</script>
</body></html>""")

print("pasta:", RAIZ)
for grupo, (titulo, _, subs) in GRUPOS.items():
    print(f"{titulo}: " + " · ".join(f"{NOMES_SUB.get(s, s)}={len(ITENS.get(f'{grupo}/{s}', []))}" for s in subs))
for chave, (titulo, _) in SIMPLES.items():
    print(f"{titulo}: {len(ITENS.get(chave, []))}")
print("total:", total)
