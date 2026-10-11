import cv2
import mediapipe as mp
import pyautogui
import time

# Kamera başlatma
cap = cv2.VideoCapture(0)

# MediaPipe El Takibi ayarları
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Ekran çözünürlüğünü alma
screen_w, screen_h = pyautogui.size()

# İşlemlerin üst üste binmesini engellemek için zamanlayıcılar
last_click_time = 0
last_copy_time = 0
cooldown_duration = 1.0  # Saniye cinsinden bekleme süresi

while True:
    success, img = cap.read()
    if not success:
        break

    # Görüntüyü aynalama yap ve RGB formatına çevir
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm = handLms.landmark

            # 1. MOUSE HAREKETİ (İşaret Parmağı - Landmark 8)
            x = lm[8].x
            y = lm[8].y
            mouse_x = screen_w * x
            mouse_y = screen_h * y
            pyautogui.moveTo(mouse_x, mouse_y)

            # PARMAK DURUMLARINI KONTROL ET (Y koordinatı aşağı doğru artar)
            # Eğer uç nokta (tip), bir alt eklemden (pip/mcp) daha aşağıdaysa parmak kapalıdır.
            index_closed = lm[8].y > lm[6].y
            middle_closed = lm[12].y > lm[10].y
            ring_closed = lm[16].y > lm[14].y
            pinky_closed = lm[20].y > lm[18].y
            
            # Baş parmak kontrolü (Yukarı doğru bakıyorsa açık kabul edilir)
            thumb_open = lm[4].y < lm[2].y

            current_time = time.time()

            # 2. YUMRUK HAREKETİ -> KOPYALAMA (Ctrl + C)
            # Tüm parmaklar (baş parmak dahil) kapalıysa
            if index_closed and middle_closed and ring_closed and pinky_closed and not thumb_open:
                if current_time - last_copy_time > cooldown_duration:
                    pyautogui.hotkey('ctrl', 'c')
                    print("Kopyalandı! (Ctrl+C)")
                    last_copy_time = current_time

            # 3. BAŞ PARMAK HAREKETİ -> TIKLAMA (Click)
            # Diğer tüm parmaklar kapalı ama sadece baş parmak yukarı doğru açıksa
            elif index_closed and middle_closed and ring_closed and pinky_closed and thumb_open:
                if current_time - last_click_time > cooldown_duration:
                    pyautogui.click()
                    print("Tıklandı!")
                    last_click_time = current_time

            # Ekranda el eklemlerini çiz
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # Görüntüyü ekranda göster
    cv2.imshow("El ile Mouse Kontrol", img)

    # 'ESC' tuşuna basılırsa döngüden çık
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
