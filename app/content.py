from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Category:
    id: str
    label: str
    icon: str
    size: tuple[int, int]
    photo_tip: str


CATEGORIES: dict[str, Category] = {
    "daily_work": Category(
        id="daily_work",
        label="Günlük İş",
        icon="🚗",
        size=(1080, 1080),
        photo_tip="Tamir edilen parça veya araç net görünsün.",
    ),
    "campaign": Category(
        id="campaign",
        label="Kampanya / İndirim",
        icon="🏷️",
        size=(1080, 1080),
        photo_tip="Servis, araç veya kampanyayı temsil eden temiz bir kare seçin.",
    ),
    "customer": Category(
        id="customer",
        label="Müşteri Memnuniyeti",
        icon="⭐",
        size=(1080, 1080),
        photo_tip="Müşteri izniyle teslim anı veya yorum ekran görüntüsü kullanın.",
    ),
    "towing": Category(
        id="towing",
        label="Çekici Hizmeti",
        icon="🚛",
        size=(1080, 1350),
        photo_tip="Çekici aracı veya kurtarma anını dikey kadraja alın.",
    ),
}

TONES = {
    "story": "Hikaye",
    "short": "Kısa & Net",
    "educational": "Eğitici",
    "urgent": "Acil / CTA",
}

HASHTAGS = {
    "campaign": "#kampanya #indirim #otoservis #araçbakım #şaşmaz #ankara #fırsat #hcotomotiv #uygunfiyat #servis",
    "daily_work": "#gününtamiri #otoservis #mekanik #araçtamiri #şaşmaz #ankara #hcotomotiv #tamirci #servis #otomotiv",
    "customer": "#müşterimemnuniyeti #googleyorum #güvenilir #otoservis #şaşmaz #ankara #hcotomotiv #5yıldız #referans",
    "towing": "#çekici #yoldakaldım #ücretsizçekici #acilservis #ankara #şaşmaz #hcotomotiv #araçkurtarma #7günacık",
}

TEMPLATES: dict[str, dict[str, list[str]]] = {
    "campaign": {
        "story": [
            "🏷️ KAMPANYA!\n\n{t}\n\n⏰ Sınırlı süre — Randevunuzu hemen oluşturun!\n\n📍 H&C Otomotiv | Şaşmaz Oto Sanayi\n📞 0541 970 09 11\n💬 WhatsApp: wa.me/905419700911"
        ],
        "short": [
            "🔥 {t}\n\nKaçırmayın!\n\n📍 Şaşmaz | 7/7 açık\n📞 0541 970 09 11"
        ],
        "educational": [
            "💰 {t}\n\nNeden bu kampanya?\nÇünkü düzenli bakım, pahalı tamirden her zaman ucuzdur.\n\n📍 H&C Otomotiv | Şaşmaz\n📞 0541 970 09 11"
        ],
        "urgent": [
            "🚨 SON GÜNLER!\n\n{t}\n\nBu fırsat kaçmadan hemen arayın!\n\n📞 0541 970 09 11\n📍 Şaşmaz Oto Sanayi\n💬 WhatsApp: wa.me/905419700911"
        ],
    },
    "daily_work": {
        "story": [
            "🚗 Bugün atölyemizde: {t}\n\nCihazla arıza tespiti → teşhis → onarım → test sürüşü → teslim.\n\nHer iş titizlikle, her araç özenle.\n\n📍 H&C Otomotiv | Şaşmaz\n📞 0541 970 09 11\n🚛 Yolda mı kaldınız? Çekici bizden!",
            "🔧 Günün işi: {t}\n\nMüşterimiz sorunu anlattı, biz dinledik, teşhis koyduk ve aynı gün çözdük.\n\nAracınız güvende, siz de rahat olun.\n\n📍 Şaşmaz Oto Sanayi — 7/7 açık\n📞 0541 970 09 11",
        ],
        "short": [
            "🔧 {t} ✅\n\nBugün de bir araç daha yola çıktı.\n\n📍 H&C | Şaşmaz\n📞 0541 970 09 11"
        ],
        "educational": [
            "🔍 Bugün gelen araç: {t}\n\nBu arızanın sebebi neydi? Belirtileri nelerdi?\nKaydırarak öğrenin 👉\n\n📍 H&C Otomotiv | Şaşmaz\n📞 0541 970 09 11"
        ],
        "urgent": [
            "✅ {t} — Aynı gün çözüm!\n\nAracınızda sorun mu var? Ertelemeyin.\n\n📞 0541 970 09 11\n📍 Şaşmaz Oto Sanayi"
        ],
    },
    "customer": {
        "story": [
            "⭐⭐⭐⭐⭐\n\n{t}\n\nMüşterilerimizin memnuniyeti bizim için en değerli referans.\n\n📍 H&C Otomotiv | Şaşmaz\n📞 0541 970 09 11\n\n💬 Siz de deneyiminizi Google'da paylaşın!"
        ],
        "short": [
            "⭐ {t}\n\nTeşekkürler! 🙏\n\n📍 H&C | Şaşmaz\n📞 0541 970 09 11"
        ],
        "educational": [
            "🙏 {t}\n\nMüşteri güveni nasıl kazanılır? Dürüst teşhis, şeffaf fiyat, kaliteli işçilik.\n\n📍 H&C Otomotiv | Şaşmaz\n📞 0541 970 09 11"
        ],
        "urgent": [
            "⭐ {t}\n\nSiz de güvenilir servis arıyorsanız hemen arayın!\n\n📞 0541 970 09 11\n📍 Şaşmaz Oto Sanayi"
        ],
    },
    "towing": {
        "story": [
            "🚛 {t}\n\nYolda mı kaldınız? Endişelenmeyin!\nServisimizde tamir yaptırın, çekici ücreti bizden! 🆓\n\n📞 Hemen arayın: 0541 970 09 11\n📍 H&C Otomotiv | Şaşmaz"
        ],
        "short": [
            "🆘 {t}\n\nÇekici bizden!\n\n📞 0541 970 09 11\n📍 Şaşmaz"
        ],
        "educational": [
            "🚛 {t}\n\nYolda kalınca ne yapmalı?\n1. Güvenli yere çekin\n2. Dörtlüleri açın\n3. Bizi arayın: 0541 970 09 11\n\nGerisini biz hallederiz.\n\n📍 H&C Otomotiv | Şaşmaz"
        ],
        "urgent": [
            "🆘 YOLDA MI KALDINIZ?\n\n{t}\n\n7/24 çekici hizmeti — ücretsiz!\nHemen arayın!\n\n📞 0541 970 09 11\n📍 H&C Otomotiv | Şaşmaz"
        ],
    },
}

IDEAS = {
    "daily_work": [
        "Renault Clio motor bakımı",
        "Fiat Egea fren sistemi tamiri",
        "Ford Focus süspansiyon değişimi",
        "VW Polo klima gaz dolumu",
        "Hyundai i20 periyodik bakım",
        "Toyota Corolla motor arıza tespiti",
        "Opel Astra triger seti değişimi",
        "Honda Civic fren balata değişimi",
    ],
    "campaign": [
        "Bu hafta periyodik bakımda %15 indirim",
        "Yaz klima bakım kampanyası — 500₺'den başlayan",
        "Fren bakımı yaptırana ücretsiz araç kontrol",
        "İlk ziyaretinize özel %10 indirim",
    ],
    "customer": [
        "Google'da 5 yıldızlı yeni yorumumuz",
        "Müşterimiz aracını memnuniyetle teslim aldı",
        "Düzenli müşterimizden güzel sözler",
        "Tavsiye ile gelen müşteri sayımız artıyor!",
    ],
    "towing": [
        "Yolda kalan müşterimizin aracını 30 dakikada kurtardık!",
        "Çekici hizmetimiz 7/24 aktif — Ankara genelinde yanınızdayız",
        "Servisimizde tamir yaptırın, çekici ücreti tamamen bizden",
        "Gece 2'de aradılar, 40 dakikada oradaydık",
    ],
}

WEEKLY = [
    {"day": "Pazartesi", "catId": "daily_work", "hint": "Hafta başı — bugünkü ilk işin fotoğrafı"},
    {"day": "Salı", "catId": "customer", "hint": "Müşteri memnuniyeti veya teslim anı"},
    {"day": "Çarşamba", "catId": "daily_work", "hint": "Tamamlanan bir tamir işini paylaş"},
    {"day": "Perşembe", "catId": "towing", "hint": "Çekici hizmeti vurgusu"},
    {"day": "Cuma", "catId": "campaign", "hint": "Hafta sonu kampanyası"},
    {"day": "Cumartesi", "catId": "daily_work", "hint": "Servisten doğal bir iş karesi"},
    {"day": "Pazar", "catId": "customer", "hint": "Güven veren yorum veya teşekkür postu"},
]

MONTHS_TR = [
    "",
    "Ocak",
    "Şubat",
    "Mart",
    "Nisan",
    "Mayıs",
    "Haziran",
    "Temmuz",
    "Ağustos",
    "Eylül",
    "Ekim",
    "Kasım",
    "Aralık",
]


def generate_caption(category: str, tone: str, content: str, variant: int = 0) -> tuple[str, str]:
    category_templates = TEMPLATES.get(category)
    if not category_templates:
        raise ValueError("Geçersiz kategori seçildi.")

    tone_templates = category_templates.get(tone) or category_templates["story"]
    template = tone_templates[variant % len(tone_templates)]
    return template.format(t=content.strip()), HASHTAGS[category]


def format_turkish_date(day: date) -> str:
    return f"{day.day} {MONTHS_TR[day.month]} {day.year}"

