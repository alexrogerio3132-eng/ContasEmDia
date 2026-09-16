"""Contas em Dia — prepara o APK.
No repositório só precisam existir: index.html, preparar_android.py e .github/workflows/apk.yml.
Uso:  python preparar_android.py inicio    (antes do npm install)
      python preparar_android.py android   (depois do npx cap add android)
"""
import base64, json, pathlib, re, sys
from PIL import Image, ImageDraw

RAIZ = pathlib.Path(__file__).resolve().parent
COR = '#1F5673'
CHAVE_B64 = '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'

def calendario(S, pad=0.16, fundo=None, arredondado=False, silhueta=False):
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if fundo:
        if arredondado: d.rounded_rectangle([0, 0, S, S], radius=int(S * 0.22), fill=fundo)
        else: d.rectangle([0, 0, S, S], fill=fundo)
    p = S * pad
    x0, y0, x1, y1 = p, p + S * 0.04, S - p, S - p
    if silhueta:
        b = (255, 255, 255, 255)
        d.rounded_rectangle([x0, y0, x1, y1], radius=int(S * 0.08), outline=b, width=int(S * 0.075))
        d.rectangle([x0, y0 + (y1 - y0) * 0.12, x1, y0 + (y1 - y0) * 0.3], fill=b)
        for fx in (0.32, 0.68):
            cx = x0 + (x1 - x0) * fx; d.rounded_rectangle([cx - S * 0.035, y0 - S * 0.08, cx + S * 0.035, y0 + S * 0.08], radius=int(S * 0.03), fill=b)
        w = int(S * 0.09); cy = y0 + (y1 - y0) * 0.64; ck = b
    else:
        d.rounded_rectangle([x0, y0, x1, y1], radius=int(S * 0.07), fill=(244, 247, 250, 255))
        d.rounded_rectangle([x0, y0, x1, y0 + (y1 - y0) * 0.26], radius=int(S * 0.07), fill=(217, 150, 26, 255))
        d.rectangle([x0, y0 + (y1 - y0) * 0.16, x1, y0 + (y1 - y0) * 0.26], fill=(217, 150, 26, 255))
        for fx in (0.32, 0.68):
            cx = x0 + (x1 - x0) * fx; d.rounded_rectangle([cx - S * 0.02, y0 - S * 0.05, cx + S * 0.02, y0 + S * 0.06], radius=int(S * 0.02), fill=(24, 33, 43, 255))
        w = int(S * 0.055); cy = y0 + (y1 - y0) * 0.62; ck = (46, 116, 71, 255)
    pts = [(x0 + (x1 - x0) * 0.28, cy), (x0 + (x1 - x0) * 0.44, cy + (y1 - y0) * 0.15), (x0 + (x1 - x0) * 0.74, cy - (y1 - y0) * 0.17)]
    d.line(pts, fill=ck, width=w, joint='curve')
    for q in (pts[0], pts[2]): d.ellipse([q[0] - w / 2, q[1] - w / 2, q[0] + w / 2, q[1] + w / 2], fill=ck)
    return im

def desenhar(tam, **kw):
    return calendario(tam * 4, **kw).resize((tam, tam), Image.LANCZOS)

def inicio():
    (RAIZ / 'package.json').write_text(json.dumps({
        "name": "contas-em-dia", "version": "1.0.0", "private": True,
        "dependencies": {"@capacitor/android": "8.5.2", "@capacitor/app": "8.1.1", "@capacitor/core": "8.5.2",
                         "@capacitor/filesystem": "8.1.3", "@capacitor/local-notifications": "8.3.1", "@capacitor/share": "8.0.2"},
        "devDependencies": {"@capacitor/cli": "8.5.2"}}, indent=2), encoding='utf-8')
    (RAIZ / 'capacitor.config.json').write_text(json.dumps({
        "appId": "br.app.contasemdia", "appName": "Contas em Dia", "webDir": "www",
        "plugins": {"LocalNotifications": {"smallIcon": "ic_stat_contas", "iconColor": COR}}}, indent=2), encoding='utf-8')
    www = RAIZ / 'www'; www.mkdir(exist_ok=True)
    (www / 'index.html').write_bytes((RAIZ / 'index.html').read_bytes())
    fundo = (31, 86, 115, 255)
    desenhar(192, fundo=fundo, arredondado=True).save(www / 'icon-192.png')
    desenhar(512, fundo=fundo, arredondado=True).save(www / 'icon-512.png')
    desenhar(512, pad=0.2, fundo=fundo).save(www / 'icon-maskable-512.png')
    (www / 'manifest.json').write_text(json.dumps({"name": "Contas em Dia", "short_name": "Contas em Dia", "start_url": "./",
        "display": "standalone", "theme_color": COR, "background_color": "#EDF0F3",
        "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]},
        ensure_ascii=False), encoding='utf-8')
    print('Arquivos do app criados.')

def android():
    app = RAIZ / 'android' / 'app'
    res = app / 'src' / 'main' / 'res'
    fundo = (31, 86, 115, 255)
    for nome, k in {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}.items():
        m = res / f'mipmap-{nome}'; m.mkdir(parents=True, exist_ok=True)
        t = round(48 * k)
        desenhar(t, fundo=fundo, arredondado=True).save(m / 'ic_launcher.png')
        redonda = Image.new('RGBA', (t, t), (0, 0, 0, 0))
        mascara = Image.new('L', (t * 4, t * 4), 0); ImageDraw.Draw(mascara).ellipse([0, 0, t * 4 - 1, t * 4 - 1], fill=255)
        redonda.paste(desenhar(t, pad=0.25, fundo=fundo), (0, 0), mascara.resize((t, t), Image.LANCZOS))
        redonda.save(m / 'ic_launcher_round.png')
        desenhar(round(108 * k), pad=0.25).save(m / 'ic_launcher_foreground.png')
        dr = res / f'drawable-{nome}'; dr.mkdir(parents=True, exist_ok=True)
        desenhar(round(24 * k), pad=0.12, silhueta=True).save(dr / 'ic_stat_contas.png')
    (res / 'values' / 'ic_launcher_background.xml').write_text(
        f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">{COR}</color>\n</resources>\n', encoding='utf-8')
    for p in res.glob('drawable*/splash.png'): p.unlink()
    (res / 'drawable' / 'splash.xml').write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<layer-list xmlns:android="http://schemas.android.com/apk/res/android">\n'
        '    <item android:drawable="@color/ic_launcher_background" />\n</layer-list>\n', encoding='utf-8')
    man = app / 'src' / 'main' / 'AndroidManifest.xml'
    t = man.read_text(encoding='utf-8')
    if 'USE_EXACT_ALARM' not in t:
        t = t.replace('</manifest>', '    <uses-permission android:name="android.permission.USE_EXACT_ALARM" />\n</manifest>')
    man.write_text(t, encoding='utf-8')
    (app / 'contasemdia.keystore').write_bytes(base64.b64decode(CHAVE_B64))
    g = (app / 'build.gradle').read_text(encoding='utf-8')
    if 'signingConfigs' not in g:
        g = g.replace('android {', '''android {
    signingConfigs {
        release {
            storeFile file("contasemdia.keystore")
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
        g = g.replace('minifyEnabled false', 'minifyEnabled false\n            signingConfig signingConfigs.release', 1)
    (app / 'build.gradle').write_text(g, encoding='utf-8')
    print('Projeto Android ajustado.')

if __name__ == '__main__':
    etapa = sys.argv[1] if len(sys.argv) > 1 else ''
    if etapa == 'inicio': inicio()
    elif etapa == 'android': android()
    else: sys.exit('Use: python preparar_android.py inicio | android')
