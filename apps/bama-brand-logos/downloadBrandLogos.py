import requests
import os

# پوشه خروجی لوگوها
folder_name = "data/logos_svg"
os.makedirs(folder_name, exist_ok=True)

# URL API
api_url = "https://bama.ir/cad/api/BasicInfo/vehicles"

try:
    # دریافت اطلاعات از API
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    brands = data.get("data", [])
    brands_dict = {
        b["name"]: b["logo"]
        for b in brands
        if "name" in b and "logo" in b and b["logo"]
    }

    if not brands_dict:
        print("هیچ لوگویی در داده‌های API یافت نشد.")
        exit()

    success_count = 0
    failed = []

    # دانلود هر لوگو
    for brand_name, logo_url in brands_dict.items():
        try:
            res = requests.get(logo_url)
            res.raise_for_status()

            file_name = f"{brand_name}.svg"
            full_path = os.path.join(folder_name, file_name)

            with open(full_path, "wb") as f:
                f.write(res.content)

            print(f"✓ {brand_name} ذخیره شد.")
            success_count += 1
        except requests.exceptions.RequestException as e:
            print(f"⚠️ خطا در دانلود لوگوی {brand_name}: {e}")
            failed.append(brand_name)

    # گزارش نهایی
    print("\n--- خلاصه عملیات ---")
    print(f"تعداد کل برندها: {len(brands_dict)}")
    print(f"تعداد ذخیره موفق: {success_count}")
    if failed:
        print(f"تعداد فایل‌های ناموفق: {len(failed)}")
        print(f"برندهای ناموفق: {', '.join(failed)}")

except requests.exceptions.RequestException as e:
    print(f"خطا در دریافت داده از API: {e}")
except Exception as e:
    print(f"خطای غیرمنتظره: {e}")
