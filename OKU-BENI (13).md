# WOLTSMS SEO paketi – kurulum rehberi

Bu klasördeki dosyalar, woltsms.com için hazırlanan SEO planının uygulanmış halidir.
Yazılımcın bu dosyaları sitenin kök dizinine yüklediğinde yeni sayfalar yayına girer.

## 1. Yayına almadan önce: sarı alanları doldur

Sayfalarda sarı arka planlı, kesik çizgili **[DOLDUR: ...]** alanları var. Bunlar
doğrulayamadığım bilgiler; tahmin yazmadım. Hepsini gerçek bilgilerle değiştir, sonra
`.doldur` sınıfını kaldır. Bulmak için dosyalarda `DOLDUR` kelimesini arat.

En önemlileri:

| Bilgi | Nerede |
| --- | --- |
| Şirket unvanı, adres, vergi no, MERSİS no | Tüm sayfaların alt bilgisi, Hakkımızda, yasal sayfalar |
| Gönderimin yapıldığı BTK yetkili operatör / altyapı | Ana sayfa "Güvence ve yasal uyum", Hakkımızda |
| İYS entegrasyonu var mı | Hakkımızda |
| Kurumsal e-posta ve Türkiye telefon numarası | Alt bilgi, Hakkımızda |
| KDV dahil/hariç, bakiye süresi, iletilemeyen SMS politikası | Fiyatlar sayfası |
| Fatura bilgisi | Ana sayfa SSS |
| API adresi ve desteklenen işlemler | SMS API sayfası |
| Başlık belgeleri, onay süresi, ücret | Başlıklı SMS sayfası |
| OTP teslim süresi | OTP SMS sayfası |

**Önemli:** BTK, İYS veya teslim süresiyle ilgili alanlara yalnızca gerçekten doğru olan
bilgiyi yaz. Bu bilgileri karşılayamıyorsan ilgili cümleyi tamamen kaldır; yanlış beyan
hem yasal risk yaratır hem de Google'ın güven değerlendirmesine zarar verir.

Sık sorulan sorulardaki cevaplar sayfa koduna FAQ şeması olarak da işleniyor; bir SSS
cevabındaki [DOLDUR] alanını doldurmazsan o soruyu tamamen sil.

Yasal sayfalar (`/yasal/...`) **şablondur**; bir hukukçunun tamamlaması gerekir.

Ana sayfadan "kripto ile yükleme" ifadesi kaldırıldı: Türkiye'de kripto varlıklarla ödeme
2021'den beri TCMB yönetmeliğiyle yasak.

## 2. Dosyaları yükle

```
index.html                                  → ana sayfa (mevcut olanın yerine)
toplu-sms-fiyatlari/index.html              → fiyatlar + hesaplayıcı + sipariş formu
sms-api/index.html
otp-sms/index.html
baslikli-sms/index.html
hakkimizda/index.html
blog/index.html
blog/toplu-sms-nasil-gonderilir/index.html
blog/sms-karakter-siniri-ve-fiyat-hesaplama/index.html
blog/iys-nedir-ticari-sms-izni/index.html
yasal/kvkk-aydinlatma-metni/index.html
yasal/kullanim-kosullari/index.html
yasal/mesafeli-satis-sozlesmesi/index.html
assets/style.css
robots.txt
sitemap.xml
```

- Sitenin mevcut bir tasarım şablonu varsa, sayfaların `<main>` içeriğini o şablona
  taşıyabilirsin. `<head>` içindeki title, description, canonical, Open Graph ve
  `application/ld+json` blokları mutlaka korunmalı.
- `/kayit` ve `/login` sayfaları mevcut haliyle kalır. `/login` sayfasının `<head>`
  bölümüne `<meta name="robots" content="noindex">` ekle.
- `woltsms.com` → `https://www.woltsms.com` yönlendirmesinin **301 (kalıcı)** olduğundan emin ol.

## 3. Sipariş formu

Fiyatlar sayfasındaki form, sunucu gerektirmeden çalışsın diye siparişi WhatsApp'a
hazır mesaj olarak gönderir. İleride sitede gerçek bir sipariş altyapısı kurulursa
formun `submit` kısmı oraya bağlanmalı.

## 4. Yayından sonra

1. Google Search Console'da `www.woltsms.com` alan adını DNS ile doğrula.
2. Dizin oluşturma > Site haritaları bölümüne `https://www.woltsms.com/sitemap.xml` gir.
3. URL denetimi aracıyla ana sayfa ve fiyatlar sayfası için "Dizine eklenmesini iste" de.
4. https://search.google.com/test/rich-results ile ana sayfa ve fiyatlar sayfasını test et
   (Product, FAQPage ve Organization şemaları görünmeli).
5. https://pagespeed.web.dev ile mobil hızı ölç.
6. Her ay 2–4 yeni rehber yazısı ekle (plan dokümanındaki başlıklar). Hizmet sayfalarını da
   zamanla müşteri sorularıyla genişlet; şu an her biri 250–400 kelime, hedef 600+ kelime.

## 5. Yeniden üretmek için (isteğe bağlı)

Sayfalar `kaynak/content/` klasöründeki parçalardan `kaynak/build.py` ile üretildi. İçeriği
orada düzenleyip `python3 build.py` çalıştırırsan tüm sayfalar, sitemap ve şemalar yeniden
oluşur; yeni blog yazısı eklediğinde sitemap kendiliğinden güncellenir.
