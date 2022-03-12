# project : group of application
# application : group of function
# application should be in small size => divide & conquer
# 언제 애플리케이션을 만들고 또 만들지 않아야 하는지 구분할 수 있어야 한다
# 한 문장으로 애플리케이션 표현 가능? don't use 'and'.
# ex. 이 애플리케이션은 유저 로그인 로그아웃 가입
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cnfg.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
