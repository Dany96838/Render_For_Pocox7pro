# Auditoria inicial — 20/11/2026

Plugin upstream consultado: f5105e4ddd1752cccdcc6421c402960d40ec3d9d. Seu submódulo core aponta para f56af31d3e490d95808b3adc4ace20234249a37a. HEAD separado do core: 97558a69157b033b890958b1e49258c5b51a80c6; não substituir silenciosamente a revisão do plugin.

Release oficial consultado: V2.0.0. O main do plugin avisa que pode conter código não lançado. versionName=2.0.0 não prova correspondência ao APK estável. Essa correspondência ainda não foi estabelecida.

## Especialização
Há classificadores Adreno 730/740/830 em config/gpu_utils.cpp e uso em config/settings.cpp. São candidatos a investigação, não remoções já aprovadas tecnicamente: preservar detecção de capacidades e GLES/ANGLE. gl/texture.cpp possui correções documentadas para Adreno e Mali; não remover sincronização ou formatos com base só no nome da GPU em comentários.

Restringir build a arm64-v8a reduz tamanho, não demonstra ganho de FPS. Preservar tradução GLSL, SPIRV-Cross/glslang, recursos Minecraft/Iris/Sodium e fallback multidraw. PanVK não testado e não integrado.

## Build proposto
GitHub Actions manual: ubuntu-24.04, JDK 17, SDK 36, NDK 27.3.13750724, CMake 3.22.1. Compilar biblioteca e plugin com commits fixados, coletar APK e SHA256. Não executar builds Android no sandbox.

## Bloqueio
A conexão GitHub permitiu criar README, mas a tentativa de enviar o workflow e os arquivos de preparação retornou HTTP 403 após tentativa de ampliar permissões. Nenhum build foi disparado. Confirmar arquivos presentes antes de retomar.

## Instalação
APK experimental terá assinatura diferente da oficial. Resolver applicationId e contrato do FCL antes de instalar. Não desinstalar original nem apagar configurações.

## Estado
Sem APK novo, sem alteração de comportamento GPU, sem medições ou testes no aparelho. Primeiro resolver acesso de workflow e correspondência do código ao estável; depois baseline e patches pequenos.
