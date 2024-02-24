import cv2
import imutils
import pyautogui
#Gerekli kütüphaneleri içe aktarır.
target_range_green = ((35, 80, 20), (70, 255, 255))
#Fıstık yeşili için hedef renk aralığını belirler.
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#Kamerayı başlatır ve çerçeve genişliği ve yüksekliğini ayarlar.
cv2.namedWindow('Kare')
cv2.moveWindow('Kare', 10, 10)
#'Kare' adında bir pencere oluşturur ve konumunu ayarlar.
target_range_red = ((0, 100, 100), (10, 255, 255))
#Kırmızı renk için hedef renk aralığını belirler.
left_clicked = False
#Sol tıklama işlemini kontrol etmek için bir bayrak değişkeni tanımlar.
while True:
#Ana döngüye girer.
    ok, kare = camera.read()
    if not ok:
        break
#Kare okur ve eğer başarısızsa döngüyü sonlandırır.
    kare = cv2.flip(kare, 1)
    kare = imutils.resize(kare, width=800)
    hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)
#Kareyi yatay olarak çevirir, boyutunu yeniden ayarlar ve HSV renk uzayına dönüştürür.
    mask_green = cv2.inRange(hsv, target_range_green[0], target_range_green[1])
    mask_red = cv2.inRange(hsv, target_range_red[0], target_range_red[1])
#Fıstık yeşili ve kırmızı renk maskelerini oluşturur.
    mask_green = cv2.erode(mask_green, None, iterations=3)
    mask_green = cv2.dilate(mask_green, None, iterations=3)
    mask_red = cv2.erode(mask_red, None, iterations=3)
    mask_red = cv2.dilate(mask_red, None, iterations=3)
#Fıstık yeşili ve kırmızı renk maskelerini oluşturur.
    contours_green = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green = imutils.grab_contours(contours_green)
#Fıstık yeşili için konturları bulur.
    if len(contours_green) > 0:
        c_max = max(contours_green, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c_max)
        if radius >= 20:
            pyautogui.moveTo(x * 2, y * 2)  # PyAutoGUI x, y koordinatlarına uygun şekilde ayarlanmalıdır
            cv2.circle(kare, (int(x), int(y)), int(radius), (0, 255, 255), 2)
#Eğer yeşil konturlar bulunursa, en büyük konturu bulur ve bu konturun çevreleyen dairenin
# merkezini ve yarıçapını hesaplar. Eğer yarıçap 20'den büyükse, PyAutoGUI ile fareyi belirtilen
# koordinatlara hareket ettirir ve kare üzerinde çevreleyen daireyi çizer.
    contours_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red = imutils.grab_contours(contours_red)
#Kırmızı konturları bulur.
    if len(contours_red) > 0:
        c_max = max(contours_red, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c_max)
        if radius >= 20:
            if not left_clicked:
                pyautogui.mouseDown()
                left_clicked = True
            cv2.circle(kare, (int(x), int(y)), int(radius), (0, 0, 255), 2)
        else:
            if left_clicked:
                pyautogui.mouseUp()
                left_clicked = False
#Eğer kırmızı konturlar bulunursa, en büyük konturu bulur ve bu konturun çevreleyen dairenin
# merkezini ve yarıçapını hesaplar. Eğer yarıçap 20'den büyükse, sol tıklama işlemi yapar.
# Eğer yarıçap 20'den küçükse, sol tıklama işlemi sonlandırır.
    cv2.imshow('Kare', kare)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#Kareyi gösterir ve eğer 'q' tuşuna basılırsa döngüyü sonlandırır.
camera.release()
cv2.destroyAllWindows()
#Kamerayı serbest bırakır ve tüm pencereleri kapatır.