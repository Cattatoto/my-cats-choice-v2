

import streamlit as st
from google import genai
from PIL import Image
import io

st.set_page_config(
    page_title="My Cat's Choice 2.0",
    page_icon="🐱",
    layout="wide"
)

# --------------------------------------------------
# LANGUAGES
# --------------------------------------------------

LANGUAGES = {
    "English": {
        "title": "My Cat's Choice",
        "subtitle": "Make smarter product choices with AI.",
        "language": "Choose your language",
        "product_a": "Product A",
        "product_b": "Product B",
        "photo_method": "How would you like to add your photo?",
        "upload": "Upload a photo",
        "camera": "Take a photo",
        "price": "Product price",
        "quantity": "Product quantity",
        "currency": "Currency",
        "preferences": "What matters to you?",
        "preferences_hint": "For example: natural ingredients, low sugar, fragrance-free",
        "compare": "Compare Products",
        "missing": "Please add photos of both products.",
        "working": "AI is analysing your products. Please wait...",
        "results": "Your AI comparison",
        "disclaimer": "AI results may contain errors. Check product labels and important claims before purchasing.",
        "no_key": "The app administrator must configure the Gemini API key in Streamlit Secrets.",
        "camera_help": "On a phone, your browser may ask permission to use the camera."
    },
    "ไทย": {
        "title": "My Cat's Choice",
        "subtitle": "เลือกสินค้าได้อย่างชาญฉลาดด้วย AI",
        "language": "เลือกภาษา",
        "product_a": "สินค้า A",
        "product_b": "สินค้า B",
        "photo_method": "คุณต้องการเพิ่มรูปภาพอย่างไร?",
        "upload": "อัปโหลดรูปภาพ",
        "camera": "ถ่ายภาพ",
        "price": "ราคาสินค้า",
        "quantity": "ปริมาณสินค้า",
        "currency": "สกุลเงิน",
        "preferences": "สิ่งที่คุณให้ความสำคัญ",
        "preferences_hint": "เช่น ส่วนผสมจากธรรมชาติ น้ำตาลต่ำ ไม่มีกลิ่นน้ำหอม",
        "compare": "เปรียบเทียบสินค้า",
        "missing": "กรุณาเพิ่มรูปภาพสินค้าทั้งสองรายการ",
        "working": "AI กำลังวิเคราะห์สินค้า กรุณารอสักครู่...",
        "results": "ผลการเปรียบเทียบด้วย AI",
        "disclaimer": "ผลลัพธ์จาก AI อาจมีข้อผิดพลาด โปรดตรวจสอบฉลากสินค้าก่อนซื้อ",
        "no_key": "ผู้ดูแลระบบต้องตั้งค่า Gemini API key ใน Streamlit Secrets",
        "camera_help": "โทรศัพท์ของคุณอาจขออนุญาตใช้กล้อง"
    },
    "Tiếng Việt": {
        "title": "My Cat's Choice",
        "subtitle": "Lựa chọn sản phẩm thông minh hơn với AI.",
        "language": "Chọn ngôn ngữ",
        "product_a": "Sản phẩm A",
        "product_b": "Sản phẩm B",
        "photo_method": "Bạn muốn thêm ảnh bằng cách nào?",
        "upload": "Tải ảnh lên",
        "camera": "Chụp ảnh",
        "price": "Giá sản phẩm",
        "quantity": "Số lượng sản phẩm",
        "currency": "Tiền tệ",
        "preferences": "Điều gì quan trọng với bạn?",
        "preferences_hint": "Ví dụ: thành phần tự nhiên, ít đường, không hương liệu",
        "compare": "So sánh sản phẩm",
        "missing": "Vui lòng thêm ảnh của cả hai sản phẩm.",
        "working": "AI đang phân tích sản phẩm. Vui lòng chờ...",
        "results": "Kết quả so sánh AI",
        "disclaimer": "Kết quả AI có thể có sai sót. Hãy kiểm tra nhãn sản phẩm trước khi mua.",
        "no_key": "Quản trị viên cần cấu hình Gemini API key trong Streamlit Secrets.",
        "camera_help": "Trình duyệt trên điện thoại có thể yêu cầu quyền sử dụng máy ảnh."
    },
    "中文": {
        "title": "My Cat's Choice",
        "subtitle": "借助 AI 做出更明智的产品选择。",
        "language": "选择语言",
        "product_a": "产品 A",
        "product_b": "产品 B",
        "photo_method": "您希望如何添加照片？",
        "upload": "上传照片",
        "camera": "拍摄照片",
        "price": "产品价格",
        "quantity": "产品数量",
        "currency": "货币",
        "preferences": "您最看重什么？",
        "preferences_hint": "例如：天然成分、低糖、无香料",
        "compare": "比较产品",
        "missing": "请添加两种产品的照片。",
        "working": "AI 正在分析产品，请稍候...",
        "results": "AI 比较结果",
        "disclaimer": "AI 结果可能存在错误。购买前请核实产品标签。",
        "no_key": "管理员需要在 Streamlit Secrets 中配置 Gemini API 密钥。",
        "camera_help": "手机浏览器可能会请求相机使用权限。"
    },
    "한국어": {
        "title": "My Cat's Choice",
        "subtitle": "AI로 더 현명한 제품을 선택하세요.",
        "language": "언어 선택",
        "product_a": "제품 A",
        "product_b": "제품 B",
        "photo_method": "사진을 어떻게 추가하시겠습니까?",
        "upload": "사진 업로드",
        "camera": "사진 촬영",
        "price": "제품 가격",
        "quantity": "제품 수량",
        "currency": "통화",
        "preferences": "무엇을 중요하게 생각하시나요?",
        "preferences_hint": "예: 천연 성분, 저당, 무향",
        "compare": "제품 비교",
        "missing": "두 제품의 사진을 모두 추가해 주세요.",
        "working": "AI가 제품을 분석하고 있습니다. 잠시 기다려 주세요...",
        "results": "AI 비교 결과",
        "disclaimer": "AI 결과에는 오류가 있을 수 있습니다. 구매 전에 제품 라벨을 확인하세요.",
        "no_key": "관리자는 Streamlit Secrets에 Gemini API 키를 설정해야 합니다.",
        "camera_help": "휴대전화 브라우저에서 카메라 권한을 요청할 수 있습니다."
    },
    "हिन्दी": {
        "title": "My Cat's Choice",
        "subtitle": "AI की मदद से बेहतर उत्पाद चुनें।",
        "language": "अपनी भाषा चुनें",
        "product_a": "उत्पाद A",
        "product_b": "उत्पाद B",
        "photo_method": "आप फोटो कैसे जोड़ना चाहेंगे?",
        "upload": "फोटो अपलोड करें",
        "camera": "फोटो लें",
        "price": "उत्पाद की कीमत",
        "quantity": "उत्पाद की मात्रा",
        "currency": "मुद्रा",
        "preferences": "आपके लिए क्या महत्वपूर्ण है?",
        "preferences_hint": "उदाहरण: प्राकृतिक सामग्री, कम चीनी, खुशबू रहित",
        "compare": "उत्पादों की तुलना करें",
        "missing": "कृपया दोनों उत्पादों की फोटो जोड़ें।",
        "working": "AI आपके उत्पादों का विश्लेषण कर रहा है। कृपया प्रतीक्षा करें...",
        "results": "AI तुलना परिणाम",
        "disclaimer": "AI के परिणाम गलत हो सकते हैं। खरीदने से पहले उत्पाद का लेबल जांचें।",
        "no_key": "व्यवस्थापक को Streamlit Secrets में Gemini API key सेट करनी होगी।",
        "camera_help": "आपका मोबाइल ब्राउज़र कैमरे की अनुमति मांग सकता है।"
    },
    "العربية": {
        "title": "My Cat's Choice",
        "subtitle": "اتخذ قرارات أفضل بشأن المنتجات باستخدام الذكاء الاصطناعي.",
        "language": "اختر لغتك",
        "product_a": "المنتج أ",
        "product_b": "المنتج ب",
        "photo_method": "كيف تريد إضافة الصورة؟",
        "upload": "تحميل صورة",
        "camera": "التقاط صورة",
        "price": "سعر المنتج",
        "quantity": "كمية المنتج",
        "currency": "العملة",
        "preferences": "ما الذي يهمك؟",
        "preferences_hint": "مثال: مكونات طبيعية، سكر منخفض، بدون عطر",
        "compare": "قارن المنتجات",
        "missing": "يرجى إضافة صور المنتجين.",
        "working": "يقوم الذكاء الاصطناعي بتحليل المنتجات. يرجى الانتظار...",
        "results": "نتائج المقارنة بالذكاء الاصطناعي",
        "disclaimer": "قد تحتوي نتائج الذكاء الاصطناعي على أخطاء. تحقق من الملصقات قبل الشراء.",
        "no_key": "يجب على المسؤول إعداد مفتاح Gemini API في Streamlit Secrets.",
        "camera_help": "قد يطلب متصفح هاتفك إذن استخدام الكاميرا."
    },
    "Deutsch": {
        "title": "My Cat's Choice",
        "subtitle": "Treffen Sie mit KI bessere Produktentscheidungen.",
        "language": "Sprache auswählen",
        "product_a": "Produkt A",
        "product_b": "Produkt B",
        "photo_method": "Wie möchten Sie Ihr Foto hinzufügen?",
        "upload": "Foto hochladen",
        "camera": "Foto aufnehmen",
        "price": "Produktpreis",
        "quantity": "Produktmenge",
        "currency": "Währung",
        "preferences": "Was ist Ihnen wichtig?",
        "preferences_hint": "Zum Beispiel: natürliche Inhaltsstoffe, wenig Zucker, parfümfrei",
        "compare": "Produkte vergleichen",
        "missing": "Bitte laden Sie Fotos von beiden Produkten hoch.",
        "working": "Die KI analysiert Ihre Produkte. Bitte warten...",
        "results": "Ihr KI-Vergleich",
        "disclaimer": "KI-Ergebnisse können Fehler enthalten. Prüfen Sie vor dem Kauf die Produktetiketten.",
        "no_key": "Der Administrator muss den Gemini API-Schlüssel in Streamlit Secrets einrichten.",
        "camera_help": "Ihr Smartphone-Browser kann nach Kamerazugriff fragen."
    },
    "Türkçe": {
        "title": "My Cat's Choice",
        "subtitle": "Yapay zekâ ile daha akıllı ürün seçimleri yapın.",
        "language": "Dil seçin",
        "product_a": "Ürün A",
        "product_b": "Ürün B",
        "photo_method": "Fotoğrafı nasıl eklemek istersiniz?",
        "upload": "Fotoğraf yükle",
        "camera": "Fotoğraf çek",
        "price": "Ürün fiyatı",
        "quantity": "Ürün miktarı",
        "currency": "Para birimi",
        "preferences": "Sizin için ne önemli?",
        "preferences_hint": "Örneğin: doğal içerikler, düşük şeker, parfümsüz",
        "compare": "Ürünleri karşılaştır",
        "missing": "Lütfen her iki ürünün de fotoğrafını ekleyin.",
        "working": "Yapay zekâ ürünlerinizi analiz ediyor. Lütfen bekleyin...",
        "results": "Yapay zekâ karşılaştırması",
        "disclaimer": "Yapay zekâ sonuçları hatalı olabilir. Satın almadan önce ürün etiketlerini kontrol edin.",
        "no_key": "Yönetici, Gemini API anahtarını Streamlit Secrets bölümünde ayarlamalıdır.",
        "camera_help": "Telefon tarayıcınız kamera izni isteyebilir."
    },
    "Italiano": {
        "title": "My Cat's Choice",
        "subtitle": "Scegli prodotti migliori con l'intelligenza artificiale.",
        "language": "Scegli la lingua",
        "product_a": "Prodotto A",
        "product_b": "Prodotto B",
        "photo_method": "Come vuoi aggiungere la foto?",
        "upload": "Carica una foto",
        "camera": "Scatta una foto",
        "price": "Prezzo del prodotto",
        "quantity": "Quantità del prodotto",
        "currency": "Valuta",
        "preferences": "Che cosa è importante per te?",
        "preferences_hint": "Ad esempio: ingredienti naturali, poco zucchero, senza profumo",
        "compare": "Confronta prodotti",
        "missing": "Aggiungi le foto di entrambi i prodotti.",
        "working": "L'IA sta analizzando i prodotti. Attendi...",
        "results": "Confronto AI",
        "disclaimer": "I risultati dell'IA possono contenere errori. Controlla le etichette prima dell'acquisto.",
        "no_key": "L'amministratore deve configurare la chiave Gemini API in Streamlit Secrets.",
        "camera_help": "Il browser del telefono potrebbe chiedere il permesso di usare la fotocamera."
    },
    "日本語": {
        "title": "My Cat's Choice",
        "subtitle": "AIでより賢い商品選びを。",
        "language": "言語を選択",
        "product_a": "商品 A",
        "product_b": "商品 B",
        "photo_method": "写真をどのように追加しますか？",
        "upload": "写真をアップロード",
        "camera": "写真を撮る",
        "price": "商品の価格",
        "quantity": "商品の数量",
        "currency": "通貨",
        "preferences": "何を重視しますか？",
        "preferences_hint": "例：天然成分、低糖、無香料",
        "compare": "商品を比較する",
        "missing": "両方の商品の写真を追加してください。",
        "working": "AIが商品を分析しています。しばらくお待ちください...",
        "results": "AI比較結果",
        "disclaimer": "AIの結果には誤りが含まれる場合があります。購入前に商品ラベルを確認してください。",
        "no_key": "管理者はStreamlit SecretsにGemini APIキーを設定する必要があります。",
        "camera_help": "スマートフォンのブラウザがカメラの使用許可を求める場合があります。"
    }
}

# --------------------------------------------------
# LANGUAGE SELECTION
# --------------------------------------------------

st.title("🐱 My Cat's Choice 2.0")

language = st.selectbox(
    "🌐 Choose your language / เลือกภาษา / Chọn ngôn ngữ",
    list(LANGUAGES.keys()),
    index=0
)

t = LANGUAGES[language]

st.subheader(t["subtitle"])

# --------------------------------------------------
# PHOTO INPUT
# --------------------------------------------------

def product_input(label, key):
    st.markdown(f"### {label}")

    method = st.radio(
        t["photo_method"],
        [t["upload"], t["camera"]],
        horizontal=True,
        key=f"method_{key}"
    )

    if method == t["upload"]:
        photo = st.file_uploader(
            t["upload"],
            type=["jpg", "jpeg", "png", "webp"],
            key=f"upload_{key}"
        )
    else:
        st.caption(t["camera_help"])
        photo = st.camera_input(
            t["camera"],
            key=f"camera_{key}"
        )

    return photo


col_a, col_b = st.columns(2)

with col_a:
    photo_a = product_input(t["product_a"], "a")
    price_a = st.number_input(
        f"{t['price']} — A",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="price_a"
    )
    quantity_a = st.number_input(
        f"{t['quantity']} — A",
        min_value=0.01,
        value=1.0,
        step=1.0,
        key="quantity_a"
    )

with col_b:
    photo_b = product_input(t["product_b"], "b")
    price_b = st.number_input(
        f"{t['price']} — B",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="price_b"
    )
    quantity_b = st.number_input(
        f"{t['quantity']} — B",
        min_value=0.01,
        value=1.0,
        step=1.0,
        key="quantity_b"
    )

currency = st.text_input(
    t["currency"],
    value="INR"
)

st.divider()

preferences = st.text_area(
    t["preferences"],
    placeholder=t["preferences_hint"]
)

# --------------------------------------------------
# AI COMPARISON
# --------------------------------------------------

if st.button(t["compare"], type="primary", use_container_width=True):

    if photo_a is None or photo_b is None:
        st.error(t["missing"])

    else:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")

            if not api_key:
                st.error(t["no_key"])
                st.stop()

            image_a = Image.open(io.BytesIO(photo_a.getvalue())).convert("RGB")
            image_b = Image.open(io.BytesIO(photo_b.getvalue())).convert("RGB")

            image_a.thumbnail((1600, 1600))
            image_b.thumbnail((1600, 1600))

            client = genai.Client(api_key=api_key)

            prompt = f"""
You are My Cat's Choice, an independent consumer product comparison assistant.

Analyse the TWO attached product photographs.

The user's selected language is: {language}

IMPORTANT:
- Write your entire answer in {language}.
- Understand packaging text even if it is written in another language.
- Identify each product and its likely category.
- Read visible ingredients, materials, features and claims.
- Compare the products fairly.
- Explain benefits and possible disadvantages.
- Identify potential allergens or ingredients that deserve attention when visible.
- Do not invent missing ingredients, certifications, safety facts or product claims.
- Clearly distinguish visible facts from your own interpretation.
- If text is unclear, say that it cannot be read reliably.
- Do not claim that a product is safe or medically suitable based only on a photo.

USER INFORMATION:

Product A price: {price_a} {currency}
Product A quantity: {quantity_a}

Product B price: {price_b} {currency}
Product B quantity: {quantity_b}

User preferences: {preferences if preferences.strip() else "No preferences provided."}

If a price is zero, treat it as not provided.
Calculate price per unit only when a valid price and quantity are available.

Please organise the answer using these sections:

1. PRODUCT IDENTIFICATION
2. PRODUCT A - INGREDIENTS / MATERIALS / FEATURES
3. PRODUCT B - INGREDIENTS / MATERIALS / FEATURES
4. SIDE-BY-SIDE COMPARISON
5. BENEFITS OF EACH PRODUCT
6. POSSIBLE DISADVANTAGES
7. USER PREFERENCE MATCH
8. PRICE AND VALUE COMPARISON
9. FINAL RECOMMENDATION

In the final recommendation:
- Say which product is the better match for the user's stated preferences, if enough information exists.
- Explain the main reason.
- Mention trade-offs.
- If there is insufficient information, say so rather than guessing.

Use clear headings and concise language.
"""

            with st.spinner(t["working"]):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        prompt,
                        image_a,
                        image_b
                    ]
                )

            st.success(t["results"])
            st.markdown(response.text or "No response was returned.")

            st.divider()
            st.caption(t["disclaimer"])

        except Exception as e:
            st.error(f"Comparison failed: {e}")
            st.info(
                "Please check your API key, internet connection, "
                "Gemini free-tier availability and uploaded images."
            )

st.divider()
st.caption("My Cat's Choice 2.0 | AI-assisted product comparison")
