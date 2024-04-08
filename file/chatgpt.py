def bmi_hesapla(kilo, boy):
    # BMI hesapla: BMI = kilo / (boy^2)
    bmi = kilo / (boy ** 2)
    return bmi

def bmi_durumu(bmi):
    # BMI durumunu belirle
    if bmi < 18.5:
        return "Zayıf"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Fazla Kilolu"
    else:
        return "Obez"

def main():
    # Kullanıcıdan kilo ve boy bilgilerini al
    kilo = float(input("Kilonuzu kilogram cinsinden girin: "))
    boy = float(input("Boyunuzu metre cinsinden girin: "))

    # BMI hesapla
    bmi = bmi_hesapla(kilo, boy)

    # BMI durumunu belirle
    durum = bmi_durumu(bmi)

    # Sonucu ekrana yazdır
    print(f"\nBMI: {bmi:.2f}")
    print(f"Durum: {durum}")

if __name__ == "__main__":
    main()