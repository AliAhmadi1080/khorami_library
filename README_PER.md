# سیستم مدیریت کتابخانه

این یک سیستم مدیریت کتابخانه مبتنی بر جنگو برای مدیریت کتاب‌ها، کاربران و امانت‌ها در یک کتابخانه مدرسه است.

## ویژگی‌ها

- **مدیریت کاربران**:

  - مدل کاربر سفارشی با فیلدهایی مانند fullname، classname، joined_number و username.
  - فرم و نمای ایجاد کاربر.

- **مدیریت کتاب‌ها**:

  - مدل کتاب با فیلدهایی مانند name، code و row_number.
  - فرم و نمای جستجوی کتاب.

- **مدیریت امانت‌ها**:

  - مدل امانت با فیلدهایی مانند book، user، loan_date، return_date، is_return و notes.
  - فرم و نمای ایجاد امانت.
  - نمای بازگرداندن امانت.

- **وارد کردن PDF**:

  - تابعی برای مدیریت فایل‌های PDF آپلود شده و استخراج داده‌های کتاب.
  - نمای وارد کردن فایل‌های اکسل.

- **داشبورد**:
  - نمای داشبورد نمایش آمار امانت‌ها.

## نصب

1. مخزن را کلون کنید:

   ```sh
   git clone https://github.com/AliAhmadi1080/khorami_library
   cd khorami_library
   ```

2. یک محیط مجازی ایجاد و فعال کنید:

   ```sh
   python -m venv venv
   source venv/bin/activate  # در ویندوز از `venv\Scripts\activate` استفاده کنید
   ```

3. وابستگی‌ها را نصب کنید:

   ```sh
   pip install -r requirements.txt
   ```

4. مهاجرت‌ها را اعمال کنید:

   ```sh
   python manage.py migrate
   ```

5. یک کاربر ابر ایجاد کنید:

   ```sh
   python manage.py createsuperuser
   ```

6. سرور توسعه را اجرا کنید:

   ```sh
   python manage.py runserver
   ```

7. به برنامه در [http://127.0.0.1:8000/](http://127.0.0.1:8000/) دسترسی پیدا کنید.

## استفاده

- **ورود**: به صفحه ورود در `/account/login/` دسترسی پیدا کنید.
- **داشبورد**: به داشبورد در `/dashbord/` دسترسی پیدا کنید.
- **ایجاد کاربر**: یک کاربر جدید در `/create_user/` ایجاد کنید.
- **ایجاد امانت**: یک امانت جدید در `/create_loan/` ایجاد کنید.
- **جستجوی کتاب‌ها**: کتاب‌ها را در `/search_books/` جستجو کنید.
- **وارد کردن فایل PDF**: داده‌های کتاب را از یک فایل PDF در `/import_file/` وارد کنید.

## پیکربندی

- **فیلد خودکار پیش‌فرض**: فیلد خودکار پیش‌فرض به `django.db.models.BigAutoField` در `/d:/projects/khorami_library/config/settings.py` تنظیم شده است.
- **مدل کاربر سفارشی**: مدل کاربر سفارشی به عنوان `account.CustomUser` در `/d:/projects/khorami_library/config/settings.py` تعریف شده است.
- **آدرس بازگشت پس از ورود**: پس از ورود، کاربران به `/` هدایت می‌شوند که در `/d:/projects/khorami_library/config/settings.py` تعریف شده است.
- **آدرس بازگشت پس از خروج**: پس از خروج، کاربران به `/` هدایت می‌شوند که در `/d:/projects/khorami_library/config/settings.py` تعریف شده است.

## TODO

- استفاده از یک تولیدکننده رمز عبور قوی‌تر.

## مجوز

این پروژه تحت مجوز GNU General Public License v3.0 منتشر شده است.
