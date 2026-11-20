# Render For POCO X7 Pro

Fork experimental, não oficial, do MobileGlues para FCL no POCO X7 Pro / Mali-G720 MC7.

## Estado real
Ainda não existe APK otimizado ou resultado de desempenho. A primeira etapa é reproduzir um build e mapear caminhos exclusivos de outras GPUs antes de removê-los. Não confundir redução de tamanho com aumento de FPS.

## Alvo
- Android 16 / API 36 (capturas de outubro de 2026)
- arm64-v8a, 12 GB RAM
- FCL 1.3.4.7; Minecraft Java 1.20.1 como primeiro alvo
- Sem root; notebook disponível para coleta de logs via ADB

## Regras
Preservar GLES, ANGLE, tradução GLSL, recursos exigidos por Minecraft/Iris/Sodium e correções compartilhadas. Remover somente caminhos comprovadamente exclusivos de outros modelos. PanVK enviado pelo usuário não foi testado e não será integrado automaticamente. Não modificar bibliotecas de sistema.

## Fontes e licença
MobileGL-Dev/MobileGlues e MobileGL-Dev/MobileGlues-plugin: LGPL-2.1; preservar licenças e disponibilizar fontes correspondentes ao distribuir binários. Dependências possuem licenças próprias. Apenas este repositório receberá alterações.
