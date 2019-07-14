# GTMail - https://oauth.yandex.ru/client/a0b6bb2743304329bd2cbde756fe2d7a
# ID: a0b6bb2743304329bd2cbde756fe2d7a
# Пароль: 6d1d71d8a2b2418bb57d0d42a7026efd
# Callback URL: http://dmitrybobrovsky.ru
# token = {"token_type": "bearer", "access_token": "AgAAAAAigT1GAAWzDIvhjOnmRE81mGDc2Xk5M2U", "expires_in": 31535999, "refresh_token": "1:Ezt2KHSyQw2MfJ1n:xS0XJVFfnPwQYVEIzZ465ZCr5rSga3NnCJBl5bI_yHXUuQFinhwy:gH9zyaCyHKKXWFWfMtHDIA"}

from yandex_connect import token_get_by_code

token = token_get_by_code()
