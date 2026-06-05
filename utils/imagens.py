from PIL import Image
import os


def redimensionar_logo(caminho_original, tamanhos=[16, 32, 64, 128, 192, 256, 512]):
    """Gera múltiplos tamanhos da logo para diferentes plataformas"""
    if not os.path.exists(caminho_original):
        print(f"Logo não encontrada: {caminho_original}")
        return

    img = Image.open(caminho_original)
    nome_base = os.path.splitext(os.path.basename(caminho_original))[0]
    pasta = os.path.dirname(caminho_original)

    for tamanho in tamanhos:
        img_redim = img.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
        caminho_saida = os.path.join(pasta, f"{nome_base}-{tamanho}.png")
        img_redim.save(caminho_saida, "PNG", optimize=True)
        print(f"✅ Gerado: {caminho_saida}")


def converter_para_ico(caminho_png, caminho_ico):
    """Converte PNG para ICO (favicon)"""
    if os.path.exists(caminho_png):
        img = Image.open(caminho_png)
        img.save(caminho_ico, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
        print(f"✅ Favicon gerado: {caminho_ico}")


if __name__ == "__main__":
    # Exemplo de uso
    redimensionar_logo("assets/logo.png")
    converter_para_ico("assets/logo.png", "assets/favicon.ico")