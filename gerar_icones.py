#!/usr/bin/env python3
"""
Gerador de Ícones para aEterna
Cria todos os tamanhos de ícone necessários para web, PWA e mobile
"""

import os
import sys
from PIL import Image


def criar_pastas():
    """Cria as pastas necessárias"""
    pastas = ['assets', 'icons']
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"✅ Pasta criada: {pasta}")
    return True


def encontrar_logo():
    """Procura a logo original em vários locais possíveis"""
    possiveis_caminhos = [
        "logo.png",
        "logo.jpg",
        "logo.jpeg",
        "assets/logo.png",
        "assets/logo.jpg",
        "assets/logo.jpeg",
        "icons/logo.png",
        "icons/logo.jpg",
        "../logo.png",
    ]

    for caminho in possiveis_caminhos:
        if os.path.exists(caminho):
            print(f"✅ Logo encontrada: {caminho}")
            return caminho

    print("❌ Nenhuma logo encontrada!")
    print("   Coloque sua logo.png na pasta raiz do projeto")
    return None


def redimensionar_imagem(imagem, tamanho, output_path, manter_proporcao=True):
    """Redimensiona uma imagem para o tamanho especificado"""
    try:
        if manter_proporcao:
            # Redimensiona mantendo proporção e centraliza
            img_temp = imagem.copy()
            img_temp.thumbnail((tamanho, tamanho), Image.Resampling.LANCZOS)

            # Cria canvas quadrado
            nova_imagem = Image.new('RGBA', (tamanho, tamanho), (0, 0, 0, 0))

            # Centraliza a imagem redimensionada
            x = (tamanho - img_temp.width) // 2
            y = (tamanho - img_temp.height) // 2
            nova_imagem.paste(img_temp, (x, y))
        else:
            # Redimensiona forçando o tamanho exato
            nova_imagem = imagem.resize((tamanho, tamanho), Image.Resampling.LANCZOS)

        # Converte para RGB se necessário (para JPEG)
        if output_path.endswith('.jpg') or output_path.endswith('.jpeg'):
            if nova_imagem.mode == 'RGBA':
                # Fundo branco para imagens com transparência
                fundo = Image.new('RGB', nova_imagem.size, (255, 255, 255))
                fundo.paste(nova_imagem, mask=nova_imagem.split()[3] if len(nova_imagem.split()) > 3 else None)
                nova_imagem = fundo

        nova_imagem.save(output_path, optimize=True, quality=85)
        return True
    except Exception as e:
        print(f"   Erro ao gerar {output_path}: {e}")
        return False


def gerar_todos_icones(logo_path):
    """Gera todos os ícones necessários"""

    # Carrega a imagem original
    try:
        img_original = Image.open(logo_path)
        print(f"\n📷 Imagem carregada: {img_original.size[0]}x{img_original.size[1]} pixels")

        # Converte para RGBA se necessário
        if img_original.mode != 'RGBA':
            img_original = img_original.convert('RGBA')

    except Exception as e:
        print(f"❌ Erro ao carregar imagem: {e}")
        return False

    print("\n🎨 Gerando ícones...\n")

    # =========================================================
    # 1. ÍCONES PARA O SITE/WEB (favicon e afins)
    # =========================================================
    print("📱 Ícones para Web:")

    web_icons = [
        (16, "favicon-16.png"),
        (32, "favicon-32.png"),
        (48, "favicon-48.png"),
        (64, "favicon-64.png"),
        (96, "favicon-96.png"),
        (128, "favicon-128.png"),
    ]

    for tamanho, nome in web_icons:
        path = f"assets/{nome}"
        if redimensionar_imagem(img_original, tamanho, path, manter_proporcao=True):
            print(f"   ✅ {nome} ({tamanho}x{tamanho})")

    # =========================================================
    # 2. ÍCONES PARA PWA (Progressive Web App)
    # =========================================================
    print("\n📱 Ícones para PWA:")

    pwa_icons = [
        (72, "icon-72.png"),
        (96, "icon-96.png"),
        (128, "icon-128.png"),
        (144, "icon-144.png"),
        (152, "icon-152.png"),
        (192, "icon-192.png"),
        (256, "icon-256.png"),
        (384, "icon-384.png"),
        (512, "icon-512.png"),
    ]

    for tamanho, nome in pwa_icons:
        path = f"assets/{nome}"
        if redimensionar_imagem(img_original, tamanho, path, manter_proporcao=True):
            print(f"   ✅ {nome} ({tamanho}x{tamanho})")

    # =========================================================
    # 3. ÍCONES PARA APP STORES
    # =========================================================
    print("\n📱 Ícones para App Stores:")

    # Para Google Play Store
    google_icons = [
        (512, "playstore-icon.png"),
    ]

    for tamanho, nome in google_icons:
        path = f"assets/{nome}"
        if redimensionar_imagem(img_original, tamanho, path, manter_proporcao=False):
            print(f"   ✅ {nome} ({tamanho}x{tamanho})")

    # Para Apple App Store
    apple_icons = [
        (1024, "appstore-icon.png"),
    ]

    for tamanho, nome in apple_icons:
        path = f"assets/{nome}"
        if redimensionar_imagem(img_original, tamanho, path, manter_proporcao=False):
            print(f"   ✅ {nome} ({tamanho}x{tamanho})")

    # =========================================================
    # 4. ÍCONES PARA SPLASH SCREEN
    # =========================================================
    print("\n📱 Splash Screens:")

    # Splash screens para diferentes dispositivos
    splash_sizes = [
        (640, 1136, "splash-iphone5.png"),  # iPhone 5/SE
        (750, 1334, "splash-iphone6.png"),  # iPhone 6/7/8
        (1242, 2208, "splash-iphoneplus.png"),  # iPhone Plus
        (1125, 2436, "splash-iphonex.png"),  # iPhone X/11/12
        (2048, 2732, "splash-ipad.png"),  # iPad Pro
        (1080, 1920, "splash-android.png"),  # Android
    ]

    for width, height, nome in splash_sizes:
        try:
            # Para splash screens, criamos uma imagem maior com a logo centralizada
            splash = Image.new('RGBA', (width, height), (46, 139, 87, 255))  # Fundo verde

            # Redimensiona a logo para caber na splash (máximo 30% da tela)
            max_logo_size = min(width, height) // 3
            logo_splash = img_original.copy()
            logo_splash.thumbnail((max_logo_size, max_logo_size), Image.Resampling.LANCZOS)

            # Centraliza a logo
            x = (width - logo_splash.width) // 2
            y = (height - logo_splash.height) // 2
            splash.paste(logo_splash, (x, y), logo_splash if logo_splash.mode == 'RGBA' else None)

            # Converte para RGB
            if splash.mode == 'RGBA':
                splash = splash.convert('RGB')

            splash.save(f"assets/{nome}", optimize=True, quality=85)
            print(f"   ✅ {nome} ({width}x{height})")
        except Exception as e:
            print(f"   ❌ Erro ao gerar {nome}: {e}")

    # =========================================================
    # 5. FAVICON.ICO (multiplos tamanhos)
    # =========================================================
    print("\n🌐 Gerando favicon.ico...")

    try:
        # Cria um arquivo .ico com múltiplos tamanhos
        sizes = [16, 32, 48, 64, 128]
        icons = []

        for size in sizes:
            icon = img_original.copy()
            icon.thumbnail((size, size), Image.Resampling.LANCZOS)
            # Centraliza em canvas quadrado
            new_icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            x = (size - icon.width) // 2
            y = (size - icon.height) // 2
            new_icon.paste(icon, (x, y))

            if new_icon.mode != 'RGBA':
                new_icon = new_icon.convert('RGBA')
            icons.append(new_icon)

        # Salva como .ico
        icons[0].save("assets/favicon.ico", format='ICO', sizes=[(s, s) for s in sizes], append_images=icons[1:])
        print("   ✅ favicon.ico gerado com múltiplos tamanhos")
    except Exception as e:
        print(f"   ⚠️ Erro ao gerar favicon.ico: {e}")
        print("   (pule este passo se não for necessário)")

    # =========================================================
    # 6. LOGO PRINCIPAL OTIMIZADA
    # =========================================================
    print("\n✨ Otimizando logo principal...")

    # Salva versão otimizada da logo
    logo_optimized = img_original.copy()

    # Redimensiona se for muito grande (máximo 1024px)
    if max(logo_optimized.size) > 1024:
        logo_optimized.thumbnail((1024, 1024), Image.Resampling.LANCZOS)

    logo_optimized.save("assets/logo.png", "PNG", optimize=True)
    print("   ✅ assets/logo.png (otimizada)")

    # Salva versão para fallback (caso a original seja removida)
    logo_optimized.save("logo_backup.png", "PNG", optimize=True)
    print("   ✅ logo_backup.png (cópia de segurança)")

    # =========================================================
    # RESUMO FINAL
    # =========================================================
    print("\n" + "=" * 50)
    print("🎉 TODOS OS ÍCONES FORAM GERADOS COM SUCESSO!")
    print("=" * 50)
    print("\n📁 Os ícones foram salvos na pasta 'assets/'")
    print("\n📋 Arquivos gerados:")

    # Lista todos os arquivos gerados
    if os.path.exists("assets"):
        for file in sorted(os.listdir("assets")):
            if file.endswith(('.png', '.ico', '.jpg')):
                file_path = os.path.join("assets", file)
                file_size = os.path.getsize(file_path)
                print(f"   📄 {file} ({file_size:,} bytes)")

    print("\n💡 Próximos passos:")
    print("   1. Verifique se todos os ícones foram gerados corretamente")
    print("   2. Execute 'streamlit run app.py' para testar")
    print("   3. O ícone na aba do navegador agora deve aparecer!")

    return True


def criar_manifest_json():
    """Cria o arquivo manifest.json para PWA"""

    manifest = {
        "name": "aEterna - Legado Digital",
        "short_name": "aEterna",
        "description": "Guarde senhas e mensagens eternas para seus entes queridos",
        "start_url": "/",
        "display": "standalone",
        "theme_color": "#2E8B57",
        "background_color": "#ffffff",
        "orientation": "portrait",
        "categories": ["lifestyle", "productivity"],
        "icons": [
            {"src": "assets/icon-72.png", "sizes": "72x72", "type": "image/png", "purpose": "any maskable"},
            {"src": "assets/icon-96.png", "sizes": "96x96", "type": "image/png", "purpose": "any maskable"},
            {"src": "assets/icon-128.png", "sizes": "128x128", "type": "image/png", "purpose": "any maskable"},
            {"src": "assets/icon-144.png", "sizes": "144x144", "type": "image/png", "purpose": "any maskable"},
            {"src": "assets/icon-152.png", "sizes": "152x152", "type": "image/png", "purpose": "any maskable"},
            {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "assets/icon-256.png", "sizes": "256x256", "type": "image/png", "purpose": "any maskable"},
            {"src": "assets/icon-384.png", "sizes": "384x384", "type": "image/png", "purpose": "any maskable"},
            {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
        ]
    }

    import json
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("\n✅ manifest.json criado/atualizado")


def verificar_dependencias():
    """Verifica se as dependências necessárias estão instaladas"""
    try:
        import PIL
        print(f"✅ Pillow (PIL) versão: {PIL.__version__}")
        return True
    except ImportError:
        print("❌ Pillow não está instalado!")
        print("   Execute: pip install Pillow")
        return False


def main():
    """Função principal"""
    print("\n" + "=" * 50)
    print("🎨 GERADOR DE ÍCONES - aEterna")
    print("=" * 50 + "\n")

    # Verificar dependências
    if not verificar_dependencias():
        print("\n📦 Instale as dependências com:")
        print("   pip install Pillow")
        return

    # Criar pastas necessárias
    criar_pastas()

    # Encontrar a logo original
    logo_path = encontrar_logo()

    if logo_path:
        # Gerar todos os ícones
        if gerar_todos_icones(logo_path):
            # Criar/atualizar manifest.json
            criar_manifest_json()

            print("\n" + "=" * 50)
            print("✨ PROCESSO CONCLUÍDO COM SUCESSO!")
            print("=" * 50)
            print("\n🚀 Agora execute: streamlit run app.py")
        else:
            print("\n❌ Falha ao gerar os ícones.")
    else:
        print("\n❌ Não foi possível gerar os ícones.")
        print("   Por favor, coloque sua logo.png na pasta raiz e tente novamente.")


if __name__ == "__main__":
    main()
