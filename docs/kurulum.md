# Kurulum: tek seferlik komuttan tekrar kullanılabilir beceriye

## 1. E-posta erişimini hazırla

Kullandığın asistanın desteklediği e-posta bağlayıcısını yetkilendir. Sağlayıcıya göre Gmail veya Microsoft 365 / Outlook bağlantısı gerekebilir. En az yetki yaklaşımını uygula: tarama için okuma erişimi yeterliyse yazma ve gönderme izinlerini açma. Hem gelen hem gönderilen mesajlar erişilebilir olursa yanlış pozitifler azalır.

> E-posta bağlantısı, uygulama tarafından gerçekten kurulmadıkça bu depodaki dosyalar hesabı okuyamaz. Bağlantı yoksa hiçbir sonuç uydurulmamalıdır.

## 2. İlk denemeyi çalıştır

[`prompts/tek-seferlik-tarama.md`](../prompts/tek-seferlik-tarama.md) dosyasını asistanın görev alanına yapıştır. İlk turda aralığı 30 günle sınırla. Çıkan adayların bir kısmını gelen/gönderilen posta kutularında elle doğrula.

## 3. Beceri kur

### Claude Code

Bu depoyu projenin içinde kullanacaksan:

```bash
mkdir -p .claude/skills/inbox-followup-audit
cp skills/inbox-followup-audit/SKILL.md .claude/skills/inbox-followup-audit/SKILL.md
```

Kişisel kurulum istersen aynı klasörü `~/.claude/skills/inbox-followup-audit/` altına yerleştir. Claude Code'daki beceri konumları: [Anthropic Agent Skills belgeleri](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

### Claude.ai / Cowork

Önce paketi oluştur:

```bash
python3 scripts/package_skill.py
```

Oluşan `dist/inbox-followup-audit-skill.zip` dosyasını hesabındaki Skills / özel beceri yükleme alanından içe aktar. Menü isimleri ürüne ve sürüme göre değişebilir. [Resmî Skills kılavuzu](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

### ChatGPT

ChatGPT'de desteklenen Gmail bağlantısını yetkilendir; `prompts/tek-seferlik-tarama.md` içeriğini kullan. Bu depo Claude'un `SKILL.md` formatında olduğu için ChatGPT'ye aynı ZIP'i yüklemek gerekli ya da eşdeğer bir kurulum yöntemi değildir.

## 4. Doğrula

- Gelen Kutusu ve Gönderilmiş kontrol ediliyor mu?
- Son gelen talebe sonradan yanıt verildiyse listeden çıkarılıyor mu?
- Kişisel veriler gereksiz yere rapora taşınmıyor mu?
- Her öneri kaynak konuşmaya bağlı mı?
- Kullanıcı onayı olmadan hiçbir değişiklik yapılmıyor mu?

## 5. Tekrar çalıştırma

Aynı denetim için “Son 7 gündeki yanıt bekleyen iş konuşmalarını bul” gibi bir istek yeterlidir; fakat her yeni çalışmada erişimin hâlâ geçerli olduğunu ve gönderme izninin kullanılmadığını doğrula. Planlı tarama için platformunun zamanlayıcı özelliğini ayrıca kurman gerekir; **bu depo kendi başına zamanlanmış görev başlatmaz**.
