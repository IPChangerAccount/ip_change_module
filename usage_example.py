# NOTES:
# 1) To use the IP change function import func change_ip from ip_change_module
# 2) The script that will use the module must run as administrator.

from ip_change_module import change_ip


print(f'Change IP result: {change_ip()}')