"""Todos os arquivos ficam soltos na raiz do repositório (fácil de enviar pelo celular).
Ajusta o projeto Android gerado pelo Capacitor: ícones, cor, permissão de alarme e assinatura."""
import pathlib, re
from PIL import Image, ImageDraw

RAIZ = pathlib.Path(__file__).resolve().parent
APP = RAIZ / 'android' / 'app'
RES = APP / 'src' / 'main' / 'res'
COR = '#1F5673'
DENS = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}

icone = Image.open(RAIZ / 'icon-512.png').convert('RGBA')
frente = Image.open(RAIZ / 'icone-frente.png').convert('RGBA')
notif = Image.open(RAIZ / 'icone-notificacao.png').convert('RGBA')

def redonda(img):
    s = img.size[0]
    fundo = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    mascara = Image.new('L', (s * 4, s * 4), 0)
    ImageDraw.Draw(mascara).ellipse([0, 0, s * 4 - 1, s * 4 - 1], fill=255)
    base = Image.new('RGBA', (s, s), COR)
    base.alpha_composite(frente.resize((s, s), Image.LANCZOS))
    fundo.paste(base, (0, 0), mascara.resize((s, s), Image.LANCZOS))
    return fundo

for nome, k in DENS.items():
    m = RES / f'mipmap-{nome}'
    m.mkdir(parents=True, exist_ok=True)
    t = round(48 * k)
    icone.resize((t, t), Image.LANCZOS).save(m / 'ic_launcher.png')
    redonda(Image.new('RGBA', (t, t))).save(m / 'ic_launcher_round.png')
    f = round(108 * k)
    frente.resize((f, f), Image.LANCZOS).save(m / 'ic_launcher_foreground.png')
    d = RES / f'drawable-{nome}'
    d.mkdir(parents=True, exist_ok=True)
    n = round(24 * k)
    notif.resize((n, n), Image.LANCZOS).save(d / 'ic_stat_contas.png')

(RES / 'values' / 'ic_launcher_background.xml').write_text(
    f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">{COR}</color>\n</resources>\n', encoding='utf-8')

# tela de abertura: só a cor do app
for p in RES.glob('drawable*/splash.png'):
    p.unlink()
(RES / 'drawable' / 'splash.xml').write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n<layer-list xmlns:android="http://schemas.android.com/apk/res/android">\n'
    '    <item android:drawable="@color/ic_launcher_background" />\n</layer-list>\n', encoding='utf-8')

# permissão de alarme exato (liberada automaticamente em apps de lembrete fora da Play Store)
manifesto = APP / 'src' / 'main' / 'AndroidManifest.xml'
txt = manifesto.read_text(encoding='utf-8')
if 'USE_EXACT_ALARM' not in txt:
    txt = txt.replace('</manifest>', '    <uses-permission android:name="android.permission.USE_EXACT_ALARM" />\n</manifest>')
manifesto.write_text(txt, encoding='utf-8')

# assinatura fixa (permite atualizar o app sem desinstalar) e versão pelo número da compilação
gradle = APP / 'build.gradle'
g = gradle.read_text(encoding='utf-8')
if 'signingConfigs' not in g:
    g = g.replace('android {', '''android {
    signingConfigs {
        release {
            storeFile file("../../contasemdia.keystore")
            storePassword "contasemdia2026"
            keyAlias "contasemdia"
            keyPassword "contasemdia2026"
        }
    }
    lint {
        checkReleaseBuilds false
        abortOnError false
    }''', 1)
    g = re.sub(r'versionCode \d+', 'versionCode Integer.parseInt(System.getenv("GITHUB_RUN_NUMBER") ?: "1")', g, count=1)
    g = re.sub(r'versionName "[^"]*"', 'versionName "1.0." + (System.getenv("GITHUB_RUN_NUMBER") ?: "1")', g, count=1)
    g = g.replace("minifyEnabled false", "minifyEnabled false\n            signingConfig signingConfigs.release", 1)
gradle.write_text(g, encoding='utf-8')
print('Projeto Android ajustado.')
